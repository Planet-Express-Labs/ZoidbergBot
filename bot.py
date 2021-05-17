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
# This software is provided free of charge without a warranty - meaning if you're an idiot and somehow
# blow up your sever, I am not liable or responsible.
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# This is designed to be used with Zoidberg bot, however I'm sure it could be adapted to work with your own projects.
# If there is an issue that might cause issue on your own bot, feel free to pull request if it will improve something.<3

import discord
from discord.ext.commands import Bot, Context

from zoidbergbot.config import *
from zoidbergbot.localization import get_string
from zoidbergbot.verify import verify_user

__version__ = get_string("VERSION")
logging.basicConfig(level=exec(LOGGING_LEVEL))

log = logging.getLogger(__name__)
bot = Bot(
    command_prefix=BOT_PREFIX
)

bot.load_extension("cogs.confess")


@bot.listen()
async def on_ready():
    log.info(f"Bot is ready: logged in as {bot.user.name} ({bot.user.id})")

    # Really make sure the internal cache is ready
    await bot.wait_until_ready()
    # await bot.change_presence(status=discord.Status.idle, activity="DM me !conf to confess text/images.")


class Main:

    def __init__(self):
        pass

    @bot.command(name="ping", brief="The bot responds if alive")
    async def cmd_ping(self, ctx: Context):
        # Literally just responds with this.
        await ctx.send(f"Pong! :ping_pong: \n :clock1: {0}".format(round(bot.latency, 1)))

    @bot.command(name="about", brief="A bit about the bot")
    async def cmd_about(self):
        # Oh no - the paragraphs.
        embed = discord.Embed(description=get_string("BOT_ABOUT").format(bot_mention=bot.user.mention,
                                                                         bot_version=__version__), title="Zoidberg")
        embed.set_author("LiemEldert/Sopmk/Sky", "https://github.com/LiemEldert", "https://cdn.discordapp.com/channel"
                                                                                  "-icons/812042455746740234"
                                                                                  "/f8c312e61a3cf74d73d6ba8583edf8b9"
                                                                                  ".webp?")
        embed.set_thumbnail("https://github.com/LiemEldert",
                            "https://user-images.githubusercontent.com/45272685/118345209-fb8ecf80-b500-11eb-9f24"
                            "-d662a27818dc.jpg")
        embed.url("https://github.com/LiemEldert/ZoidbergBot/")

    @bot.command(name="check-special", brief="Checks if user has any special roles configured within the bot. ")
    async def cmd_check_perms(self, ctx, message):
        # TODO: change how this is handled. This will likely just be moved into a differ ent function. Works fine as
        #  is, however.
        permission_levels = ["dev", "admin"]
        await ctx.send("Checking user permissions... ")
        for each in permission_levels:
            message += f"{each}: {verify_user(ctx, each)}\n"
            if "True" in message:
                message += "\n:green_circle:"
            else:
                message += "\n:red_circle"
        embed = discord.Embed(description=message, title="Special Permissions: ")
        await ctx.send(embed=embed)


bot.run(BOT_TOKEN)
