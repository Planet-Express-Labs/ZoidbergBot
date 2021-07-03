import discord

from io import BytesIO

from discord.ext import commands
from dislash import SelectMenu, MessageInteraction, SelectOption

from cogs.data import NLP
from bot import bot


async def summarize_text(text):
    nlp = NLP.BartCnn()
    return str(await nlp.summarize(text))


async def paginate(bytes, ctx):
    content = bytes.read()
    pages = commands.Paginator(max_size=4000)
    ctx.send()


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
                    SelectOption("Send message content here", f"content,{message.id},{channel.id}"),  # This is a garbage hack.
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
        if label == "summary":
            message = await channel.fetch_message(message_id)
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

    @commands.Cog.listener()
    async def on_message(self, message):
        for file in message.attachments:
            if ".txt" in file.filename:
                await txt_file(file, message)


def setup(bot):
    bot.add_cog(FileTools(bot))
