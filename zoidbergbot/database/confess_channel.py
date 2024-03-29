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
from tortoise.models import Model
from tortoise import fields


class ConfessChannel(Model):
    confess_id = fields.IntField(pk=True)
    enable = fields.BooleanField(default=False, null=True)
    guild = fields.BigIntField(default=0, null=True)
    confess_channel = fields.BigIntField(default=0)
    log_channel = fields.BigIntField(default=0, null=True)
    last_confess = fields.BigIntField(default=0, null=True)
    blocked_users = fields.TextField(default="", null=True)
    whitelist = fields.BooleanField(default=False, null=True)
    allowed_roles = fields.TextField(default="", null=True)
