# This is designed to be used with Zoidberg bot, however I'm sure it could be adapted to work with your own projects.
# If there is an issue that might cause issue on your own bot, feel free to pull request if it will improve something.<3
import discord
from discord.ext import commands
from dislash import *
import dislash

from bot import guilds
from zoidbergbot.paginate import Element
from zoidbergbot.utils import option_menu


class Listeners(commands.Cog):
    """
        Centralized location for all listeners.
        Prevents making a million listeners in each cog which might have performance and readability issues.
    """
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, inter, error):
        if isinstance(error, slash_commands.MissingPermissions):
            await inter.reply("You do not have permissions to run that command!")
        raise error

        
def setup(bot):
    bot.add_cog(Listeners(bot))
