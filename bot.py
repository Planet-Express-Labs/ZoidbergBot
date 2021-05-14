import discord
from typing import Optional
from random import choice
from discord import Member, Guild, TextChannel, Message, PermissionOverwrite, Role, CategoryChannel, Reaction
from discord.ext.commands import Bot, Context, check_any, CheckFailure
from discord import RawReactionActionEvent
from discord.errors import HTTPException
from confessbot.state import state
from confessbot.config import *
from confessbot.strings import gets, String
from confessbot.utilities import generate_id, generate_code
from datetime import datetime
from io import BytesIO
from discord.ext import commands
import os

__version__ = "1.0 RELEASE CANDIDATE"

log = logging.getLogger(__name__)
bot = Bot(
    command_prefix=BOT_PREFIX
)

# "!conf" command
@bot.command()
async def conf(ctx, *, message=""):
    if (len(message) != 0) or (ctx.message.attachments != []):

        now = datetime.now()
        currentTime = now.strftime("%d/%m %H:%M")
        userID = ctx.message.author.id
        server = bot.get_guild(GUILD_ID)
        member = ctx.message.author
        # TODO: change this to sqlite3. Not here, in beta, but do that.
        print(now.strftime("%d/%m %H:%M"), file=open("output.txt", "a"))
        print(userID, file=open("output.txt", "a"))
        print(server, file=open("output.txt", "a"))
        print(member, file=open("output.txt", "a"))

        # Grabs channel IDS from config.
        # TODO: convert this to use a specific 
        channel = bot.get_channel(CHANNEL_ID)
        logChannel = bot.get_channel(LOG_ID)

        # Embed looks fancy.
        embed = discord.Embed(description=message)
        print(message, file=open("output.txt", "a"))
        # Set date/time as footer of embed
        embed.set_footer(text=currentTime)

        # Image attachments
        files = []
        for file in ctx.message.attachments:
            fp = BytesIO()
            await file.save(fp)
            files.append(discord.File(
                fp, filename=file.filename, spoiler=file.is_spoiler()))
            imageURL = ctx.message.attachments[0].url
            embed.set_image(url=imageURL)
            print("image" + imageURL)

        # Send embed message to channel
        await channel.send(embed=embed)
        embed.set_footer(text=currentTime + str(member))
        await logChannel.send(embed=embed)

        await ctx.send("Your message has been sent!")


    else:
        # TODO: Change this to use strings. 
        await ctx.send("Your message does not contain any content. Message failed.")
    print("--------------------------------------- END CONFESS ---------------------------------------",
          file=open("output.txt", "a"))


#############
# Discord events
#############

# Perhaps add an optional member join message? 
@bot.listen()
async def on_ready():
    log.info(f"Bot is ready: logged in as {bot.user.name} ({bot.user.id})")

    # Ensure the bot is like actually ready so it won't break. 
    await bot.wait_until_ready()


#############
# Normal commands
#############
@bot.command(name="ping", brief="The bot responds if alive")
async def cmd_ping(ctx: Context):
    await ctx.send(f"Pong! :ping_pong: \n :clock1: {0}" .format(round(bot.latency, 1)))


@bot.command(name="about", brief="Information about the bot. ")
async def cmd_about(ctx: Context):
    await ctx.send(gets(String.BOT_ABOUT).format(bot_mention=bot.user.mention, bot_version=__version__))


bot.run(BOT_TOKEN)
