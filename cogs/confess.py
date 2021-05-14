"""
  ____             __ _           _
 / ___|___  _ __  / _| |__   ___ | |_
| |   / _ \| '_ \| |_| '_ \ / _ \| __|
| |__| (_) | | | |  _| |_) | (_) | |_
 \____\___/|_| |_|_| |_.__/ \___/ \__|


 ____  _____ _____  _      ____  ____      _    _   _  ____ _   _
| __ )| ____|_   _|/ \    | __ )|  _ \    / \  | \ | |/ ___| | | |
|  _ \|  _|   | | / _ \   |  _ \| |_) |  / _ \ |  \| | |   | |_| |
| |_) | |___  | |/ ___ \  | |_) |  _ <  / ___ \| |\  | |___|  _  |
|____/|_____| |_/_/   \_\ |____/|_| \_\/_/   \_\_| \_|\____|_| |_|
"""
# This software is provided free of charge without a warranty - meaning if you're an idiot and somehow
# blow up your sever, I am not liable or responsible.
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# This is designed as a component for confbot. Use outside of that is not supported.
# Do not create an issue on the repo if this is used outside of the main bot. If you create one, it will be closed.
import asyncio
from datetime import datetime
from io import BytesIO
import re

import discord
from discord.ext import commands

from bot import bot, permissionLevels
from confessbot.strings import gets, String
from confessbot.verify import verify_user
from confessbot.config import *

def find_url(input):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
            r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])) "
    return re.search(input, regex)

class Confess(commands.Cog):
    """Cog for confessing. As the name makes clear. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="conf")
    async def cmd_conf(self, ctx, *, message=""):
        # Error check: skips if message has no content or image
        if (len(message) != 0) or (ctx.message.attachments != []):
            if not find_url(message):

            else:

            now = datetime.now()
            current_time = now.strftime("%d/%m %H:%M")

            # Obtains User ID and nickname to verify user is in guild/server
            user_id = ctx.message.author.id
            server = bot.get_guild(GUILD_ID)
            # Assigns Discord channel (given channel ID)
            channel = bot.get_channel(int(CHANNEL_ID))
            logChannel = bot.get_channel(int(LOG_ID))
            # last_message_id = ctx.channel.last_message_id

            # TODO: reformat this and add better logging options.
            print(now.strftime("%d/%m %H:%M"), file=open("../output.txt", "a"))
            print(user_id, file=open("../output.txt", "a"))
            print("Guild ID:", GUILD_ID)
            print(server, file=open("../output.txt", "a"))
            print("Channel:", CHANNEL_ID, channel, file=open("../output.txt", "a"))
            print("Log:", LOG_ID, file=open("../output.txt", "a"))
            print(str(ctx.message.author).encode("utf-8"), file=open("../output.txt", "a"))
            print(ctx.message)

            print(CONFESS_BANS)
            for each in CONFESS_BANS:
                print(each)
                if user_id == each:
                    await ctx.send(
                        "You have been temporarily blacklisted from sending confessions. \nThis could be a "
                        "permanent ban, or simply rate limiting. ")
                    return None
            # Create embed. They're fancy
            embed = discord.Embed(description=f"{message}\n\n:id:: \n:card_box::")
            print(message, file=open("../output.txt", "a"))
            embed.set_footer(text=f"Pulling info. ")
            # Send embed.
            msg = await channel.send(embed=embed)
            embed = discord.Embed(
                description=f"{message}  \n\n:id:: {msg.id}")
            files = []
            for file in ctx.message.attachments:
                fp = BytesIO()
                await file.save(fp)
                files.append(discord.File(fp, filename=file.filename, spoiler=file.is_spoiler()))
                imageURL = ctx.message.attachments[0].url
                embed.set_image(url=imageURL)
                print("image" + imageURL)
            url = find_url(message)
            if url is not None:
                imageURL = url
            await asyncio.sleep(3)
            embed.set_footer(text=f"{current_time}")
            await msg.edit(embed=embed)

            # log message
            embed.set_footer(text="%s %s\n%s" % (current_time, str(user_id + 10), ctx.message.author))
            await logChannel.send(embed=embed)
            # Inform user their message has been sent
            await ctx.send("Your message has been sent!")

        # If the message contains no image or text
        else:
            await ctx.send("Your message does not contain any content. Message failed.")
        print("--------------------------------------- END CONFESS ---------------------------------------",
              file=open("../output.txt", "a"))

    @cmd_conf.error
    async def conf_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Please wait before sending ')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have manage_messages permission')

    @commands.command(name="announcement")
    async def cmd_conf_announcement(self, ctx, message):
        channel = bot.get_channel(int(CHANNEL_ID))
        if verify_user(ctx, "admin"):
            embed = discord.Embed(body=ctx.message, color=0xFF5733, title="Confession Announcement",
                                  footer=f"confessbot v{String.VERSION}.")
            await ctx.send(embed=embed)

            async def confirm(m):
                await ctx.send('Please reply "Confirm" to send the message.')

            try:
                send = await bot.wait_for('message', check=confirm, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send('Timed out.')
            if send == "Confirm":
                await channel.send(embed=embed)

        else:
            await ctx.send("You do not have sufficient permissions to run that command. This event will be logged, "
                           "Daddy is disappointed. ")
            print(f"{ctx.message.author} just attempted to use set-status without proper permissions. ",
                  file=open("permissionLog.txt", "a"))

    @commands.command(name="ban-confessions", brief="Bans a user from using confessions. A reason is not yet supported, "
                                               "but might be implemented soon:tm:. ")
    async def cmd_ban_confessions(self, ctx, *, message=""):
        if verify_user(ctx, "admin"):
            if message is None:
                await ctx.send(
                    "Please provide the user ID. To grab someone's ID, enable developer options in appearance, "
                    "right click their username and click ''Copy ID''")
            else:
                add_banned_user(int(message))
                await ctx.send("User banned from sending confessions.")
        else:
            await ctx.send(
                "You do not have sufficient permissions (%s) to run that command. This event will be logged, "
                "Daddy is disappointed. " % "dev")
            print(f"{ctx.message.author} just attempted to use set-status without proper permissions. ",
                  file=open("permissionLog.txt", "a"))

    @commands.command(name="unban-confessions", brief="Unbans a user from confessions. ")
    async def cmd_unban_confessions(self, ctx, *, message=""):
        if verify_user(ctx, "admin"):
            if message is None:
                await ctx.send(
                    "Please provide the user ID. To grab someone's ID, enable developer options in appearance, "
                    "right click their username and click ''Copy ID''")
            else:
                try:
                    remove_banned_user(int(message))
                except ValueError:
                    await ctx.send("Invalid ID. ")
                await ctx.send("User unbanned from sending confessions. ")
                print(f"{ctx.message.author} just unbanned {bot.get_user(int(message))}. ",
                      file=open("permissionLog.txt", "a"))
        else:
            await ctx.send(
                "You do not have sufficient permissions (%s) to run that command. This event will be logged, "
                "Daddy is disappointed. " % "dev")
            print(f"{ctx.message.author} just attempted to use set-status without proper permissions. ",
                  file=open("permissionLog.txt", "a"))
    
    @commands.command(name="confession-bans", brief="Lists all banned confession users. ")
    async def cmd_confession_bans(self, ctx, *, message=""):
        embed = discord.Embed(description=f"Pulling bans, please wait.")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Confess(bot))
