import discord

from io import BytesIO
from discord.ext import commands
from dislash import *

from cogs.data import NLP
from bot import bot
from zoidbergbot.paginate import *


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
        labels = ["summary", "content"]
        option = [option.value for option in inter.select_menu.selected_options]
        first_option = option[0]
        # Let's eliminate edgecases to an alarming degree!
        if option not in labels and len(option) == 1 and len(option[0] > 10) and first_option[10].type in range(9):
            options = str([option.value for option in inter.select_menu.selected_options][0]).split(',')
            print(options)
            print(options)
            label = options[0]
            message_id = int(options[1])
            channel_id = int(options[2])
            channel = bot.get_channel(channel_id)
            message = await channel.fetch_message(message_id)
            if label == "summary":
                await summary(channel, message, inter)
            if label == "content":
                file = message.attachments[0]
                bytes_io = BytesIO()
                await file.save(bytes_io)
                byte = bytes_io.read()
                text = byte.decode()[0]
                await inter.reply(type=5)
                await paginate(text, channel, inter)

    @commands.Cog.listener()
    async def on_message(self, message):
        for file in message.attachments:
            if ".txt" in file.filename:
                await txt_file(file, message)


def setup(bot):
    bot.add_cog(FileTools(bot))
