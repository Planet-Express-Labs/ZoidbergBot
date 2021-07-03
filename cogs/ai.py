from discord.ext import commands
from discord.ext.commands.errors import ConversionError
from dislash import SlashInteraction, slash_commands, Type, Option

from bot import guilds
from cogs.data import NLP


def trim(input, max, min):
    if input > max:
        input = max
    elif input < min:
        input = min
    return input


class Ai(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @slash_commands.command(name='summarize',
                            description='Summarizes input text into something shorter using Facebook BartCNN',
                            testing_guilds=guilds,
                            options=[
                                Option('input', 'The text you want to be summarized.', Type.STRING, required=True),
                                Option('min_length', 'The minimum length of the summary', Type.INTEGER),
                                Option('max_length', 'The maximum length of the summary', Type.INTEGER),
                                Option('temperature', 'The temperature of the sampling operation. Higher is closer to '
                                                      'uniform probablility.', Type.STRING),
                                Option('repetition_penalty', 'The higher the value, the higher the penalty is for '
                                                             'repeated token.', Type.STRING)
                            ]
                            )
    async def cmd_summarize(self, ctx: SlashInteraction):

        repetition_penalty = ctx.get("repetition_penalty")
        temperature = ctx.get("temperature")
        if temperature is not None:
            # convert the values into floats since discord does not seem to support them.
            try:
                temperature = float(repetition_penalty)
            except ConversionError:
                await ctx.reply("The repetition_penalty and temperature must be floats. ")
            # Cut the values down if they are too large.
            temperature = trim(temperature, 100, 0)
        else:
            temperature = 1.0
        if repetition_penalty is not None:
            try:
                repetition_penalty = float(repetition_penalty)
            except ConversionError:
                await ctx.create_response("The repetition_penalty and temperature must be floats. ")
            repetition_penalty = trim(repetition_penalty, 100, 0)
        await ctx.reply(type=5)
        nlp = NLP.BartCnn()
        text = ctx.get('input')
        min_length = ctx.get('min_length')
        max_length = ctx.get('max_length')

        print(str(text), min_length, max_length, temperature, repetition_penalty)
        out = str(await nlp.summarize(text))
        #   , min_length, max_length, repetition_penalty=repetition_penalty, temperature=temperature
        await ctx.edit(out)
    
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
        gpt = NLP.Gpt2()
        out = str(await gpt.expand_text(text))
        await ctx.edit(out)


def setup(bot):
    bot.add_cog(Ai(bot))
