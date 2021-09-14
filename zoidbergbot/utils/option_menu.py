import discord
from dislash import *
from tortoise import *

class OptionMenu:
    def __init__(self, tortoise_object:Tortoise):
        self.fields = []

    def add_field(self, name: str, prompt_text: str, field_type: str):
        """
        Adds a field into your OptionMenu object. Field type must be of the following strings:
            - channel, waits for user to tag a channel and saves it into your database.
        """
        field = {"name": name, "prompt": prompt_text, "type": field_type}
        self.fields.append(field)
