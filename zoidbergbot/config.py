"""
  ____             __ _           _   
 / ___|___  _ __  / _| |__   ___ | |_ 
| |   / _ \| '_ \| |_| '_ \ / _ \| __|
| |__| (_) | | | |  _| |_) | (_) | |_ 
 \____\___/|_| |_|_| |_.__/ \___/ \__|
                                      

 ____  _____ _____  _      ____  ____      _    _   _  ____ _   _ 
| __ )| ____|_   _|/ \    | __ )|  _ \    / \  | \ | |/ ___| | | |
|  _ \|  _|   | | / _ \   |  _ \| |_) |  / _ \ |  \| | |   | |_| |
| |_) | |___  | |/ ___ \  | |_) |  _ <  / ___ \| |\  | |___|  _  |
|____/|_____| |_/_/   \_\ |____/|_| \_\/_/   \_\_| \_|\____|_| |_|
"""
# This software is provided free of charge without a warranty - meaning if you're an idiot and somehow
# blow up your sever, I am not liable or responsible.
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import configparser
import logging
import codecs
import os
import csv

from json import loads

log = logging.getLogger(__name__)

CONFIG_FILE = "./data/config.ini"
config = configparser.ConfigParser()
config.read_file(codecs.open(CONFIG_FILE, "r+", "utf-8"))


def read_config(section, value, file="./data/config.ini"):
    config.read_file(codecs.open(file, "r+", "utf-8"))


try:
    CHANNEL_ID = config.get("Bot", "channel_id")
except configparser.NoOptionError:
    print("config.ini missing!")
BOT_TOKEN = config.get("Bot", "bot_token", fallback=None)
BOT_PREFIX = config.get("Bot", "bot_prefix", fallback="!").strip(" ")
SPECIAL_USERS_IDS = [int(id_) for id_ in loads(config.get("Bot", "special_user_ids", fallback="[]"))]


# Users section.

log.info(f"Special users: {', '.join([str(a) for a in SPECIAL_USERS_IDS])}")
DEV_ID = config.get("Users", "developer_id").strip(" ")
ADMIN_ID = config.get("Users", "admin_id").split()
CONFESS_BANS = config.get("Users", "confess_ban").split()
GUILD_ID: int = config.getint("Bot", "guild_id")
LOG_ID:int = config.getint("Bot", "log_channel_id")

"""def add_banned_user(id):
    ban_list = config.get("Users", "confess_ban").split()
    banned: str = ''
    for each in ban_list:
        banned += f"{str(each)} "
    banned += str(id)
    print(banned)
    config.set("Users", "confess_ban", str(banned))
    config.write(codecs.open(CONFIG_FILE, "r+", "utf-8"))
    config.read_file(codecs.open(CONFIG_FILE, "r+", "utf-8"))
    CONFESS_BANS = config.get("Users", "confess_ban").split()


def remove_banned_user(id):
    ban_list = config.get("Users", "confess_ban").split()
    banned: str = ''
    for each in ban_list:
        if each is not id:
            banned += f"{str(each)} "
    config.set("Users", "confess_ban", str(banned))
    config.write(codecs.open(CONFIG_FILE, "r+", "utf-8"))
    config.read_file(codecs.open(CONFIG_FILE, "r+", "utf-8"))
    CONFESS_BANS = config.get("Users", "confess_ban").split()
"""
####################
#       bans       #
####################


# TODO: fix all of this garbage. I really have no idea if it works.
def add_banned_user(self, name):
    with open(os.getcwd()+'/data/bans.csv', 'w', newline='') as file:
        write = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        write.writerow(name)


def get_bans(self):
    with open(os.getcwd()+"/data/bans.csv", 'w', newline='') as file:
        names = []
        read = csv.reader(file, delimiter=' ', quotechar='|')
        for row in read:
            names += row
            print(names)

