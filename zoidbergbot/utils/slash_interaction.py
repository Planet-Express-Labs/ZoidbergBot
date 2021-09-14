import dislash.slash_commands.slash_command
from dislash.interactions import SlashInteraction as DislashSlashInteraction, BaseInteraction as DislashBaseInteraction

class SlashInteraction(DislashSlashInteraction):
    pass

class BaseInteraction(DislashBaseInteraction):
    def get_user_info(self):
        self.author.id