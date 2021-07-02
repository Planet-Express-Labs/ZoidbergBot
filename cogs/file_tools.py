from discord.ext import commands
from dislash import SlashInteraction, slash_commands, Type, Option

from bot import guilds
from cogs.data import NLP


class FileTools(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @

    @commands.command(name="summarize")
    @slash_commands.command(name="expand_text",
                            description="Uses the GPT2 model to write text from a shorter piece of text.",
                            testing_guilds=guilds,
                            options=[
                                Option('input', 'The text you want to feed into the NLP. ', Type.STRING, required=True)
                            ]
                            )
    async def expand_text(self, ctx):
        await ctx.reply(type=5)
        text = ctx.get('input')
        nlp = NLP.BartCnn()
        out = str(await nlp.summarize(text))
        # , min_length, max_length, repetition_penalty=repetition_penalty, temperature=temperature
        await ctx.edit(out)


def setup(bot):
    bot.add_cog(FileTools(bot))
