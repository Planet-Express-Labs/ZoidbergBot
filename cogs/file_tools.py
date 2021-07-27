# 8888888888P         d8b      888 888                                    888               888
#       d88P          Y8P      888 888                                    888               888
#      d88P                    888 888                                    888               888
#     d88P    .d88b.  888  .d88888 88888b.   .d88b.  888d888 .d88b.       88888b.   .d88b.  888888
#    d88P    d88""88b 888 d88" 888 888 "88b d8P  Y8b 888P"  d88P"88b      888 "88b d88""88b 888
#   d88P     888  888 888 888  888 888  888 88888888 888    888  888      888  888 888  888 888
#  d88P      Y88..88P 888 Y88b 888 888 d88P Y8b.     888    Y88b 888      888 d88P Y88..88P Y88b.
# d8888888888 "Y88P"  888  "Y88888 88888P"   "Y8888  888     "Y88888      88888P"   "Y88P"   "Y888
# This software is provided free of charge without a warranty.   888
# This Source Code Form is subject to the terms of the      Y8b d88P
# Mozilla Public License, v. 2.0. If a copy of the MPL was   "Y88P"
# this file, You can obtain one at https://mozilla.org/MPL/2.0/.

# This is designed to be used with Zoidberg bot, however I'm sure it could be adapted to work with your own projects.
# If there is an issue that might cause issue on your own bot, feel free to pull request if it will improve something.<3
from io import BytesIO
from discord.ext import commands
from cogs.data import NLP
from zoidbergbot.paginate import *


async def summarize_text(text):
    nlp = NLP.BartCnn()
    return str(await nlp.summarize(text))


async def summary(message, inter):
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


async def txt_file(message):
    channel = message.channel
    embed = discord.Embed(title="TXT file detected. ")
    embed.set_footer(text="This feature is in beta, and is only enabled in certain guilds. More actions and file"
                          "types will be added soon. ")
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
        # Let's eliminate edge-cases to an alarming degree!
        if option not in labels and len(option) == 1 and len(option[0]) > 10:
            options = str([option.value for option in inter.select_menu.selected_options][0]).split(',')
            print(options)
            print(options)
            label = options[0]
            message_id = int(options[1])
            channel_id = int(options[2])
            channel = self.bot.get_channel(channel_id)
            message = await channel.fetch_message(message_id)
            if label == "summary":
                await summary(message, inter)
            if label == "content":
                file = message.attachments[0]
                bytes_io = BytesIO()
                await file.save(bytes_io)
                byte = bytes_io.read()
                text = byte.decode()
                print(text)
                await inter.reply(type=5)
                await paginate(text, channel, inter)

    @commands.Cog.listener()
    async def on_message(self, message):
        for file in message.attachments:
            if ".txt" in file.filename:
                await txt_file(message)


def setup(bot):
    bot.add_cog(FileTools(bot))
