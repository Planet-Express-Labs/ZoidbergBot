# This is designed to be used with Zoidberg bot, however I'm sure it could be adapted to work with your own projects.
# If there is an issue that might cause issue on your own bot, feel free to pull request if it will improve something.<3
import discord
from discord.ext import commands
from dislash import *

from bot import guilds
from zoidbergbot.paginate import Element


class Listeners(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, inter, error):
        if isinstance(error, slash_commands.MissingPermissions):
            await inter.reply("You do not have permissions to run that command!")
        raise error

def setup(bot):
    bot.add_cog(Listeners(bot))
