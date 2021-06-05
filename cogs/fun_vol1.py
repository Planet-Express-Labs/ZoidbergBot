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
import discord
from discord.ext import commands
import art

from bot import bot, BOT_PREFIX, slash
from zoidbergbot.verify import verify_user
from data.gifs import *
from zoidbergbot.localization import get_string

from dislash import slash_commands
from dislash.slash_commands import *
from dislash.interactions import *

import random
import base64
import aiohttp

# please ignore this list. It's so people don't slur. please thank me
bad_words = str(base64.b64decode("ZnVjayxiaXRjaCxjdW50LHJhcGUsbmlnZ2VyLG5pZ2dhLG5pZ2EsbmlnLGZhZ2dvdCxxdWVlcixyZXRhcmQsY"
                                 "XV0aXN0LGt5cyxhdXRpc3RpYyxjaGluayxjb29uLGpldyxkeWtlLGtpa2UscmFpZDpzc2hhZG93IGxlZ2VuZH"
                                 "Msbm9yZHZwbg=="), "utf-8").split(',')
words = ["hello"]
test_guild = 842987183588507670

# update this to not suck
last_index = 0


class FunVol1(commands.Cog):
    """Procrastination but as a module.
    """
    def __init__(self, bot):
        self.bot = bot
        # self.slash = slash

    @commands.command(name="big_text")
    async def cmd_big_text(self, ctx, *, message, style="big"):
        """Repeats your message but ***big***
        """
        await ctx.send(f"```{art.text2art(message, font=style)}```")
        await ctx.message.delete()

    @commands.command(name="random_art")
    async def cmd_random_art(self, ctx):
        """Sends a random piece of ASCII art from the python art library.
        """
        message = ctx.message
        await message.delete()
        await ctx.send(f"`{art.randart()}`")
        buttons = ActionRow(Button(
            style=ButtonStyle.blurple,
            label=""
        ))

    @commands.command(name="ceaser")
    async def cmd_ceaser(self, ctx, message, offset=1, inter=None, msg=None):
        """Literally nobody knows what this does. Kai just made it for some reason.
        (Silence liem (Next time capitalize.)
        """
        final = ""
        if type(message) is discord.Message:
            message = ctx.message.content
            await ctx.message.delete()
        for i in message:
            final += chr(int(ord(i))+int(offset))
        buttons = ActionRow(
            Button(
                style=ButtonStyle.green,
                label="Offset +",
                custom_id="add"
            ),
            Button(
                style=ButtonStyle.red,
                label="Offset -",
                custom_id="sub"
            )
        )

        try:
            if inter is None:
                msg = await ctx.send(f"```{final}```\noffset={offset}", components=[buttons])
            else:
                await inter.reply(f"```{final}```\noffset={offset}", components=[buttons], type=7)
        except ValueError:
            pass

        def wait_for(inter):
            return inter.message.id == msg.id

        inter = await ctx.wait_for_button_click(wait_for)
        # Send what you received
        if inter.clicked_button.custom_id == "add":
            await self.cmd_ceaser(ctx, message, offset + 1, inter, msg)
        if inter.clicked_button.custom_id == "sub":
            await self.cmd_ceaser(ctx, message, offset - 1, inter, msg)

    @commands.command(name="lonely")
    async def cmd_lonely(self, ctx, *, message):
        # message = ctx.message.content.strip(BOT_PREFIX + "lonely").split(' ')
        message = message.split(' ')
        if int(len(words)) < 500:
            for i in message:
                # this is so bad. I don't care tho.
                if (i in words) is False and int(len(i)) < 20 and not (i in bad_words):
                    words.append(i)

        iters = range(random.randint(2, 15))

        final = ""
        prev = ""
        for i in iters:
            idx = random.randint(0, int(len(words))-1)
            if words[idx] != prev:
                final += words[idx] + " "
            prev = words[idx]

        await ctx.send(final)

    @commands.command(name="get_words")
    async def cmd_get_words(self, ctx):
        if verify_user(ctx, "admin"):
            await ctx.send(words)
        else:
            await ctx.send("No ")

    @commands.command(name="reset_words")
    async def cmd_reset_words(self, ctx):
        if verify_user(ctx, "admin"):
            words = ["hello"]
            await ctx.send("Done!")
        else:
            await ctx.send("No ")

    @commands.command(name="blockchain_ceaser")
    async def cmd_blockchain_ceaser(self, ctx, *, message, inter=None, msg = None):
        net_value = 0
        prev_values = []

        for i in message:
            val = int(ord(i))
            net_value += val
            prev_values.append(net_value + val)

        final = ""
        for i in prev_values:
            final += chr(i)

        await ctx.send(final)

    @commands.command(name="slap")
    async def cmd_slap(self, ctx, person, lastIndex=last_index, loops=0):
        """Slap your friends for fun. 👏
        """
        if loops > 10:
            await ctx.send(get_string("UNKNOWN_ERROR") + " TIMEOUT EXCEEDED \n COMMAND: " + ctx.message.content)
            return
        index = random.randint(0, len(slap) - 1)
        timeout = 0
        while (index != lastIndex | lastIndex != 0) & timeout > 10:
            timeout += 1
            index = random.randint(0, len(slap) - 1)
        async with aiohttp.ClientSession() as session:
            async with session.get(slap[index]) as r:
                print(r.status)
                if r.status == 404:
                    print([index], "is a dead link!")
                    await self.cmd_slap(ctx, person, lastIndex, loops + 1)
        lastIndex = index
        embed = discord.Embed(title="SLAPPED!", colour=discord.Colour(0x007E5F))
        embed.add_field(name="Slapped:", value=f"{person} (real person!)")
        # TODO: make this use a self hosted CDN instead of random peoples.
        embed.set_image(url=slap[index])
        await ctx.send(embed=embed)

    # Ignore this - It's example code to teach Kai.

    # @commands.command(name="simple_interaction")
    # async def cmd_simple(self, ctx):
    #     buttons = ActionRow(
    #         Button(
    #             style=ButtonStyle.blurple,
    #             label="Click me!",
    #             custom_id="interaction"
    #         ),
    #         Button(
    #             style=ButtonStyle.danger,
    #             label="Don't click me!",
    #             custom_id="bad"
    #         )
    #     )
    #     msg = await ctx.send("click the good one", components=[buttons])
    #
    #     def wait_for(inter):
    #         return inter.message.id == msg.id
    #
    #     inter = await ctx.wait_for_button_click(wait_for)
    #
    #     if inter.clicked_button.custom_id == "interaction":
    #         await inter.reply("Thank you, kind sir")
    #     elif inter.clicked_button.custom_id == "bad":
    #         embed = discord.Embed()
    #         embed.set_image(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia.giphy.com%2Fmedia"
    #                             "%2Fd3MEQYJQpJSKs%2Fgiphy.gif&f=1&nofb=1")
    #         await inter.reply(embed=embed)

    @commands.command(name="discord_friends")
    async def cmd_discord_friends(self, ctx, person):
        row_of_buttons = ActionRow(
            Button(
                style=ButtonStyle.green,
                label="Accept",
                custom_id="green"
            ),
            Button(
                style=ButtonStyle.red,
                label="Decline",
                custom_id="red"
            )
        )

        # Send a message with buttons
        msg = await ctx.send(
            "This message has buttons!",
            components=[row_of_buttons]
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(get_string("COMMAND_EMPTY"))

def setup(bot):
    bot.add_cog(FunVol1(bot))
