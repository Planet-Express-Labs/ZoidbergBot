import discord
from dislash import *
from discord.ext import commands

from tortoise import *

max_id = 0

class OptionMenu(commands.Cog):
    def __init__(self, tortoise_object, inter):
        self.fields = []
        self.author = inter.author
        self.channel - inter.channel
        self.inter = inter

        self.server = tortoise_object
        
        global max_id

    def add_field(self, name: str, prompt_text: str, field_type: str):
        """
        Adds a field into your OptionMenu object. Field type must be of the following strings:
            - channel, waits for user to tag a channel and saves it into your database.
        """
        field = {"id": max_id,"name": name, "prompt": prompt_text, "type": field_type}
        self.fields.append(field)

    async def create_listener(self):
        """
        Creates the menu listener using the fields defined in add_field. Returns nothing
        """
    

    @dislash.listener()
    async def on_button_press(self, inter):
        if self.author == self.author and inter.channel == self.channel:
            for each in self.fields:
                if inter.id == each["id"]:
                    if each["type"] == "channel":
                        await self.server.add_channel(inter.channel)
                        await self.inter.send(f"Added channel {inter.channel.name} to the database.")
                        return
                    else:
                        await self.inter.send("Invalid field type.")
                        return

    @slash.command()
    async def _channel_option(self, inter, entry):
        
                

def setup(bot):
    bot.add_cog(OptionMenu(bot))
        
