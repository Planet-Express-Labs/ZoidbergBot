import discord

from io import BytesIO
from discord.ext import commands
from dislash import *

from cogs.data import NLP
from bot import bot
from zoidbergbot.paginator import Element


async def summarize_text(text):
    nlp = NLP.BartCnn()
    return str(await nlp.summarize(text))


async def summary(channel, message, inter):
    text = []
    for file in message.attachments:
        bytes_io = BytesIO()
        await file.save(bytes_io)

        byte = bytes_io.read()
        content = byte.decode("utf-8")

        await inter.reply(type=5)
        text.append(await summarize_text(content))

    embed = discord.Embed(title="Summarized text:", description='')
    for each in text:
        embed.description += each
    await inter.edit(embed=embed)


async def paginate(message, channel, emphemeral=False):
    content = bytes.read()
    pages = commands.Paginator(max_size=4000)
    elements = []
    for each, index in enumerate(pages):
        elements.append(
            Element(
                header=f"Page {index}:",
                long_desc=each
            )
        )
    menu = Element(
        header="Message content",
        elements=elements
    )
    # Build buttons
    button_row = ActionRow(
        auto_rows(2),
        Button(
            style=ButtonStyle.blurple,
            emoji="⬆",
            custom_id="up"
        ),
        Button(
            style=ButtonStyle.green,
            label="Select",
            custom_id="select"
        ),
        Button(
            style=ButtonStyle.blurple,
            emoji="⬇",
            custom_id="down"
        ),
        Button(
            style=ButtonStyle.red,
            label="Back",
            custom_id="back"
        )
    )
    # Send a message with buttons
    emb = discord.Embed(
        title=menu.header,
        description=f"{menu.long_desc}\n\n{menu.display_elements()}"
    )
    msg = await channel.send(embed=emb, components=[button_row], emphemeral=emphemeral)

    # Click manager usage

    on_click = msg.create_click_listener(timeout=60)

    @on_click.matching_id("down")
    async def down(inter):
        menu.next_elem()

    @on_click.matching_id("up")
    async def up(inter):
        menu.prev_elem()

    @on_click.matching_id("select")
    async def select(inter):
        nonlocal menu
        menu = menu.element

    @on_click.matching_id("back")
    async def back(inter):
        nonlocal menu
        menu = menu.parent

    @on_click.no_checks()
    async def response(inter):
        emb.title = menu.header
        emb.description = f"{menu.long_desc}\n\n{menu.display_elements()}"
        await inter.reply(embed=emb, type=ResponseType.UpdateMessage)

    @on_click.timeout
    async def on_timeout():
        for button in button_row.components:
            button.disabled = True
        await msg.edit(embed=emb, components=[button_row])


async def txt_file(file, message):
    channel = message.channel
    await channel.send(
        "TXT file detected.",
        components=[
            SelectMenu(
                custom_id="test",
                placeholder="Choose an action",
                max_values=1,
                options=[
                    SelectOption("Send message content here", f"content,{message.id},{channel.id}"),
                    # This is a garbage hack.
                    SelectOption("Summarize content", f"summary,{message.id},{channel.id}")
                ]
            )
        ]
    )


class FileTools(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_dropdown(self, inter: MessageInteraction):
        options = str([option.value for option in inter.select_menu.selected_options][0]).split(',')
        print(options)
        print(options)
        label = options[0]
        message_id = int(options[1])
        channel_id = int(options[2])
        channel = bot.get_channel(channel_id)
        message = channel.fetch_message(message_id)
        if label == "summary":
            await summary(channel, message, inter)
        if label == "content":
            await paginate(channel, message, inter)

    @commands.Cog.listener()
    async def on_message(self, message):
        for file in message.attachments:
            if ".txt" in file.filename:
                await txt_file(file, message)

def setup(bot):
    bot.add_cog(FileTools(bot))
