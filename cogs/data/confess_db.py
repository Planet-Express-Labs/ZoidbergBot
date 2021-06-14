# 8888888888P         d8b      888 888                                    888               888
#       d88P          Y8P      888 888                                    888               888
#      d88P                    888 888                                    888               888
#     d88P    .d88b.  888  .d88888 88888b.   .d88b.  888d888 .d88b.       88888b.   .d88b.  888888
#    d88P    d88""88b 888 d88" 888 888 "88b d8P  Y8b 888P"  d88P"88b      888 "88b d88""88b 888
#   d88P     888  888 888 888  888 888  888 88888888 888    888  888      888  888 888  888 888
#  d88P      Y88..88P 888 Y88b 888 888 d88P Y8b.     888    Y88b 888      888 d88P Y88..88P Y88b.
# d8888888888 "Y88P"  888  "Y88888 88888P"   "Y8888  888     "Y88888      88888P"   "Y88P"   "Y888
# This software is provided free of charge without a warranty.   888
# This Source Code Form is subject to the terms of the      Y8b d88P
# Mozilla Public License, v. 2.0. If a copy of the MPL was   "Y88P"
# this file, You can obtain one at https://mozilla.org/MPL/2.0/.

# This is designed to be used with Zoidberg bot, however I'm sure it could be adapted to work with your own projects.
# If there is an issue that might cause issue on your own bot, feel free to pull request if it will improve something.<3
import sqlite3
import os

import discord

from bot import bot
from discord.ext.commands import Context
from dislash import *

slash = SlashClient(bot)

if not os.path.isfile(os.getcwd() + '\\data.db'):
    print("Confess DB missing! Creating new DB. ")
    connection = sqlite3.connect(os.getcwd() + '\\data.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE data (
                    guild INTEGER,
                    confess_channel INTEGER,
                    logging_channel INTEGER,
                    last_message_number INTEGER)"""
                   )
else:
    # I know that sqlite3 will automatically make the db file, but I'd prefer to handle it like this.
    connection = sqlite3.connect(os.getcwd() + '\\data.db')
    cursor = connection.cursor()


# I really hope to restructure this. If I could somehow make the database entry a python object without having to parse
# like every like, I'd be happy. If anyone knows how to do that, please, please, PR, and I'll love you forever.


def initialize_server(guild, logging_channel, confess_channel):
    # This might be worth having it back up the db every time.
    cursor.execute(f'''INSERT INTO data(guild, confess_channel, logging_channel, last_message_number)
                        VALUES({guild}, {confess_channel} , {logging_channel} , {0});''')
    connection.commit()


def update_channel(channel, channel_id, guild):
    cursor.execute(f"""UPDATE data 
                    SET {channel} = {channel_id} 
                    WHERE guild = {guild}; 
                    """)
    connection.commit()


def increment_last_message(guild):
    data = cursor.execute(f'SELECT last_message_number FROM data WHERE guild = {guild}')
    data = int(''.join(map(str, data.fetchall()[0]))) + 1
    cursor.execute(f'UPDATE data set last_message_number={data} WHERE guild={guild};')
    connection.commit()


def get_db_int(channel, guild):
    data = cursor.execute(f'SELECT {channel} FROM data WHERE guild = {guild}')
    return int(''.join(map(str, data.fetchall()[0])))


async def server_picker(ctx: Context):
    author = ctx.message.author()
    servers = ""
    i = 0
    guilds = author.mutual_guilds()
    print(guilds)
    if guilds is None:
        return None
    # for each in guilds:
    #     i += 1
    #     logging = get_db_int("logging_channel", each) != 0
    #     servers += f"{i}: {bot.get_guild(each)}\n```logging: {logging}\n```"

    embed = discord.Embed(title="Which server do you want me to send this message in? ",
                          description="Please click which server you want to send this in: \n Loading servers... "
                          )

    if guilds > 25:
        embed = discord.Embed(title="Which server do you want me to send this message in? ",
                              description="Please send the number of the server you want to choose: \n" + servers
                              )
        message = await ctx.send(embed=embed)
    else:
        def get_logging(guild):
            if get_db_int("logging_channel", guild.id) == 0:
                return True
            return False

        buttons = []
        for each in guilds:
            buttons += Button(
                style=ButtonStyle.green,
                label=f"{each.name}\n :notepad_spiral: - {get_logging(each)}",
                custom_id=each
            )
        button_elements = auto_rows(buttons, max_in_row=5)
        message = await ctx.send(embed=embed, content=button_elements)

    def wait_for(inter):
        return inter.message.id == message.id

    inter = await ctx.wait_for_button_click(wait_for)
    # Send what you received
    for each in servers:
        if inter.clicked_button.custom_id == each:
            return each
    return None
