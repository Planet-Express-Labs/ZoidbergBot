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
from sqlalchemy import Column, String, Date, Integer, Numeric

from sessions import Base


class Server(Base):
    __tablename__ = 'server_data'

    guild = Column(Integer, primary_key=True)
    enabled_modules = Column(String)  # Reserved for future use
    # I'll probably change this to something that will allow more then just two levels of permission, but that's later.
    # If admin_role == 0, then it's just going to go off of each role's permissions.
    admin_role = Column(bool)
    mod_role = Column(bool)
    cooldown = Column(Integer)  # Reserved for future use
    auto_delete = Column(Integer)  # Reserved for future use
    premium = Column(bool)  # Reserved for future use
    official_guild = Column(bool)

    def __init__(self, enabled_modules, guild, admin_role, mod_role, cooldown, auto_delete, premium, official_guild):
        self.guild = guild
        self.enabled_modules = enabled_modules
        self.admin_role = admin_role
        self.mod_role = mod_role
        self.cooldown = cooldown
        self.auto_delete = auto_delete
        self.premium = premium
        self.official_guild = official_guild
