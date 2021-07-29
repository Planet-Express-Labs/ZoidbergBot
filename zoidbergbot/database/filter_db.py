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


class FilterServer(Model):
    guild = fields.BigIntField(pk=True)

    image_filter = fields.BooleanField(default=False, null=True, blank=True)

    allow_nsfw_channels = fields.BooleanField(default=True, null=True, blank=True)
    allow_for_roles = fields.TextField(default='', null=True, blank=True)  # placeholder
    action = fields.TextField(default='', null=True, blank=True)  # placeholder

    google_adult_threshold = fields.IntField(default=6, null=True, blank=True)
    google_racy_threshold = fields.IntField(default=6, null=True, blank=True)
    google_medical_threshold = fields.IntField(default=9, null=True, blank=True)
    google_spoofed_threshold = fields.IntField(default=10, null=True, blank=True)
    google_violence_threshold = fields.IntField(default=7, null=True, blank=True)

    azure_adult_threshold = fields.IntField(default=6, null=True, blank=True)
    azure_racy_threshold = fields.IntField(default=8, null=True, blank=True)
    image_algor_bias = fields.IntField(default=1, null=True, blank=True)

    text_filtering = fields.BooleanField(default=False, null=True, blank=True)
    text_threshold = fields.IntField(default=8, null=True, blank=True)

    facial_recognition = fields.BooleanField(default=False, null=True, blank=True)
    facial_threshold = fields.IntField(default=5, null=True, blank=True)

    event_channel = fields.BigIntField(default=0, null=True, blank=True)
