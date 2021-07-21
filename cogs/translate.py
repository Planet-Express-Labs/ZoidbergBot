import json

import discord
from discord.ext import commands
from dislash import *
import pycountry
import os
import six
from google.cloud import translate_v2 as translate

from bot import guilds


if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') is None:
    if os.path.exists(os.getcwd() + "\\data\\config.ini"):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "gcloud.json"
    else:
        dict = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON_RAW'))
        with open('crownbot.json', 'w+') as file:
            json.dump(dict, file)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "crownbot.json"


def translate_text_target(text, target):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    return result
    # print(u"Text: {}".format(result["input"]))
    # print(u"Translation: {}".format(result["translatedText"]))
    # print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))


class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_commands.command(name="translate",
                            guild_ids=guilds,
                            description="Translates text to a target language.",
                            options=[
                                Option("text", "The text that you want to translate.",
                                       type=Type.STRING, required=True),
                                Option("language", "The language that you want to translate to.",
                                       type=Type.STRING)
                            ])
    async def translate_to(self, ctx):
        """Translates text to a target language."""
        text = ctx.get("text")
        target = ctx.get("language")
        langs = pycountry.languages

        if target is None:
            target = "english"
        language = langs.lookup(target).alpha_2
        if language is None:
            await ctx.reply("Invalid language.")
            return

        print(language)
        await ctx.reply(type=5)
        translated = translate_text_target(text, language)
        text = translated['translatedText']
        source = translated['detectedSourceLanguage']
        embed = discord.Embed(title=f"Translated from {source} to {target}",
                              description=text,
                              footer="Engine: Google Cloud Translate API"
                              )
        await ctx.edit(embed=embed)

def setup(bot):
    bot.add_cog(Translate(bot))
