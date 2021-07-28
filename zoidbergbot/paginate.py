from dislash import *
import discord
import textwrap


# Stolen, with permission from the dislash.py example bot:
# https://github.com/EQUENOS/slash-commands-example-bot/blob/main/pagination.py
# Many thanks to EQUENOS.


async def progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    return f'\r{prefix} |{bar}| {percent}% {suffix}'


class Menu:
    def __init__(self):
        self.pages = []

    def add_page(self, name, description, type):
        if type == "int":
            buttons = ActionRow(
                Button(
                    style=ButtonStyle.green,
                    label="+",
                    custom_id="add"
                ),
                Button(
                    style=ButtonStyle.red,
                    label="-",
                    custom_id="sub"
                )
            )

        self.pages.update({"name": name, "buttons": buttons, "description": description})

    async def send_pages(self, ctx):
        buttons = []
        for page in self.pages:
            buttons.append(page["buttons"])

        rows = auto_rows(*buttons)
        msg = await ctx.send(content=rows)
        on_click = msg.create_click_listener(timeout=60)

        @on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=False)
        async def on_wrong_user(inter):
            # Reply with a hidden message
            await inter.reply(
                "This command's buttons can only be used by the person who originally sent it for security reasons.",
                ephemeral=True)

        @on_click.matching_id("test_button")
        async def on_test_button(ctx):
            await ctx.reply("You've clicked the button!")


class Element:
    def __init__(self, *, header, short_desc=None, long_desc=None, elements=None):
        self._parent = None
        self.header = header
        self.short_desc = short_desc or ""
        self.long_desc = long_desc or ""
        self.elements = elements or []
        self.current = 0
        # Set parents
        for elem in self.elements:
            elem._parent = self

    @property
    def parent(self):
        return self if self._parent is None else self._parent

    @property
    def element(self):
        if len(self.elements) == 0:
            return self
        return self.elements[self.current]

    def next_elem(self):
        if len(self.elements) > 0:
            self.current = (self.current + 1) % len(self.elements)

    def prev_elem(self):
        if len(self.elements) > 0:
            self.current = (self.current - 1) % len(self.elements)

    def display_elements(self, sep="\n"):
        table = ""
        for i, elem in enumerate(self.elements):
            table = f"{table}{sep}{elem.display(1, i == self.current)}"
        return table[len(sep):]

    def display(self, depth=0, highlight=False):
        header = f"**{self.header}**" if not highlight else f"> **{self.header}**"
        content = self.long_desc if depth == 0 else self.short_desc
        content = f"{header}\n{content}"
        # Also display children
        if len(self.elements) > 0 and depth < 1:
            content = f"{content}\n{self.display_elements()}"
        return content.strip()


def paginator(text, max_length):
    # too lazy to actually fix
    return textwrap.wrap(text, max_length)


async def paginate(text, channel, inter, ephemeral=False):
    print(text)
    pages = textwrap.wrap(text, 4000)
    elements = []
    for each, index in enumerate(pages):
        elements.append(
            Element(
                header=f"Page {index}:",
                long_desc=each
            )
        )

    # Build buttons
    button_row = auto_rows(
        Button(
            style=ButtonStyle.blurple,
            emoji="⬅️",
            custom_id="left",
            disabled=False
        ),
        Button(
            style=ButtonStyle.blurple,
            emoji="➡️",
            custom_id="right",
            disabled=False
        ),
        max_in_row=2
    )
    # Send a message with buttons
    emb = discord.Embed(
        title="Message content:",
        description=pages[0]
    )
    msg = await inter.edit(embed=emb, components=button_row)

    # Click manager usage

    on_click = msg.create_click_listener(timeout=60)
    print(len(pages))
    index = 0
    if len(pages) == 0:
        for button in button_row:
            button.disabled = True
        await msg.edit(embed=emb, components=button_row)

    def increment_page(page):
        page_length = len(page)
        temp = index
        if index + 1 > page_length:
            return index + 1
        return 0

    def decrement_page(page):
        page_length = len(page)
        if index - 1 < page_length:
            return index - 1
        return page_length

    @on_click.matching_id("right")
    async def down(inter):
        index = decrement_page(pages)
        emb.description = pages[index]
        await msg.edit(embed=emb, components=button_row)
        await inter.reply(type=6)

    @on_click.matching_id("left")
    async def up(inter):
        index = increment_page(pages)
        emb.description = pages[index]
        await msg.edit(embed=emb, components=button_row)
        await inter.reply(type=6)

    @on_click.timeout
    async def on_timeout():
        for button in button_row:
            button.disabled = True
        await msg.edit(embed=emb, components=button_row)