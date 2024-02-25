import discord, discord.ui


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Delete Bot Message', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Code to delete bot message
        await interaction.response.send_message('Bot message deleted!', ephemeral=True)

    @discord.ui.button(label='Delete Original Message', style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Code to delete original message
        await interaction.response.send_message('Original message deleted!', ephemeral=True)
        