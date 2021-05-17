"""
8888888888P         d8b      888 888                                    888               888
      d88P          Y8P      888 888                                    888               888
     d88P                    888 888                                    888               888
    d88P    .d88b.  888  .d88888 88888b.   .d88b.  888d888 .d88b.       88888b.   .d88b.  888888
   d88P    d88""88b 888 d88" 888 888 "88b d8P  Y8b 888P"  d88P"88b      888 "88b d88""88b 888
  d88P     888  888 888 888  888 888  888 88888888 888    888  888      888  888 888  888 888
 d88P      Y88..88P 888 Y88b 888 888 d88P Y8b.     888    Y88b 888      888 d88P Y88..88P Y88b.
d8888888888 "Y88P"  888  "Y88888 88888P"   "Y8888  888     "Y88888      88888P"   "Y88P"   "Y888
                                                               888
                                                          Y8b d88P
                                                           "Y88P"
"""
# This software is provided free of charge without a warranty.
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
# This is designed to be used with Zoidberg bot, however I'm sure it could be adapted to work with your own projects.
# If there is an issue that might cause issue on your own bot, feel free to pull request if it will improve something.<3
from datetime import datetime
from io import BytesIO

import discord
from discord.ext import commands

from bot import bot
from zoidbergbot.config import *
from zoidbergbot.localization import get_string
from zoidbergbot.verify import verify_user


def find_url(url):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
            r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])) "
    return re.search(url, regex)


class Confess(commands.Cog):
    """Cog for confessing. As the name makes clear. """

    # noinspection PyShadowingNames
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="conf")
    async def cmd_conf(self, ctx, *, message=""):
        if (len(message) != 0) or (ctx.message.attachments != []):
            now = datetime.now()
            current_time = now.strftime("%d/%m %H:%M")

            # Obtains User ID and nickname to verify user is in guild/server
            user_id = ctx.message.author.id
            server = bot.get_guild(GUILD_ID)
            # Assigns Discord channel (given channel ID)
            channel = bot.get_channel(int(CHANNEL_ID))
            log_channel = bot.get_channel(int(LOG_ID))
            # last_message_id = ctx.channel.last_message_id

            if get_user_ban(user_id):
                await ctx.send(
                    "You have been temporarily blacklisted from sending confessions. \nThis could be a "
                    "permanent ban, or simply rate limiting. ")
                pass
            # Create embed. They're fancy
            embed = discord.Embed(description=f"{message}\n\n:id:: \n:card_box::")
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
                image_url = ctx.message.attachments[0].url
                embed.set_image(url=image_url)
                print("image" + image_url)
            image = str(find_url(message))
            if image is not None:
                embed.set_image(url=image)

            embed.set_footer(text=f"{current_time}")
            await msg.edit(embed=embed)

            # log message
            embed.set_footer(text="%s %s\n%s" % (current_time, str(user_id + 10), ctx.message.author))
            await log_channel.send(embed=embed)
            # Inform user their message has been sent
            await ctx.send("Your message has been sent!")

            # If the message contains no image or text
        else:
            await ctx.send("Your message does not contain any content. Message failed.")

    @cmd_conf.error
    async def conf_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Please wait before sending ')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have manage_messages permission')

    @commands.command(name="ban-confessions")
    async def cmd_ban_confessions(self, ctx, *, message=""):
        # TODO: convert everything to docstrings.
        """Bans a user from using confessions. A reason is not yet supported, but might be implemented soon:tm:.
        """
        if not verify_user(ctx, "admin"):
            await ctx.send(get_string("CMD_PERMISSION_ERROR"))
        else:
            if message is None:
                await ctx.send(get_string("COMMAND_EMPTY_USER_ID"))
            else:
                add_ban(message)
                await ctx.send(f":white_check_mark: Banned {0} from sending confessions.".format(bot.get_user(int(message))))

    @commands.command(name="unban-confessions", brief="Unbans a user from confessions. ")
    async def cmd_unban_confessions(self, ctx, *, message=""):
        if verify_user(ctx, "admin"):
            if message is None:
                await ctx.send(
                    "Please provide the user ID. To grab someone's ID, enable developer options in appearance, "
                    "right click their username and click ''Copy ID''")
            else:
                try:
                    rm_ban(int(message))
                except ValueError:
                    await ctx.send("Invalid ID. ID must be an integer. ")
                await ctx.send("User unbanned from sending confessions. ")
                print(f"{ctx.message.author} just unbanned {bot.get_user(int(message))}. ",
                      file=open("permissionLog.txt", "a"))
        else:
            await ctx.send(get_string("CMD_PERMISSION_ERROR"))

    @commands.command(name="confession-bans", brief="Lists all banned confession users. ")
    async def cmd_confession_bans(self, ctx):
        embed = discord.Embed(description="Getting bans, please wait.")
        message = ctx.send(embed=embed)
        if verify_user(ctx, "admin"):
            if get_bans() is not None:
                for each in get_bans():
                    embed += "\n {0}".format(bot.get_user(each))
                    message.edit(embed=embed)
            else:
                await ctx.send(get_string("NO_RESULTS"))
        else:
            await ctx.send(get_string("CMD_PERMISSION_ERROR"))


def setup(bot):
    bot.add_cog(Confess(bot))
