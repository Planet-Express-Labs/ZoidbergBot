from google.cloud import vision
import io
import base64

import discord
from discord.ext import commands
from dislash import *
import re

from cogs.api import ms_content_moderation
from zoidbergbot.database import filter_db
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


async def combine_results(google, azure, ctx):
    guild = ctx.guild.id
    server = await filter_db.FilterServer.filter(
        participants=guild[0].id
    ).prefetch_related('participants', 'tournament')
    if server > 1:
        await ctx.reply("An unexpected database error has occurred. Your settings have been reset. ")


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
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return urls


class SafeImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_commands.command(name="scan-image-ms",
                            guild_ids=guilds,
                            description="Scans an image for NSFW content using MS content filtering. ",
                            options=[
                                Option("image", "The link to the image to scan. ",
                                       type=Type.STRING, required=True)
                            ])
    async def cmd_scan_image_ms(self, ctx):
        uri = ctx.get("image")
        await ctx.reply(type=5)
        result = ms_content_moderation.image_moderation(uri)
        embed = discord.Embed(title="Image scan results:",
                              description=f'adult: {result["adult_classification_score"]}\n'
                                          f'medical: {result["racy_classification_score"]}\n')
        await ctx.reply(embed=embed)

    @slash_commands.command(name="scan-image-safesearch",
                            guild_ids=guilds,
                            description="Scans an image for NSFW content using Google SafeSearch. ",
                            options=[
                                Option("image", "The link to the image to scan. ",
                                       type=Type.STRING, required=True)
                            ])
    async def cmd_scan_image_safesearch(self, ctx):
        uri = ctx.get("image")
        print(uri)
        # if find_url(uri) == 1:
        await ctx.reply(type=5)
        resp, safe = detect_safe_search_uri(uri)
        embed = discord.Embed(title="Image scan results:", description=f'adult: {resp[safe.adult]}\n'
                                                                       f'medical: {resp[safe.medical]}\n'
                                                                       f'spoofed: {resp[safe.spoof]}\n'
                                                                       f'violence: {resp[safe.violence]}\n'
                                                                       f'racy: {resp[safe.racy]}')
        await ctx.edit(embed=embed)
        # else:
        # await ctx.reply("This must be in the format of a URI/URL!")

    @slash_commands.has_permissions(administrator=True)
    @slash_commands.command(name="safeguard-ai",
                            guild_ids=guilds,
                            description="Sets up AI based text and image filtering using AI. ",
                            # options=[
                            #     Option("setup-code", "A premade setup code to be transfered between servers. OPTIONAL ",
                            #            type=Type.STRING)
                            # ]
                            )
    async def cmd_setup_safeguard(self, ctx):
        await ctx.reply(type=5)
        server = await filter_db.FilterServer.filter(guild=ctx.guild.id).first()

        if server is None:
            server = filter_db.FilterServer(guild=ctx.guild.id, null=True, blank=True)
            await server.save()

        async def setup_buttons():
            if server.image_filter:
                safe_image = ButtonStyle.green
                text = "Disable SafeImage"
            else:
                safe_image = ButtonStyle.red
                text = "Enable SafeImage"
            # if server.text_filter_mode != 0:
            #     safe_text = ButtonStyle.red
            # else:
            #     safe_text = ButtonStyle.green
            buttons = ActionRow(
                Button(
                    style=safe_image,
                    label=text,
                    custom_id="SI"
                )
                # Button(
                #     style=safe_text,
                #     label="Enable SafeText",
                #     custom_id="ST"
                # )
            )
            msg = await ctx.edit(
                "These are the options for SafeGuard. We are planning to add more options in the future, "
                "including video filtering, text filtering, and more fine tuning. ", components=[buttons])
            return msg

        msg = await setup_buttons()
        on_click = msg.create_click_listener(timeout=60)

        @on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=False)
        async def on_wrong_user(inter):
            # Reply with a hidden message
            await inter.reply(
                "This command's buttons can only be used by the person who originally sent it for security reasons.",
                ephemeral=True)

        @on_click.matching_id("SI")
        async def on_test_button(ctx):
            server.image_filter = not server.image_filter
            await server.save()
            await setup_buttons()
            await ctx.reply(type=6)

        # SelectOption("Enable SafeImage", "enable"),
        # SelectOption("Adult image threshold", "adult_threshold"),
        # SelectOption("Medical image threshold", "medical_threshold"),
        # SelectOption("Spoof image threshold", "spoof_threshold"),
        # SelectOption("Violence image threshold", "violence_threshold"),
        # SelectOption("Racy image threshold", "racy_threshold"),
        # SelectOption("Notification threshold", "notification_threshold"),

    @commands.Cog.listener()
    async def on_message(self, message):
        # this is an alarming number of conditions. 
        if message.author.id != self.bot.user.id:
            server = await filter_db.FilterServer.filter(guild=message.guild.id).first()
            if server is not None and server.image_filter:
                channel = message.channel
                attachments = message.attachments
                if attachments is not None:
                    attachment_urls = [x.url for x in attachments]
                    for url in attachment_urls:
                        azure = ms_content_moderation.image_moderation(url)
                        pl, google = detect_safe_search_uri(url)
                        # print(azure, pl, google)
                        # if azure["adult_classification_score"] > server.azure_adult_threshold or google.adult / 5> server.google_adult_threshold or \
                        #         azure[
                        #             "racy_classification_score"] > server.azure_racy_threshold or google.racy /5 > server.google_racy_threshold or \
                        #         google.medical > server.google_medical_threshold or google.spoof > server.google_spoof_threshold or google.violence > server.google_violence_threshold:
                        if azure["adult_classification_score"] > 0.6 or google.adult / 5 > 0.6 or \
                                azure["racy_classification_score"] > 0.6 or google.racy / 5 > 0.6:
                            await channel.send("NSFW image detected. ")
                            await message.delete()
                            break
                if find_url(message.content) is not None:
                    urls = find_url(message.content)
                    for url in urls:
                        azure = ms_content_moderation.image_moderation(url)
                        pl, google = detect_safe_search_uri(url)
                        print(azure, pl, google)
                        if azure["adult_classification_score"] > 0.6 or google.adult / 5 > 0.6 or \
                                azure["racy_classification_score"] > 0.6 or google.racy / 5 > 0.6:
                            await channel.send("NSFW image detected. ")
                            await message.delete()
                            break


def setup(bot):
    bot.add_cog(SafeImage(bot))
