import asyncio

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

async def check_conditions(azure, google, channel, message, medical:bool):
    if (azure["adult_classification_score"] > 0.6 or google.adult / 5 > 0.8 or \
            google.racy == 5) or (not medical and (azure["medical_classification_score"] > 0.6 or \
            google.medical > 0.8)):
        await channel.send("NSFW image detected.")
        await message.delete()
        return


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
    return likelihood_name, safe


def find_url(string):
    # findall() has been used
    # with valid conditions for urls in string
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return urls


class SafeImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="scan-image",
                            guild_ids=guilds,
                            description="Scans an image for NSFW content using AI. ",
                            options=[
                                Option("image", "The link to the image to scan. ",
                                       type=Type.STRING, required=True)
                            ])
    async def cmd_scan_image(self, ctx):
        uri = ctx.get("image")
        print(uri)
        # if find_url(uri) == 1:
        await ctx.reply(type=5)
        resp, safe = detect_safe_search_uri(uri)
        result = ms_content_moderation.image_moderation(uri)
        embed = discord.Embed(title="Image scan results:",
                                description=(f'adult: {resp[safe.adult]}\n'
                                f'medical: {resp[safe.medical]}\n'
                                f'spoofed: {resp[safe.spoof]}\n'
                                f'violence: {resp[safe.violence]}\n'
                                f'racy: {resp[safe.racy]}\n',
                                f'adult: {result["adult_classification_score"]}\n',
                                f'medical: {result["racy_classification_score"]}\n'))
        await ctx.edit(embed=embed)
        # else:
        # await ctx.reply("This must be in the format of a URI/URL!")

    @slash_commands.has_permissions(administrator=True)
    @slash_command(name="safeguard-ai",
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
            if server.allow_for_channels != '':
                channel_override = ButtonStyle.green
                channel_override_text = "Channel override set."
            else:
                channel_override = ButtonStyle.red
                channel_override_text = "Channel overrides have not been set."
            if server.allow_nsfw_channels:
                nsfw_override = ButtonStyle.green
                nsfw_override_text = "NSFW channels are ignored."
            else:
                nsfw_override = ButtonStyle.red
                nsfw_override_text = "NSFW channels are not ignored."
            if server.allow_for_roles != '':
                role_override = ButtonStyle.green
                role_override_text = "Role override set."
            else:
                role_override = ButtonStyle.red
                role_override_text = "Role overrides have not been set."
                
            buttons = ActionRow(
                Button(
                    style=safe_image,
                    label=text,
                    custom_id="SI"
                ),
                Button(
                    style=channel_override,
                    label=channel_override_text,
                    custom_id="CO"),
                Button(
                    style=nsfw_override,
                    label=nsfw_override_text,
                    custom_id="NSFW"),
                Button(
                    style=role_override,
                    label=role_override_text,
                    custom_id="RL"
                )
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
            print(server.image_filter)
            server.image_filter = not server.image_filter
            print(server.image_filter)
            await server.save()
            await setup_buttons()
            await ctx.reply(type=6)
            
        @on_click.matching_id("CO")
        async def on_test_button(inter):
            def check(m):
                if m.channel.id == inter.channel.id and m.author.id == inter.author.id:
                 return m.content
            if server.allow_for_channels != '':
                await ctx.send(f"Here's your current setting: {server.allow_for_channels}")
            await ctx.send("Waiting for list of channel ids or tags. Separate each entry with a comma.")
            await inter.reply(type=5)
            try:
                resp = await self.bot.wait_for('message', check=check)
            except asyncio.TimeoutError:
                await ctx.reply("Timeout reached. Try again. ")
            print(resp)
            resp = re.sub("[<># ]", '', resp.content)
            resp = resp.split(',')
            print(resp)
            for each in resp:
                try:
                    channel = await self.bot.fetch_channel(each)
                except discord.errors.HTTPException:
                    return await inter.reply(f"Entry invalid: {each}\nThere is a chance this is an issue in our "
                                             "codebase.")
                if channel is None:
                    return await inter.reply("Entry invalid: " + each)
            server.allow_for_channels = resp
            await server.save()
            await setup_buttons()
            await inter.edit("Your channels have been recorded.")
        
        @on_click.matching_id("RL")
        async def on_test_button(inter):
            def check(m):
                return m.content
            if server.allow_for_roles != '':
                await ctx.send(f"Here's your current setting: {server.allow_for_roles}")
            await ctx.send("Waiting for a list of role names. Separate each entry with a comma, with spaces.\n"
                           "role_name, role name 2")
            await inter.reply(type=5)
            try:
                resp = await self.bot.wait_for('message', check=check)
            except asyncio.TimeoutError:
                await ctx.reply("Timeout reached. Try again. ")
            resp = resp.content.split(',')
            ids = []
            for each in resp:
                for role in ctx.guild.roles:
                    if role.name == each:
                        ids.append(role.id)
            server.allow_for_roles = str(ids)
            await server.save()
            await inter.edit("Your roles have been recorded.")
     
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # this is an alarming number of conditions. 
        if message.author.id != self.bot.user.id:
            server = await filter_db.FilterServer.filter(guild=message.guild.id).first()
            if server is not None and server.image_filter:
                if message.channel.is_nsfw and not server.allow_nsfw_channels:
                    return
                roles = list(server.allow_for_roles)
                if not isinstance(message.author, discord.Member):
                    member = message.guild.get_member(message.author.id)
                else:
                    member = message.author
                if roles is not None:
                    for each in member.roles:
                        if each in roles:
                            return

                permissions = list(server.allow_for_permissions)
                if permissions is not None:
                    for each in message.author.permissions_in(message.channel):
                        if each in permissions:
                            return

                channels = list(server.allow_for_channels)
                for each in channels:
                    if message.channel.id == each:
                        return

                channel = message.channel
                attachments = message.attachments
                if attachments is not None:
                    attachment_urls = [x.url for x in attachments]
                    for url in attachment_urls:
                        azure = ms_content_moderation.image_moderation(url)
                        pl, google = detect_safe_search_uri(url)
                        await check_conditions(azure, google, channel, message, server.allow_medical)
                        break

                if find_url(message.content) is not None:
                    urls = find_url(message.content)
                    for url in urls:
                        azure = ms_content_moderation.image_moderation(url)
                        pl, google = detect_safe_search_uri(url)
                        print(azure, pl, google)
                        await check_conditions(azure, google, channel, message, server.allow_medical)
                        break


def setup(bot):
    bot.add_cog(SafeImage(bot))
