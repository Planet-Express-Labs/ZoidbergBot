import discord
from discord.ext import commands
from discord.ext.commands import Context
from dislash import slash_commands, Option, Type, interactions

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


def setup(bot):
    bot.add_cog(Moderation(bot))
