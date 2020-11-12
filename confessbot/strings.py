import logging
from typing import Optional
from json import loads

log = logging.getLogger(__name__)


with open("./data/strings.json", "r") as strings_:
    STRINGS = loads(strings_.read())

REQUIRED_STRING_LIST = [
    "BOT_ABOUT",
    "CMD_PERMISSION_ERROR",
]

# Make sure all required strings are present
for s in REQUIRED_STRING_LIST:
    if STRINGS.get(s) is None:
        raise Exception(f"String {s} missing. Bot cannot open.")


class String:
    """
    helpful.
    """
    BOT_ABOUT = "BOT_ABOUT"
    CMD_NOT_ALLOWED_FOR_USER = "CMD_PERMISSION_ERROR"


def gets(string_name: str) -> Optional[str]:
    return STRINGS.get(string_name)
