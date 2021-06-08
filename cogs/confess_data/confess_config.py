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


import configparser
import logging
import codecs
import os
import csv

from json import loads

log = logging.getLogger(__name__)

CONFIG_FILE = os.getcwd() + "\\cogs\\confess_data\\config.ini"
config = configparser.ConfigParser()
config.read_file(codecs.open(CONFIG_FILE, "r+", "utf-8"))


def read_config(section, value, file="./data/config.ini"):
    config.read_file(codecs.open(file, "r+", "utf-8"))


MAX_BACKUPS = config.get("db", "max_backups")

####################
#       bans       #
####################

#
# def get_bans():
#     with open("./data/bans.csv", newline='') as file:
#         names = []
#         read = csv.reader(file, delimiter='\n', quotechar='|')
#         for row in read:
#             names.append(row)
#         return names
#
#
# def get_user_ban(name):
#     if not os.path.isfile("./data/bans.csv"):
#         file = open("./data/bans.csv", "w")
#         file.close()
#     bans = get_bans()
#     for each in bans:
#         if each == name:
#             return True
#     return False
#
#
# I highly doubt this is remotely close to the correct way of doing something like this, but it is what it is, I guess.
# def rm_ban(user):
#     with open("./data/bans.csv", newline='') as read_file:
#         read = csv.reader(read_file, delimiter='\n', quotechar='|')
#         file = []
#         for each in read:
#             if each != user:
#                 file.append(each)
#     with open("./data/bans.csv", 'w+', newline='') as write_file:
#         write = csv.writer(write_file, delimiter='\n', quotechar='|')
#         for each in file:
#             write.writerow(each)
#
#
# def add_ban(user):
#     if get_user_ban(user):
#         return False
#     with open("./data/bans.csv", "a", newline='') as write_file:
#         write = csv.writer(write_file, delimiter='\n', quotechar='|')
#         user = [user]
#         write.writerow(user)
