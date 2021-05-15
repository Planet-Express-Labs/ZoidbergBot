import logging
from typing import Optional
from json import loads
from zoidbergbot.config import BOT_LANGUAGE

log = logging.getLogger(__name__)


with open(f"./data/{BOT_LANGUAGE}.json", "r") as read_strings:
    STRINGS = loads(read_strings.read())

REQUIRED_STRING_LIST = [
    "BOT_ABOUT",
    "CMD_PERMISSION_ERROR",
    "COMMAND_ON_COOLDOWN",
    "VERSION",
    "COMMAND_EMPTY_USER_ID"
]

# Makes sure everything is present on runtime.
for s in REQUIRED_STRING_LIST:
    if STRINGS.get(s) is None:
        raise Exception(f"String {s} missing or localization file is missing. The bot cannot start up. ")


def get_string(string_name: str) -> Optional[str]:
    return STRINGS.get(string_name)
