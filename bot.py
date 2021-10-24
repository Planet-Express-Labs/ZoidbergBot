# This software is provided free of charge without a warranty. 
# This Source Code Form is subject to the terms of the Mozilla Public License, 
# v. 2.0. If a copy of the MPL was this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import discord
import os
from discord.ext import commands
from dislash import *
from base64 import b64decode
from tortoise import Tortoise, run_async

from zoidbergbot.config import *
from zoidbergbot.localization import get_string

__version__ = get_string("VERSION")
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
activity = discord.Activity(name='zoidberg.pexl.pw', type=discord.ActivityType.playing)


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url=DATABASE,
        modules={'models': ['zoidbergbot.database.filter_db', 'zoidbergbot.database.confess_channel']}
    )

    # Generate the schema, only run on new
    if os.getenv("zoidberg_has_run") != 1:
        await Tortoise.generate_schemas()
        os.environ['zoidberg_has_run'] = '1'


# run_async is a helper function to run simple async Tortoise scripts.
# run_async(init())
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix='-=',
    activity=activity,
    intents=intents
)
slash_client = InteractionClient(bot)

# TODO: Move both of these into the config file., test_guilds=TEST_GUILDSshow_warnings=True
guilds = TEST_GUILDS

blocked_cogs = []
failed_cogs = []

for filename in os.listdir("cogs"):
    if filename.endswith(".py") and filename not in blocked_cogs:
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
        except commands.ExtensionNotLoaded:
            failed_cogs.append(filename)


@bot.event
async def on_ready():
    print(f"Bot is ready: logged in as {bot.user.name} ({bot.user.id})")
    await init()
    await bot.wait_until_ready()


@slash_client.command(name="ping", description="Replies with Zoidberg's response time.")
async def cmd_ping(ctx):
    """Check if the bots alive and what the latency is. """
    await ctx.reply(f"Pong! :ping_pong:       Latency: {0} ms".format(bot.latency))


@slash_client.slash_command(name="about", description="Provides  some information about the bot.", guild_ids=guilds)
async def cmd_about(ctx):
    """About the bot. """
    embed = discord.Embed(
        description=get_string("BOT_ABOUT").format(bot_mention=bot.user.mention, bot_version=__version__) +
        f"\n\nI'm in {len(bot.guilds)} servers. ",
        title="Zoidberg",
        url="https://github.pexl.pw")
    embed.set_footer(text="How we use your data: https://privacy.pexl.pw/")
    embed.set_author(name="Zoidberg v" + __version__,
                     icon_url="https://i.imgur.com/wWa4zCM.png",
                     url="https://github.pexl.pw")
    embed.set_thumbnail(
        url="https://user-images.githubusercontent.com/45272685/118345209-fb8ecf80-b500-11eb-9f24-d662a27818dc.jpg")
    await ctx.reply(embed=embed)


@slash_client.command(name="modules", description="Shows the currently loaded modules.", guild_ids=guilds)
async def cmd_modules(ctx):
    global failed_cogs
    sm = b64decode("YWksZmlsZV90b29scyxoZWxwLG1vZGVyYXRpb24sbXVzaWMsZnVuLTEsdHJhbnNsYXRlLHJvbGVz")
    sm = sm.decode().split(',')
    modules = []
    for filename in os.listdir("cogs"):
        if filename.endswith(".py") and filename not in blocked_cogs:
            modules.append(filename[:-3])

    embed = discord.Embed(title="Modules:", description="")
    embed.set_footer(text="yellow_circle - unofficial module\nZoidberg v" + str(__version__))
    for each in sm:
        if each not in modules:
            failed_cogs += each
            embed.description += f"{each}: :red_circle:\n"
    for module in modules:
        if module not in sm:
            embed.description += f"{module}: :yellow_circle:\n"
        else:
            embed.description += f"{module}: :green_circle:\n"
    await ctx.reply(embed=embed)


@slash_client.command(name="invite", description="Sends a bot invite link.", guild_ids=guilds)
async def cmd_invite(ctx):
    """About the bot. """
    embed = discord.Embed(
        description="Invite Zoidberg to your server. ",
        title="Zoidberg",
        url="https://discord.com/api/oauth2/authorize?client_id=769035491278061639&permissions=8&scope=bot"
            "%20applications.commands")
    embed.set_author(name="Zoidberg v" + __version__,
                     icon_url="https://i.imgur.com/wWa4zCM.png",
                     url="https://github.com/LiemEldert/ZoidbergBot")
    embed.set_thumbnail(
        url="https://user-images.githubusercontent.com/45272685/118345209-fb8ecf80-b500-11eb-9f24-d662a27818dc.jpg")
    await ctx.reply(embed=embed)


bot.run(BOT_TOKEN)
