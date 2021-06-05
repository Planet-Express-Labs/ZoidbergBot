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

# This isn't even really a cog. 

import sqlite3

from discord.ext import commands
from dislash.interactions import *
from dislash.slash_commands import *

from bot import bot, slash
from zoidbergbot.config import *

# TODO: It's probably worth adding something to remove servers when the bot has been removed or perhaps even inactive
#  servers if it gets to the point of causing an actual response time issue

# Yup! it's your local moron reusing code that I'm planning on getting rid of later!
# To be fair, I don't really know how much it really matters here.
if not os.path.isfile(os.getcwd() + '\\data\\logging.db'):
    print("Logging DB missing! Creating new DB. ")
    connection = sqlite3.connect(os.getcwd() + '\\data\\logging.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE logging (
                    guild INTEGER PRIMARY KEY,
                    log_channel INTEGER,
                    message_log_channel INTEGER,
                    log_joins BOOLEAN DEFAULT False,
                    log_leaves BOOLEA NDEFAULT False,
                    log_invites BOOLEAN DEFAULT False,
                    log_messages BOOLEAN DEFAULT False,
                    log_message_edits BOOLEAN DEFAULT False,
                    log_roles BOOLEAN DEFAULT False,
                    log_profile BOOLEAN DEFAULT False,
                    log_nickname BOOLEAN DEFAULT False,
                    log_user_nickname BOOLEAN DEFAULT False,
                    log_bans BOOLEAN DEFAULT False,
                    log_kicks BOOLEAN DEFAULT False,
                    log_vc_mute BOOLEAN DEFAULT False,
                    log_vc_move BOOLEAN DEFAULT False,
                    log_vc_kick BOOLEAN DEFAULT False,
                    log_vc_user_mute BOOLEAN DEFAULT False,        
                    log_vc_user_leave BOOLEAN DEFAULT False  
                    )"""
                   )
else:
    # I know that sqlite3 will automatically make the db file, but I'd prefer to handle it like this.
    connection = sqlite3.connect(os.getcwd() + '\\data\\logging.db')
    cursor = connection.cursor()


def initialize_server(guild):
    # This might be worth having it back up the db every time.
    # Holy cow this is bad.
    # Please put this code out of it's misery.
    cursor.execute(f'''INSERT INTO logging({guild} {False} {False} {False} {False} {False} {False} {False} {False} {False} {False} {False} {False} {False} {False} {False} {False} {False} {False} )''')
    # cursor.execute(f'''INSERT INTO logging({guild})''')
    connection.commit()


def update_attribute(column, value, guild):
    cursor.execute(f"""UPDATE logging 
                    SET {column} = {value} 
                    WHERE guild = {guild}; 
                    """)
    connection.commit()


def get_val(val, guild):
    data = cursor.execute(f'SELECT {val} FROM logging WHERE guild = {guild}')
    return int(''.join(map(str, data.fetchall()[0])))


class Logging(commands.Cog):

    # noinspection PyShadowingNames
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild == get_val("log_joins", member.guild):
            channel = member.guild.system_channel
            guild = member.guild
            invites = await guild.invites()
            invite = None
            for each in invites:
                if member.id in each.uses:
                    invite = each
            if channel is not None:
                await channel.send(f"""{member.display_name} has joined the server. 
                :calendar_spiral:Account made: {member.created_at}
                :incoming_envelope:Invite used: {invite.id}
                --> :detective:Created by: {invite.inviter}
                """)

    @commands.command(name="setup-logging")
    async def cmd_setup_logging(self, ctx, msg=None, inter=None):
        options = ["log_channel", "message_log_channel", "log_joins", "log_leaves", "log_invites",
                   "log_messages", "log_message_edits", "log_roles", "log_profile", "log_nickname", "log_user_nickname",
                   "log_bans", "log_kicks", "log_vc_mute", "log_vc_move", "log_vc_kick", "log_vc_user_mute",
                   "log_vc_user_leave"]

        # jesus christ. fix it fix it fix it fix it fix it fix it fix it fix it fix it fix it fix it fix it fix it fixit
        # Also, this needs to be changed so I can localize it at some point. Ouch.
        friendly_options = ["action logging channel", "message logging channel", "log user joins", "log user leaves",
                            "log when invites are created or used.", "log message deletions",
                            "log when messages are edited", "log when roles are given/removed",
                            "log profile changes like usernames", "log nickname changes when changed by an admin",
                            "log nicknames when changed by the user", "log bans", "log kicks",
                            "log when someone is muted", "log if someone is moved VC channels by an admin",
                            "log when someone is kicked from a voice channel", "log when someone mutes themselves",
                            "log when someone leaves a voice channel"]
        buttons = []
        button_grid = auto_rows(max_in_row=5)

        # This is a garbage solution.
        async def refresh_buttons(grid):
            for index, each in enumerate(options):
                color = ButtonStyle.blurple
                state = get_val(each, ctx.guild)
                if type(state) == bool:
                    if state:
                        color = ButtonStyle.green
                    else:
                        color = ButtonStyle.red

                button = Button(
                    style=color,
                    label=friendly_options[index],
                    custom_id=each
                )
                buttons.append(button)
                grid = auto_rows(*buttons, max_in_row=5)
            return grid

        try:
            if inter is None:
                msg = await ctx.send("Click each button to configure the options.", components=button_grid)
            else:
                await inter.reply(f"", components=[buttons], type=7)
        except ValueError:
            pass

        button_grid = await refresh_buttons(button_grid)


        def wait_for(inter):
            return inter.message.id == msg.id

        inter = await ctx.wait_for_button_click(wait_for)


# noinspection PyShadowingNames
def setup(bot):
    bot.add_cog(Logging(bot))
