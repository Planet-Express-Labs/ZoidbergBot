# This software is provided free of charge without a warranty. 
# This Source Code Form is subject to the terms of the Mozilla Public License, 
# v. 2.0. If a copy of the MPL was this file, You can obtain one at https://mozilla.org/MPL/2.0/.
import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import Context
from dislash import slash_commands, Option, Type, Interaction

from bot import guilds
from zoidbergbot import localization
from cogs.api import ms_content_moderation
import textwrap


class TextFiltering(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #
    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.author.id != self.bot.user.id:
    #         channel = message.channel
    #         chunks = textwrap.wrap(message.content, 1024)
    #         result = []
    #         print(chunks)
    #         for each in chunks:
    #             print(each)
    #             result.append(ms_content_moderation.text_moderation(each))
    #             if len(chunks) > 1:
    #                 await asyncio.sleep(1)
    #         print(result)
    #         await channel.send(result)


def setup(bot):
    bot.add_cog(TextFiltering(bot))
