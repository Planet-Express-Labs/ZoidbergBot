"""
WaveLink Playlist Example.
Please understand Music bots are complex, and that even this basic example can be daunting to a beginner.
For this reason it's highly advised you familiarize yourself with discord.py, python and asyncio, BEFORE
you attempt to write a music bot.
This example makes use of: Python 3.7, WaveLink(https://github.com/EvieePy/Wavelink) and LavaLink.
This is a very basic playlist example, which allows per guild playback of unique queues.
The commands implement very basic logic for basic usage. But allow for expansion. It would be advisable to implement
your own permissions and usage logic for commands.
e.g You might like to implement a vote before skipping the song or only allow admins to cmd_stop the player.
Music bots require lots of work, and tuning. Goodluck.
If you find any bugs feel free to ping me on discord. @Eviee#0666
"""
import asyncio
import datetime
import itertools
import re
import sys
import traceback
from typing import Union

import discord
from humanize import naturalsize
import wavelink
from discord.ext import commands
from dislash import slash_commands, Option, Type, Interaction

from bot import guilds
from cogs.data.music_nodes import nodes

RURL = re.compile('https?:\/\/(?:www\.)?.+')
loop = False


class Bot(commands.Bot):

    def __init__(self):
        super(Bot, self).__init__(command_prefix=['audio ', 'wave ', 'aw ', 'link '])

        self.add_cog(Music(self))

    async def on_ready(self):
        print(f'Logged in as {self.user.name} | {self.user.id}')


class MusicController:

    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.channel = None

        self.next = asyncio.Event()
        self.queue = asyncio.Queue()

        self.volume = 40
        self.now_playing = None

        self.bot.loop.create_task(self.controller_loop())

    async def controller_loop(self):
        await self.bot.wait_until_ready()

        player = self.bot.wavelink.get_player(self.guild_id)
        await player.set_volume(self.volume)

        while True:
            if self.now_playing:
                await self.now_playing.delete()

            self.next.clear()

            song = await self.queue.get()
            await player.play(song)
            self.now_playing = await self.channel.send(f'Now playing: `{song}`')

            await self.next.wait()


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.controllers = {}

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        for n in nodes.values():
            node = await self.bot.wavelink.initiate_node(**n)
            node.set_hook(self.on_event_hook)
            print(f"Node connected: {node.identifier} at {node.region}")

    async def on_event_hook(self, event):
        """Node hook callback."""
        if isinstance(event, (wavelink.TrackEnd, wavelink.TrackException)):
            controller = self.get_controller(event.player)
            controller.next.set()

    def get_controller(self, value: Union[commands.Context, wavelink.Player]):
        if isinstance(value, Interaction):
            gid = value.guild.id
        else:
            gid = value.guild_id

        try:
            controller = self.controllers[gid]
        except KeyError:
            controller = MusicController(self.bot, gid)
            self.controllers[gid] = controller

        return controller

    async def cog_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def cog_command_error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    # @wavelink.WavelinkMixin.listener()
    # async def on_track_end(self, payload):
    #     player = payload.player()
    #     print(controller.cmd_queue._queue)
    #
    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        raise error

    @slash_commands.command(name='connect',
                            guild_ids=guilds,
                            description="Connect the bot to a voice channel.",
                            options=[
                                Option('channel', 'The channel you want the bot to join.', type=Type.CHANNEL)
                            ])
    async def cmd_connect_(self, ctx):
        """Connect the bot to a voice channel. """
        channel = ctx.get('channel')
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f'Connecting to **`{channel.name}`**')
        await player.connect(channel.id)

        controller = self.get_controller(ctx)
        controller.channel = ctx.channel

    # @commands.command(name="play")
    @slash_commands.command(name='play',
                            guild_ids=guilds,
                            description="Search for and adds a song to the queue.",
                            options=[
                                Option('song', 'The song you want to play', type=Type.STRING, required=True)
                            ])
    async def cmd_play(self, ctx):
        query = ctx.get('song')
        if not RURL.match(query):
            query = f'ytsearch:{query}'

        try:
            tracks = await self.bot.wavelink.get_tracks(f'{query}')
        except wavelink.errors.ZeroConnectedNodes:
            return await ctx.reply("Unknown node error occurred, are the nodes online? ")

        if not tracks:
            # TODO: convert to a localization string.
            return await ctx.reply('Could not find any songs with that query.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await self.cmd_connect_(ctx)

        track = tracks[0]

        controller = self.get_controller(ctx)
        await controller.queue.put(track)
        # TODO: convert to a localization string.
        await ctx.reply(f'Added {str(track)} to the queue.')

    @slash_commands.command(name='pause',
                            guild_ids=guilds,
                            description="Pauses the song."
                            )
    async def cmd_pause(self, ctx):
        """Pauses the song."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('I am not currently playing anything!')

        await ctx.send('Pausing the song!')
        await player.set_pause(True)

    @slash_commands.command(name="resume",
                            guild_ids=guilds,
                            description="Resumes the song if it is paused."
                            )
    async def cmd_resume(self, ctx):
        """Resumes the song if pauced. ."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.paused:
            return await ctx.send('The song is not currently paused!')

        await ctx.send('Resumed. ')
        await player.set_pause(False)

    @slash_commands.command(name='skip',
                            guild_ids=guilds,
                            description="Skips the currently playing song. "
                            )
    async def cmd_skip(self, ctx):
        """Skip the currently playing song."""
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send("There isn't anything playing!")

        await ctx.send('Skipping...')
        await player.stop()

    @slash_commands.command(name='volume',
                            aliases=['vol'],
                            guild_ids=guilds,
                            description="Sets the volume. Leave it empty to adjust it using the buttons.",
                            options=[
                                Option('volume', 'What volume you want to set the bot to 0-100', type=Type.INTEGER)
                            ]
                            )
    async def cmd_volume(self, ctx):
        """Set the player volume."""
        vol = ctx.get('volume')
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if vol is not None:
            vol = max(min(vol, 1000), 0)
            controller.volume = vol
            await ctx.send(f'Setting the cmd_volume to `{vol}`')
            await player.set_volume(vol)

    @slash_commands.command(name='now_playing',
                            aliases=['np', 'current', 'nowplaying'],
                            guild_ids=guilds,
                            description="Sends the currently playing song, if present. "
                            )
    async def cmd_now_playing(self, ctx):
        """Retrieve the currently playing song."""
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.current:
            return await ctx.send('I am not currently playing anything!')

        controller = self.get_controller(ctx)
        await controller.now_playing.delete()

        controller.now_playing = await ctx.send(f'Now playing: `{player.current}`')

    @slash_commands.command(name="queue",
                            aliases=['q'],
                            guild_ids=guilds,
                            description="Lists the songs in the queue."
                            )
    async def cmd_queue(self, ctx):
        """Retrieve information on the next 5 songs from the queue."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        if not player.current or not controller.queue._queue:
            return await ctx.send('There are no songs currently in the queue.', delete_after=20)

        upcoming = list(itertools.islice(controller.queue._queue, 0, 5))

        fmt = '\n'.join(f'**`{str(song)}`**' for song in upcoming)
        embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt)

        await ctx.send(embed=embed)

    @slash_commands.command(name='stop',
                            aliases=['disconnect', 'dc'],
                            guild_ids=guilds,
                            description="Stops and disconnects the bot."
                            )
    async def cmd_stop(self, ctx):
        """Stop and disconnect the player and controller."""
        player = self.bot.wavelink.get_player(ctx.guild.id)

        try:
            del self.controllers[ctx.guild.id]
        except KeyError:
            await player.disconnect()
            return await ctx.send('There was no controller to cmd_stop.')

        await player.disconnect()
        await ctx.send('Disconnected player and killed controller.', delete_after=20)

    @slash_commands.command(name='nodes',
                            guild_ids=guilds,
                            description="Lists information about the currently connected nodes. "
                            )
    async def cmd_nodes(self, ctx):
        """Retrieve various Node/Server/Player information."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        node = player.node

        used = naturalsize(node.stats.memory_used)
        total = naturalsize(node.stats.memory_allocated)
        free = naturalsize(node.stats.memory_free)
        cpu = node.stats.cpu_cores

        fmt = f'Running: **WaveLink:** `{wavelink.__version__}`\n\n' \
              f'Connected to `{len(self.bot.wavelink.nodes)}` nodes.\n' \
              f'Best available Node `{self.bot.wavelink.get_best_node().__repr__()}`\n' \
              f'`{len(self.bot.wavelink.players)}` players are distributed on nodes.\n' \
              f'`{node.stats.players}` players are distributed on server.\n' \
              f'`{node.stats.playing_players}` players are playing on server.\n\n' \
              f'Server Memory: `{used}/{total}` | `({free} free)`\n' \
              f'Server CPU: `{cpu}`\n\n' \
              f'Server Uptime: `{datetime.timedelta(milliseconds=node.stats.uptime)}`'
        await ctx.send(fmt)


def setup(bot):
    bot.add_cog(Music(bot))
