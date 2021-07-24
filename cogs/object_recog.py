from google.cloud import vision
import io
import base64

import discord
from discord.ext import commands
from dislash import *
import re

from bot import guilds, bot


# def detect_safe_search(file):
#     """Detects unsafe features in the file."""
#     bytes_io = io.BytesIO()
#     file.save(bytes_io)
#     byte = bytes_io.read()
#
#     client = vision.ImageAnnotatorClient()
#
#     b64 = base64.b64encode(byte)
#     image = vision.Image(content=b64)
#
#     response = client.safe_search_detection(image=image)
#     safe = response.safe_search_annotation
#
#     # Names of likelihood from google.cloud.vision.enums
#     likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
#                        'LIKELY', 'VERY_LIKELY')
#     # print('Safe search:')
#
#     print('adult: {}'.format(likelihood_name[safe.adult]))
#     print('medical: {}'.format(likelihood_name[safe.medical]))
#     print('spoofed: {}'.format(likelihood_name[safe.spoof]))
#     print('violence: {}'.format(likelihood_name[safe.violence]))
#     print('racy: {}'.format(likelihood_name[safe.racy]))
#     return likelihood_name, safe


def detect_safe_search_uri(uri):
    """Detects unsafe features in the file located in Google Cloud Storage or
    on the Web."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    # print('Safe search:')
    #
    # print('adult: {}'.format(likelihood_name[safe.adult]))
    # print('medical: {}'.format(likelihood_name[safe.medical]))
    # print('spoofed: {}'.format(likelihood_name[safe.spoof]))
    # print('violence: {}'.format(likelihood_name[safe.violence]))
    # print('racy: {}'.format(likelihood_name[safe.racy]))
    return likelihood_name, safe


def find_url(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
            r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])) "
    url = re.findall(regex, string)
    return [x[0] for x in url]


class SafeImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_commands.command(name="scan-image",
                            guild_ids=guilds,
                            description="Scans an image for NSFW content. ",
                            options=[
                                Option("image", "The link to the image to scan. ",
                                       type=Type.STRING, required=True)
                            ])
    async def cmd_scan_image(self, ctx):
        uri = ctx.get("image")
        print(uri)
        #if find_url(uri) == 1:
        await ctx.reply(type=5)
        resp, safe = detect_safe_search_uri(uri)
        embed = discord.Embed(title="Image scan results:", description=f'adult: {safe.adult}\n'
                                                                       f'medical: {safe.medical}\n'
                                                                       f'spoofed: {safe.spoof}\n'
                                                                       f'violence: {safe.violence}\n'
                                                                       f'racy: {safe.racy}\n')
        await ctx.edit(embed=embed)
        #else:
            #await ctx.reply("This must be in the format of a URI/URL!")


def setup(bot):
    bot.add_cog(SafeImage(bot))
