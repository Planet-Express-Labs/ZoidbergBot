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


import codecs
import configparser
import logging
import os

log = logging.getLogger(__name__)
use_env = False
required_vars = ["token", "logging", "developer", "admin"]


class MissingEnvironmentVariableError(Exception):
    """Raised when a value is not found in the environment variables. """
    pass


if not os.path.exists(os.getcwd() + "\\data\\config.ini"):
    print("Config file missing! Attempting to use environment variables. ")
    for each in required_vars:
        # checks each required variable if it exists and raises an exception if it isn't.
        temp = os.getenv("zoidberg_" + each)
        if temp is None:
            raise MissingEnvironmentVariableError

    BOT_TOKEN = os.getenv("zoidberg_token")
    LOGGING_LEVEL = os.getenv("zoidberg_logging")

    # These will be removed later.
    DEV_ID = os.getenv("zoidberg_developer").split(",")
    ADMIN_ID = os.getenv("zoidberg_admin").split(",")
    TEST_GUILDS = os.getenv("zoidberg_guilds")
    if TEST_GUILDS is not None:
        TEST_GUILDS = TEST_GUILDS.split(",")
else:
    CONFIG_FILE = os.getcwd() + "\\data\\config.ini"
    config = configparser.ConfigParser()
    config.read_file(codecs.open(CONFIG_FILE, "r+", "utf-8"))


    def read_config(section, value, file=CONFIG_FILE):
        config.read_file(codecs.open(file, "r+", "utf-8"))


    # Bot section.
    TEST_GUILDS = config.get("Bot", "testing_guilds").split(" ")

    DATABASE = config.get("Bot", "database_path")
    BOT_TOKEN = config.get("Bot", "bot_token")

    LOGGING_LEVEL = config.get("Bot", "logging_level")
    DEV_ID = config.get("Users", "developer_id")
    ADMIN_ID = config.get("Users", "admin_ids").split(" ")
