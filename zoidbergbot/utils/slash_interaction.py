import dislash.slash_commands.slash_command
from dislash.interactions import SlashInteraction as DislashSlashInteraction, BaseInteraction as DislashBaseInteraction
from zoidbergbot.database import user

class BaseInteraction(DislashBaseInteraction):
    def get_user_info(self):
        server = user.ZoidbergUser().filter(id = self.author.id).first
        return server

class SlashInteraction(BaseInteraction):
    pass
