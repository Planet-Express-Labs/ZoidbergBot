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
from dislash import *

from bot import guilds
from zoidbergbot import localization


async def avatar(ctx, user):
    embed = discord.Embed(description=f"{user.display_name}'s profile picture:")
    embed.set_image(url=user.avatar_url)
    await ctx.reply(embed=embed)


async def user_info(ctx, user):
    badges = {
        "staff": "<:staff:812692120049156127>",
        "partner": "<:partner:812692120414322688>",
        "hypesquad": "<:hypesquad_events:812692120358879262>",
        "bug_hunter": "<:bug_hunter:812692120313266176>",
        "hypesquad_bravery": "<:bravery:812692120015339541>",
        "hypesquad_brilliance": "<:brilliance:812692120326373426>",
        "hypesquad_balance": "<:balance:812692120270798878>",
        "verified_bot_developer": "<:verified_bot_developer:812692120133042178>"
    }

    badge_string = ' '.join(badges[pf.name] for pf in user.public_flags.all() if pf.name in badges)
    created_at = str(user.created_at)[:-7]
    reply = discord.Embed(color=discord.Color.blurple())
    reply.title = str(user)
    reply.set_thumbnail(url=user.avatar_url)
    reply.add_field(
        name="Registration",
        value=(
            f"⌚ **Created at:** `{created_at}`\n"
            f"📋 **ID:** `{user.id}`"
        ),
        inline=False
    )
    if len(badge_string) > 1:
        reply.add_field(
            name="Badges",
            value=f"`->` {badge_string}"
        )
    await ctx.send(embed=reply)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_commands.has_permissions(manage_messages=True)
    @slash_command(name="embed",
        description="Creates an embed",
        options=[
            Option("channel", "Where the message should be sent.", Type.CHANNEL),
            Option("title", "Creates a title", Type.STRING),
            Option("description", "Creates a description", Type.STRING),
            Option("color", "Colors the embed", Type.STRING),
            Option("image_url", "URL of the embed's image", Type.STRING),
            Option("footer", "Creates a footer", Type.STRING),
            Option("footer_url", "URL of the footer image", Type.STRING)
        ],
        guild_ids=guilds)
    async def cmd_embed(self, ctx: Interaction,
                        channel: discord.TextChannel,
                        title: str = None,
                        description: str = None,
                        color: str = None,
                        image_url: str = None,
                        footer: str = None,
                        footer_url: str = None):
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
        if description is not None:
            reply.description = description
        if image_url is not None:
            reply.set_image(url=image_url)
        pl = {}
        if footer is not None:
            pl['text'] = footer
        if footer_url is not None:
            pl['icon_url'] = footer_url
        if len(pl) > 0:
            reply.set_footer(**pl)
        if channel is None:
            await ctx.send(embed=reply)
        else:
            await ctx.reply("Sent!")
            await channel.send(embed=reply)

    @slash_commands.has_permissions(manage_messages=True)
    @slash_command(name="purge",
                            description="Deletes many messages at once. Syntax: /purge <messages> <channel>. ",
                            guild_ids=guilds,
                            options=[
                                Option('messages', 'The number of messages to delete.', Type.INTEGER, required=True),
                                Option("user", "The user who's messages you want to delete.", Type.USER),
                                Option('channel', 'The channel to delete the messages in.', Type.CHANNEL)]
                            )
    async def cmd_purge(self, ctx):
        """Deletes Multiple messages from a channel.
        The syntax is as follows:
        purge <messages> <channel>.
        If the channel is none, it will use the current channel.
        """
        msg = []
        channel = ctx.get('channel')
        limit = ctx.get('messages')
        member = ctx.get('user')
        await ctx.reply(type=5)
        if not member:
            await ctx.channel.purge(limit=limit)
            return await ctx.send(f"Purged {limit} messages", delete_after=3)
        async for m in ctx.channel.history():
            if len(msg) == limit:
                break
            if m.author == member:
                msg.append(m)
        await ctx.channel.delete_messages(msg)
        await ctx.reply(f"Deleted {limit} messages. ", delete_after=5)

    @slash_command(name="avatar",
                            description="Gets the avatar from the pinged user.",
                            guild_ids=guilds,
                            options=[
                                Option('user', "Who's avatar you want to pull.", Type.USER)
                            ])
    async def cmd_avatar(self, ctx):
        user = ctx.get('user', ctx.author)
        await avatar(ctx, user)

    @application_commands.user_command(name="Show user avatar",
                                       description="Sends an embed comtaining a direct link to a user's avatar",
                                       testing_guilds=guilds)
    async def ctx_avatar(self, inter):
        await avatar(inter, inter.target)

    # User info
    @slash_command(
        name="user-info",
        description="Shows user profile",
        options=[Option("user", "Which user to inspect", Type.USER)],
        guild_ids=guilds)
    async def cmd_user_info(self, ctx):
        user = ctx.get("user", ctx.author)
        await user_info(ctx, user)

    @application_commands.user_command(name="Show user info", description="Shows user profile", testing_guilds=guilds)
    async def ctx_user_info(self, inter):
        await user_info(inter, inter.target)


def setup(bot):
    bot.add_cog(Moderation(bot))
