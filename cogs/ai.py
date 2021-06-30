import re
from discord.ext import commands
from discord.ext.commands.errors import ConversionError
from dislash import SlashInteraction, ActionRow, Button, slash_commands, Element, Type, Option

from bot import guilds
from data.gifs import *
from zoidbergbot.localization import get_string
from zoidbergbot.verify import verify_user
from cogs.data import NLP


def trim(input, max, min):
    if input > max:
        input = max
    elif input < min:
        input = min
    return input


class Ai(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Ai(bot))
