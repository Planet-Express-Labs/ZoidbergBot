from discord.ext import commands
from dislash import *

from bot import guilds


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @slash_commands.command(name="role_menu")
    # async def cmd_role_menu(self):
    #     pass

    @slash_commands.has_permissions(administrator=True)
    @slash_commands.command(name="select_roles",
                            guild_ids=guilds,
                            options=[
                                Option("member", "Who you want to apply these role edits to. ", type=Type.USER)
                            ])
    async def cmd_select_roles(self, ctx: SlashInteraction):
        guild = ctx.guild
        roles = guild.roles
        member = ctx.get("member")
        menus = []
        options = []
        for index, role in enumerate(roles):
            if index == 25:
                menus.append(
                    SelectMenu(
                        custom_id=f"Roles{index}",
                        placeholder="Pick roles.",
                        options=options
                    ))
                options = []
            options.append(SelectOption(role.name, "select_roles" + role.id))
        menus.append(
                    SelectMenu(
                        custom_id=f"Roles{index}",
                        placeholder="Pick roles.",
                        options=options
                    ))
        print(menus)
        await ctx.send(
            f"Select which roles you want to give {member.name}:",
            components=menus
        )



def setup(bot):
    bot.add_cog(Roles(bot))
