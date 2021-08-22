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
import asyncio
import aiohttp
import json

import discord
from discord.ext import commands
from discord.ext.commands import Context
from dislash import slash_commands, Option, Type, Interaction

from bot import guilds
from zoidbergbot import localization
from zoidbergbot.config import AI21_API_KEY


class AI21(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='talk',
                            description='This command allows you to talk to zoidberg and make him do your work. ',
                            testing_guilds=guilds,
                            options=[
                                Option('input', 'Your query to Zoidberg.', Type.STRING, required=True),
                            ]
                            )
    async def ai21Query(self, ctx):
        input = ctx.get('input')
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.ai21.com/studio/v1/j1-large/complete",
                                    headers={"Authorization": "Bearer " + AI21_API_KEY},
                                    data={
                                        "prompt": input,
                                        "numResults": 1,
                                        "maxTokens": 8,
                                        "stopSequences": ["."],
                                        "topKReturn": 0,
                                        "temperature": 0.0
                                    }) as response:
                data = await response.text()
                data = json.loads(data)
                print(data)
                data = data['completions']['data']['text']
        await ctx.reply(data)


def setup(bot):
    bot.add_cog(AI21(bot))
