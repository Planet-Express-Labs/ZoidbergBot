from zoidbergbot.config import *


def verify_user(ctx, perm):
    if perm == "dev":
        print(DEV_ID, ctx.message.author.id)
        return int(ctx.message.author.id) == int(DEV_ID)
    if perm == "admin":
        for each in ADMIN_ID:
            print(ADMIN_ID, ctx.message.author.id)
            return int(ctx.message.author.id) == int(each)
