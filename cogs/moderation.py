from bot import bot
import discord
from discord.ext import commands
from discord.ext.commands import Context
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

    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def cmd_purge(self, ctx, messages=0, channel=None):
        if channel is None:
            channel = ctx.channel
        await channel.purge(limit=messages)

    @commands.command(name="avatar")
    async def cmd_avatar(self, ctx, *, user: discord.Member = None):
        embed = discord.Embed(description=f"{user.display_name}'s profile picture:")
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(get_string("COMMAND_EMPTY"))


def setup(bot):
    bot.add_cog(Moderation(bot))
