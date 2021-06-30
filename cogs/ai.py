import re
from discord.ext import commands
from discord.ext.commands.errors import ConversionError
from dislash import SlashInteraction, ActionRow, Button, slash_commands, Element, Type, Option

from bot import guilds
from data.gifs import *
from zoidbergbot.localization import get_string
from zoidbergbot.verify import verify_user
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
                                Option('temperature', 'The temperature of the sampling operation. Higher is closer to uniform probablility.', Type.STRING),
                                Option('repetition_penalty', 'The higher the value, the higher the penalty is for repeated token.', Type.STRING)
                            ]
                            )
    async def cmd_summarize(self, ctx: SlashInteraction):
        # convert the values into floats since discord does not seem to support them. 
        try:
            repetition_penalty = float(ctx.get("repetition_penalty"))
            temperature = float(ctx.get("temperature"))
        except ConversionError:
            ctx.create_response("The repetition_penalty and temperature must be floats. ")

        # Cut the values down if they are too large.
        repetition_penalty = trim(repetition_penalty, 100, 0)
        temperature = trim(temperature, 100, 0)

        text = ctx.get('input')
        min_length = ctx.get('min_length')
        max_length = ctx.get('max_length')
        out = str(NLP.summarize(text, min_length, max_length, repetition_penalty=repetition_penalty, temperature=temperature))
        ctx.create_response(out)


def setup(bot):
    bot.add_cog(Ai(bot))
