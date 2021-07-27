from dislash import *
import discord
import textwrap


# Stolen, with permission from the dislash.py example bot:
# https://github.com/EQUENOS/slash-commands-example-bot/blob/main/pagination.py
# Many thanks to EQUENOS.

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
    temp = ''
    final = []
    print(text)
    for ind, each in enumerate(text):
        if ind % 4 == max_length:
            final.append(temp)
            temp = ''
        print(len(temp), temp)
        temp += each
    print(final)
    return final


def increment_page(page, index):
    page_length = len(page)
    if index + 1 > page_length:
        return index + 1
    return 0


def decrement_page(page, index):
    page_length = len(page)
    if index - 1 < page_length:
        return index - 1
    return page_length

    index = 0


async def paginate(text, channel, inter, ephemeral=False):
    pages = textwrap.wrap(inter.message.content, 4000)
    elements = []
    for each, index in enumerate(pages):
        elements.append(
            paginator.Element(
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
        description=text
    )
    msg = await inter.edit(embed=emb, components=button_row)

    # Click manager usage

    on_click = msg.create_click_listener(timeout=60)

    print(len(pages))

    if len(pages) == 0:
        for button in button_row:
            button.disabled = True
        await msg.edit(embed=emb, components=button_row)

    @on_click.matching_id("left")
    async def down(inter):
        global index
        index = decrement_page(pages, index)
        emb.description = pages[index]

    @on_click.matching_id("right")
    async def up(inter):
        global index
        index = increment_page(pages, index)
        emb.description = pages[index]

    @on_click.timeout
    async def on_timeout():
        for button in button_row:
            button.disabled = True
        await msg.edit(embed=emb, components=button_row)
