import base64
import random

import aiohttp
import art
# This is designed to be used with Zoidberg bot, however I'm sure it could be adapted to work with your own projects.
# If there is an issue that might cause issue on your own bot, feel free to pull request if it will improve something.<3
import discord
from discord.ext import commands
from dislash import SlashInteraction, ActionRow, Button, slash_commands, Element

from bot import guilds
from data.gifs import *
from zoidbergbot.localization import get_string
from zoidbergbot.verify import verify_user


class Help(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    async def create_menu(ctx: SlashInteraction, menu):
        # Build buttons
        button_row_1 = ActionRow(
            Button(
                style=ButtonStyle.blurple,
                emoji="⬆",
                custom_id="up"
            ),
            Button(
                style=ButtonStyle.green,
                label="Select",
                custom_id="select"
            )
        )
        button_row_2 = ActionRow(
            Button(
                style=ButtonStyle.blurple,
                emoji="⬇",
                custom_id="down"
            ),
            Button(
                style=ButtonStyle.red,
                label="Back",
                custom_id="back"
            )
        )
        # Send a message with buttons
        emb = discord.Embed(
            title=menu.header,
            description=f"{menu.long_desc}\n\n{menu.display_elements()}"
        )
        msg = await ctx.send(embed=emb, components=[button_row_1, button_row_2])

        # Click manager usage
        
        on_click = msg.create_click_listener(timeout=60)
        
        @on_click.matching_id("down")
        async def down(inter):
            menu.next_elem()
        
        @on_click.matching_id("up")
        async def up(inter):
            menu.prev_elem()
        
        @on_click.matching_id("select")
        async def select(inter):
            nonlocal menu
            menu = menu.element
        
        @on_click.matching_id("back")
        async def back(inter):
            nonlocal menu
            menu = menu.parent
        
        @on_click.no_checks()
        async def response(inter):
            emb.title = menu.header
            emb.description = f"{menu.long_desc}\n\n{menu.display_elements()}"
            await inter.reply(embed=emb, type=ResponseType.UpdateMessage)

        @on_click.timeout
        async def on_timeout():
            for button in button_row_1.components:
                button.disabled = True
            for button in button_row_2.components:
                button.disabled = True
            await msg.edit(embed=emb, components=[button_row_1, button_row_2])

    @slash_commands.command(name='music-help',
                            description='Provides information on how to use the music commands. ', 
                            testing_guilds=guilds)
    async def cmd_music_help(self, ctx:SlashInteraction):
        menu = Element(
        header="Music commands",
        long_desc="Navigate through all the entries",
        elements=[
            Element(
                header="/connect <channel, current channel if None>",
                long_desc="Connects the bot to a channel and creates a player.\n"
                "This command is automatically executed if you are not in a channel."
            ),
            Element(
                header="/play <song>",
                long_desc="Starts playing a song in the currently connected channel.\n"
                "If you are not in a channel, it will automatically connect.\n\n"
                "This command supports playing from youtube, bandcamp, soundcloud, twitch, vimeo and direct http streams."
            ),
            Element(
                header="/pause",
                long_desc="Pauses playback. "
            ),
            Element(
                header="/resume",
                long_desc="Resumes playback. "
            ),
            Element(
                header="/skip",
                long_desc="Skips the currently playing song. "
            ),
            Element(
                header="/volume",
                long_desc="Sets the volume of the player. "
            ),
            Element(
                header="/now_playing",
                long_desc="Displays the currently playing song. "
            ),
            Element(
                header="/queue",
                long_desc="Displays the queue of the player. "
            ),
            Element(
                header="/stop",
                long_desc="Stops playback. "
            ),
            Element(
                header="/nodes",
                long_desc="Displays information about the connected nodes. "
            )
            ]
        )
        self.create_menu(ctx, menu)

def setup(bot):
    bot.add_cog(Help(bot))
