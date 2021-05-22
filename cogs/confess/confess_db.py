import sqlite3
import os

import discord

from bot import bot
from discord.ext.commands import Context

if not os.path.isfile(os.getcwd() + '/data.db'):
    print("Confess DB missing! Creating new DB. ")
    connection = sqlite3.connect(os.getcwd() + '/data.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE confess_data (
                    guild INTEGER,
                    confess_channel INTEGER,
                    logging_channel INTEGER,
                    last_message_number INTEGER)"""
                   )
else:
    # I know that sqlite3 will automatically make the db file, but I'd prefer to handle it like this.
    connection = sqlite3.connect(os.getcwd() + '/data.db')
    cursor = connection.cursor()

# I really hope to restructure this. If I could somehow make the database entry a python object without having to parse
# like every like, I'd be happy. If anyone knows how to do that, please, please, PR, and I'll love you forever.


def initialize_server(guild, logging_channel, confess_channel):
    # This might be worth having it back up the db every time.
    cursor.execute(f'''INSERT INTO confess_data(guild, confess_channel, logging_channel, last_message_number)
                        VALUES({guild}, {confess_channel} , {logging_channel} , {0});''')
    connection.commit()


def update_channel(channel, channel_id, guild):
    cursor.execute(f"""UPDATE confess_data 
                    SET {channel} = {channel_id} 
                    WHERE guild = {guild}; 
                    """)
    connection.commit()


def increment_last_message(guild):
    data = cursor.execute(f'SELECT last_message_number FROM confess_data WHERE guild = {guild}')
    data = int(''.join(map(str, data.fetchall()[0]))) + 1
    cursor.execute(f'UPDATE confess_data set last_message_number={data} WHERE guild={guild};')
    connection.commit()


def get_db_int(channel, guild):
    data = cursor.execute(f'SELECT {channel} FROM confess_data WHERE guild = {guild}')
    return int(''.join(map(str, data.fetchall()[0])))


def server_picker(ctx: Context):
    author = ctx.message.author()
    servers = ""
    i = 0
    for each in author.mutual_guilds():
        i += 1
        logging = get_db_int("logging_channel", each) != 0
        servers += f"{i}: {bot.get_guild(each)}\n```logging: {logging}\n```"

    embed = discord.Embed(title="Which server do you want me to send this message in? ",
                          description="Please react with the server you want to choose. . \n" + servers
                          )
    message = ctx.send(embed=embed)

