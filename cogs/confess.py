# 8888888888P         d8b      888 888                                    888               888
#       d88P          Y8P      888 888                                    888               888
#      d88P                    888 888                                    888               888
#     d88P    .d88b.  888  .d88888 88888b.   .d88b.  888d888 .d88b.       88888b.   .d88b.  888888
#    d88P    d88""88b 888 d88" 888 888 "88b d8P  Y8b 888P"  d88P"88b      888 "88b d88""88b 888
#   d88P     888  888 888 888  888 888  888 88888888 888    888  888      888  888 888  888 888
#  d88P      Y88..88P 888 Y88b 888 888 d88P Y8b.     888    Y88b 888      888 d88P Y88..88P Y88b.
# d8888888888 "Y88P"  888  "Y88888 88888P"   "Y8888  888     "Y88888      88888P"   "Y88P"   "Y888
# This software is provided free of charge without a warranty.   888
# This Source Code Form is subject to the terms of the      Y8b d88P
# Mozilla Public License, v. 2.0. If a copy of the MPL was   "Y88P"
# this file, You can obtain one at https://mozilla.org/MPL/2.0/.

# This is designed to be used with Zoidberg bot, however I'm sure it could be adapted to work with your own projects.
# If there is an issue that might cause issue on your own bot, feel free to pull request if it will improve something.<3
import re
from datetime import datetime
from io import BytesIO

from discord.ext import commands
from dislash import *
import discord
from dislash import *
import asyncio

from zoidbergbot.database.confess_channel import *
from zoidbergbot.localization import get_string
from bot import guilds, bot

__version__ = '0.1 PRERELEASE'


async def server_picker(ctx):
    author = ctx.author
    servers = []
    i = 0
    guilds = author.mutual_guilds

    # for each in guilds:
    #     i += 1
    #     logging = get_db_int("logging_channel", each) != 0
    #     servers += f"{i}: {bot.get_guild(each)}\n```logging: {logging}\n```"
    if isinstance(ctx.channel, discord.TextChannel):
        await ctx.send("This command is intended to be used within a DM with the bot.")
    server_names = ""
    # channels = ConfessChannel
    for each in guilds:
        serv = await ConfessChannel.filter(guild=each.id)
        if len(serv) != 0:
            servers.append(serv[0])

    if len(servers) == 0:
        await ctx.reply("It doesn't appear that we share any servers with confess enabled!"
                        "Tell the admins of your server to run the comamand /setup-confess.\n\n"
                        "If you believe this to be an error, let us know in the support server (/server).")
        returnw
    for each in servers:
        server_names += f"{1}: {bot.get_guild(each.guild)}\n"

    embed = discord.Embed(title="Which server do you want me to send this message in? ",
                          description="Please send the number of the server you want to choose: \n" + server_names
                          )
    # message = await ctx.send(embed=embed)
    channel = ctx.channel
    await ctx.reply(embed=embed)

    def wait(msg):
        if msg.channel.id == channel.id and msg.author.id == author.id:
            return msg.content

    message = await bot.wait_for('Waiting for response...', check=check)
    print(message)
    try:
        server = servers[message]
    except IndexError:
        await ctx.reply("That is an invalid server!")
    # await message.delete()
    return server


async def log_confess(ctx, channel, message_object, timestamp):
    embed = discord.Embed(title="Confess event", timestamp=timestamp, description=message_object)
    author = ctx.message.author
    ava_url = author.avatar_urlz    
    embed.set_author(name=author, icon_url=ava_url, url=create_message_link(message_object))
    await channel.send(embed=embed)


def create_message_link(guild=None, channel=None, message=None):
    if guild is None:
        guild = message.guild.id
    if channel is None:
        channel = message.channel.id
    message_id = message.id()
    return f"https://discord.com/channels/{guild}/{channel}/{message_id}"


def find_url(url):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
            r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])) "
    return re.search(url, regex)


async def handle_image_embed(ctx, embed, message):
    files = []
    for file in ctx.message.attachments:
        fp = BytesIO()
        await file.save(fp)
        files.append(discord.File(fp, filename=file.filename, spoiler=file.is_spoiler()))
        image_url = ctx.message.attachments[0].url
        embed.set_image(url=image_url)
        print("image" + image_url)
    image = str(find_url(message))
    if image is not None:
        embed.set_image(url=image)
    return embed


class Confess(commands.Cog):
    """Cog for confessing. As the name makes clear. """

    # noinspection PyShadowingNames
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="server_pick_test", testing_guilds=guilds, description='if you see this, run.')
    async def cmd_server_pick_test(self, ctx):
        resp = await server_picker(ctx)
        await ctx.reply(resp.name)

    @slash_commands.has_permissions(administrator=True)
    @slash_command(name="setup_confess", testing_guilds=guilds,
                   description='Allows you to configure options for confess.')
    async def cmd_confess_setup(self, ctx):
        await ctx.reply(type=5)

        server = await ConfessChannel.filter(guild=ctx.guild.id).first()

        if server is None:
            server = await ConfessChannel(guild=ctx.guild.id)
            await server.save()

        async def setup_buttons():
            if server.enable:
                enable = ButtonStyle.green
                text = "Enable confess"
            else:
                enable = ButtonStyle.red
                text = "Enable SafeImage"
            if server.confess_channel == 0:
                confess_channel_enable = ButtonStyle.danger
                confess_channel_text = "Set confess channel"
            else:
                confess_channel_enable = ButtonStyle.green
                confess_channel_text = "Confess channel set"

            buttons = ActionRow(
                Button(
                    style=enable,
                    label=text,
                    custom_id="EN"
                ),
                Button(
                    style=confess_channel_enable,
                    label=confess_channel_text,
                    custom_id="CC")
            )
            return await ctx.edit("These are the options for confessions. Confessions are made in DMs using the /conf "
                                  "command.", components=[buttons])

        msg = await setup_buttons()
        on_click = msg.create_click_listener(timeout=60)

        @on_click.matching_id("EN")
        async def on_test_button(ctx):
            server.enable = not server.enable
            await server.save()
            await setup_buttons()
            await ctx.reply(type=6)

        @on_click.matching_id("CC")
        async def on_test_button(inter):
            def check(m):
                return m.content
            if server.confess_channel != '':
                await ctx.send(f"Here's your current setting: {server.confess_channel}")
            await ctx.send("Waiting for a single channel id...")
            await inter.reply(type=5)
            try:
                resp = await self.bot.wait_for('message', check=check)
            except asyncio.TimeoutError:
                await ctx.reply("Timeout reached. Try again. ")
            resp = re.sub("[<># ]", '', resp.content)
            try:
                channel = await self.bot.fetch_channel(resp)
            except discord.errors.HTTPException:
                return await inter.reply(f"Entry invalid: {resp}\ntry again")
            if channel is None:
                return await inter.reply("Entry invalid: " + resp)
            server.confess_channel = resp
            await server.save()
            await setup_buttons()
            await inter.edit("Your channels have been recorded.")

    @slash_command(name="conf", testing_guilds=guilds, description='Sends a message anonymously to a channel.',
                   options=[
                       Option('message', 'The message you want to confess', Type.STRING, required=True)
                   ])
    async def cmd_confess(self, ctx):
        print("123")
        message = ctx.get('message')
        confchannel = await ConfessChannel.filter(guild=ctx.guild.id).first()
        print(123)
        guild = confchannel.guild
        current_time = datetime.now().strftime("%d/%m %H:%M")
        # user_id = ctx.author.id
        # await ctx.reply(type=5)
        server = await server_picker(ctx)
        # channel = await bot.get_channel(server)
        print('spp', server)
        # Create embed. They're fancy
        embed = discord.Embed(description=f"{message}", timestamp=current_time)
        embed = handle_image_embed(ctx, embed, message)
        msg = await channel.send(embed=embed)
        await log_confess(ctx, bot.get_channel(int(confchannel.log_channel)), message, current_time)
        embed = discord.Embed(description=get_string("message_sent"), url=create_message_link(guild, channel, msg))
        embed.set_author(name=f"Zoidberg confess v{0}".format(__version__),
                         icon_url="https://i.imgur.com/wWa4zCM.png",
                         url="https://github.com/LiemEldert/ZoidbergBot")
        await ctx.reply(embed=embed)

    @cmd_confess.error
    async def conf_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Please wait before sending ')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have manage_messages permission')


def setup(bot):
    bot.add_cog(Confess(bot))
