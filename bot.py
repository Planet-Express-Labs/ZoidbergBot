import logging
import discord
from typing import Optional
from random import choice
from asyncio import TimeoutError
from discord import Member, Guild, TextChannel, Message, PermissionOverwrite, Role, CategoryChannel, Reaction
from discord.ext.commands import Bot, Context, check_any, CheckFailure
from discord import RawReactionActionEvent
from discord.errors import HTTPException
from confessbot.state import state
from confessbot.config import BOT_TOKEN, BOT_PREFIX
from confessbot.strings import gets, String
from confessbot.utilities import generate_id, generate_code
from datetime import datetime
from io import BytesIO
from discord.ext import commands
import os

# This is a horrible hack. I will fix this later. Hopefully.
CHANNEL_ID = 769050998790291476

GUILD_ID = 769039315945914370

LOG_ID = 769062433314439199

Token = os.getenv("DISCORD_BOT_TOKEN")


logging.basicConfig(level=logging.INFO)
__version__ = "0.2.0"

log = logging.getLogger(__name__)
bot = Bot(
    command_prefix=BOT_PREFIX
)


# These functions cache the Guild, TextChannel and Message objects
async def get_main_guild() -> Guild:
    """
    :return: Guild that was configured for this bot to work on
    """
    stored: Optional[Guild] = state.get("main_guild")

    if stored is None:
        main_guild = bot.get_guild(GUILD_ID)
        state.set("main_guild", main_guild)
        return main_guild
    else:
        return stored


def find_category_by_id(guild: Guild, category_id: int) -> Optional[CategoryChannel]:
    category = None
    for c in guild.categories:
        if c.id == category_id:
            category = c
            break

    return category


# "!conf" command
@bot.command()
async def conf(ctx, *, message=""):
    # Error check: skips if message has no content or image
    if (len(message) != 0) or (ctx.message.attachments != []):

        now = datetime.now()
        currentTime = now.strftime("%d/%m %H:%M")

        # Obtains User ID and nickname to verify user is in guild/server
        userID = ctx.message.author.id
        server = bot.get_guild(GUILD_ID)
        member = ctx.message.author
        print(now.strftime("%d/%m %H:%M"), file=open("output.txt", "a"))
        print(userID, file=open("output.txt", "a"))
        print(server, file=open("output.txt", "a"))
        print(member, file=open("output.txt", "a"))

        # If member is a member of the server, they will have a name (instead of None)
        if member is not None:
            # Assigns Discord channel (given channel ID)
            channel = bot.get_channel(CHANNEL_ID)
            logChannel = bot.get_channel(LOG_ID)

            # datetime object containing current date and time

            # Create embed message (looks better)
            embed = discord.Embed(description=message)
            print(message, file=open("output.txt", "a"))
            # Set date/time as footer of embed
            embed.set_footer(text=currentTime)

            # Image attachments
            files = []
            for file in ctx.message.attachments:
                fp = BytesIO()
                await file.save(fp)
                files.append(discord.File(fp, filename=file.filename, spoiler=file.is_spoiler()))
                imageURL = ctx.message.attachments[0].url
                embed.set_image(url=imageURL)
                print("image" + imageURL)
            # The following prints the image as a separate message
            # await channel.send(files=files)

            # Send embed message to channel
            await channel.send(embed=embed)
            embed.set_footer(text=currentTime + str(member))
            await logChannel.send(embed=embed)

            # Inform user their message has been sent
            await ctx.send("Your message has been sent!")

        # If member is not a member is the server, they will be tagged None
        else:
            await ctx.send("You are not a member of the server! The message was not sent.")

    # If the message contains no image or text
    else:
        await ctx.send("Your message does not contain any content. Message failed.")
    print("--------------------------------------- END CONFESS ---------------------------------------",
          file=open("output.txt", "a"))


#############
# Discord events
#############
@bot.listen()
async def on_ready():
    log.info(f"Bot is ready: logged in as {bot.user.name} ({bot.user.id})")

    # Really make sure the internal cache is ready
    await bot.wait_until_ready()


"""
@bot.listen()
async def on_member_join(member: Member):


@bot.listen()
async def on_raw_reaction_add(payload: RawReactionActionEvent):
"""


#############
# Normal commands
#############
@bot.command(name="ping", brief="The bot responds if alive")
async def cmd_ping(ctx: Context):
    await ctx.send("Pong! :ping_pong:")


@bot.command(name="about", brief="A bit about the bot")
async def cmd_about(ctx: Context):
    await ctx.send(gets(String.BOT_ABOUT).format(bot_mention=bot.user.mention, bot_version=__version__))


bot.run(BOT_TOKEN)
