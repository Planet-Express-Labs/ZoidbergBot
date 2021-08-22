from discord.ext import commands
from discord.ext.commands.errors import ConversionError
from dislash import SlashInteraction, slash_commands, Type, Option, application_commands

from bot import bot, guilds
from cogs.data import NLP
from zoidbergbot.database import bookmark_db


class Bookmarks(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="bookmark", brief="Save a short message or link.", testing_guilds=guilds, options=[
                            Option('message', 'Content you want to save.', Type.STRING, required=True),
                            Option('collection', 'Categorize your bookmarks.', Type.STRING),
                            Option('tags', 'Label your bookmarks using tags.')
                            ])
    async def cmd_bookmark(self, ctx):
        message = ctx.get('message')
        collection = ctx.get('collection')
        tags = ctx.get('tags')
        if collection is None:
            collection = 'uncategorized'
        if tags is None:
            tags = 'untagged'
        bookmark = await bookmark_db.create(user_id=ctx.author.id, content=message, collection=collection)
        bookmark.save()
        await ctx.reply(type=1)

    # @slash_command(name="bookmarks", brief="Returns a list of all saved bookmarks.", testing_guilds=guilds, options=[
    #                         Option('collection', 'Filter by a specific collection name', Type.STRING)
    #                         ])
    # async def bookmarks(self, ctx):

    @application_commands.message_command(name="Resend", testing_guilds=guilds)
    async def ctx_quick_bookmark(self, inter):
        # Message commands are visible in message context menus
        # inter is instance of ContextMenuInteraction
        await inter.respond(inter.message.content)
        


def setup(bot):
    bot.add_cog(Bookmarks(bot))
