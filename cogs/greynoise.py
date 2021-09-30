from discord.ext import commands
from discord.ext.commands.errors import ConversionError
from dislash import SlashInteraction, slash_commands, Type, Option, application_commands
from greynoise import GreyNoise
from zoidbergbot.config import GREYNOISE_API_KEY

from bot import bot, guilds
from cogs.data import NLP
from zoidbergbot.database import bookmark_db


class Greynoise(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.api_client = GreyNoise(api_key=GREYNOISE_API_KEY, timeout=60, use_cache=True, cache_max_size=1000, cache_ttl=3600, integration_name="Zoidberg")
        
    @slash_command(name="scan-ip", testing_guilds=guilds,
                   description='Scans an IP using greynoise.io')
    def scan_ip(self, ctx, ip):
        quick = self.api_client.quick(ip)[1]

        if quick["code"] == "404":
            return None
        if quick[""]
        
        


def setup(bot):
    bot.add_cog(Greynoise(bot))
