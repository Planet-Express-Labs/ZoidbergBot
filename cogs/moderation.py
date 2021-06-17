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
import discord
from discord.ext import commands
from discord.ext.commands import Context
from dislash import slash_commands, Option, Type, Interaction

from bot import guilds
from zoidbergbot import localization


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(localization.get_string("COMMAND_EMPTY"))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(localization.get_string("CMD_PERMISSION_ERROR"))

    @slash_commands.has_permissions(manage_messages=True)
    @slash_commands.command(
        name="embed",
        description="Creates an embed",
        options=[
            Option("title", "Creates a title", Type.STRING),
            Option("description", "Creates a description", Type.STRING),
            Option("color", "Colors the embed", Type.STRING),
            Option("image_url", "URL of the embed's image", Type.STRING),
            Option("footer", "Creates a footer", Type.STRING),
            Option("footer_url", "URL of the footer image", Type.STRING)

        ],
        guild_ids=guilds)
    async def cmd_embed(self, ctx: Interaction):
        title = ctx.get('title')
        desc = ctx.get('description')
        color = ctx.get('color')
        image_url = ctx.get('image_url')
        footer = ctx.get('footer')
        footer_url = ctx.get('footer_url')
        if color is not None:
            # try:
            color = await commands.ColorConverter().convert(ctx, color)
            # except:
            #     color = discord.Color.default()
        else:
            color = discord.Color.default()
        reply = discord.Embed(color=color)
        if title is not None:
            reply.title = title
        if desc is not None:
            reply.description = desc
        if image_url is not None:
            reply.set_image(url=image_url)
        pl = {}
        if footer is not None:
            pl['text'] = footer
        if footer_url is not None:
            pl['icon_url'] = footer_url
        if len(pl) > 0:
            reply.set_footer(**pl)
        await ctx.send(embed=reply)

    @slash_commands.has_permissions(manage_messages=True)
    @slash_commands.command(name="purge",
                            description="Deletes many messages at once. Syntax: /purge <messages> <channel>. ",
                            guild_ids=guilds,
                            options=[
                                Option('messages', 'The number of messages to delete.', Type.INTEGER, required=True),
                                Option('channel', 'The channel to delete the messages in.', Type.CHANNEL)]
                            )
    async def cmd_purge(self, interaction):
        """Deletes Multiple messages from a channel.
        The syntax is as follows:
        purge <messages> <channel>.
        If the channel is none, it will use the current channel.
        """
        messages = int(interaction.get("messages"))
        channel = interaction.get("channel")
        if channel is None:
            channel = interaction.channel
        await channel.purge(limit=messages)
        await interaction.reply(f"Deleted {messages} messages. ")

    @slash_commands.command(name="avatar",
                            description="Gets the avatar from the pinged user.",
                            guild_ids=guilds,
                            options=[
                                Option('user', "Who's avatar you want to pull.", Type.USER, required=True)
                            ])
    async def cmd_avatar(self, ctx):
        user = ctx.get('user')
        embed = discord.Embed(description=f"{user.display_name}'s profile picture:")
        embed.set_image(url=user.avatar_url)
        await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(localization.get_string("COMMAND_EMPTY"))
        if isinstance(error, slash_commands.MissingPermissions):
            await ctx.send(localization.get_string("NO_PERMISSION"))


def setup(bot):
    bot.add_cog(Moderation(bot))
