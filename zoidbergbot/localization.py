import logging
from typing import Optional
from json import loads

log = logging.getLogger(__name__)


with open("./data/strings.json", "r") as read_strings:
    STRINGS = loads(read_strings.read())

REQUIRED_STRING_LIST = [
    "BOT_ABOUT",
    "CMD_PERMISSION_ERROR",
    "COMMAND_ON_COOLDOWN",
    "VERSION"
]

# Make sure all required strings are present
for s in REQUIRED_STRING_LIST:
    if STRINGS.get(s) is None:
        raise Exception(f"String {s} missing. Bot cannot open.")


class String:
    BOT_ABOUT = "BOT_ABOUT"
    CMD_NOT_ALLOWED_FOR_USER = "CMD_PERMISSION_ERROR"
    COMMAND_ON_COOLDOWN = "COMMAND_ON_COOLDOWN"
    VERSION = "VERSION"


def get_string(string_name: str) -> Optional[str]:
    return STRINGS.get(string_name)
