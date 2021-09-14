from tortoise.models import Model
from tortoise import fields

class ZoidbergUser(Model):
    id = fields.BigIntField(pk=True)

    premium = fields.BooleanField(default=False)
    premium_expire = fields.DatetimeField(null=True)
    
    timezone = fields.CharField(default="UTC")
    language = fields.CharField(default="en")
    auto_file_tools = fields.boolField(default=False)
    bans = fields.JSONField(default=dict)
    warnings = fields.JSONField(default=dict)