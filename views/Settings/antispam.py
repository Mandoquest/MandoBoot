import discord
from discord.ui import View, Button

from funktionen.choose_Embeds import choose_Embeds
from funktionen.choose_Views import choose_Views
from funktionen.check_admin import AuthorView

class AntispamButtons(AuthorView):
    def __init__(self, author_id):
        super().__init__(author_id=author_id, timeout=None)
        self.author_id = author_id
    
    @discord.ui.button(label="Back", style=discord.ButtonStyle.primary, emoji="◀️")
    async def first_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = await choose_Embeds("Main", guild=interaction.guild)
        view = choose_Views("Main", author_id=self.author_id)
        await interaction.response.edit_message(embed=embed, view=view)