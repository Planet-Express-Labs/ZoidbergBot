"""
8888888888P         d8b      888 888                                    888               888
      d88P          Y8P      888 888                                    888               888
     d88P                    888 888                                    888               888
    d88P    .d88b.  888  .d88888 88888b.   .d88b.  888d888 .d88b.       88888b.   .d88b.  888888
   d88P    d88""88b 888 d88" 888 888 "88b d8P  Y8b 888P"  d88P"88b      888 "88b d88""88b 888
  d88P     888  888 888 888  888 888  888 88888888 888    888  888      888  888 888  888 888
 d88P      Y88..88P 888 Y88b 888 888 d88P Y8b.     888    Y88b 888      888 d88P Y88..88P Y88b.
d8888888888 "Y88P"  888  "Y88888 88888P"   "Y8888  888     "Y88888      88888P"   "Y88P"   "Y888
                                                               888
                                                          Y8b d88P
                                                           "Y88P"
"""
# This software is provided free of charge without a warranty - meaning if you're an idiot and somehow
# blow up your sever, I am not liable or responsible.
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# This is designed to be used with Zoidberg bot, however I'm sure it could be adapted to work with your own projects.
# If there is an issue that might cause issue on your own bot, feel free to pull request if it will improve something.<3
import logging
from typing import Optional
from json import loads
from zoidbergbot.config import BOT_LANGUAGE

log = logging.getLogger(__name__)


with open(f"./data/{BOT_LANGUAGE}.json", "r") as read_strings:
    STRINGS = loads(read_strings.read())

# Maybe we shouldn't be handling version through localization...
REQUIRED_STRING_LIST = [
    "BOT_ABOUT",
    "CMD_PERMISSION_ERROR",
    "COMMAND_ON_COOLDOWN",
    "VERSION",
    "COMMAND_EMPTY_USER_ID",
    "NO_RESULTS",
    "MESSAGE_SENT"
]

# Makes sure everything is present on runtime.
for s in REQUIRED_STRING_LIST:
    if STRINGS.get(s) is None:
        raise Exception(f"String {s} missing or localization file is missing. The bot cannot start up. ")


def get_string(string_name: str) -> Optional[str]:
    return STRINGS.get(string_name)
