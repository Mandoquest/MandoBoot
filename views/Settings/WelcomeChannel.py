import discord

from funktionen.choose_Embeds import choose_Embeds
from funktionen.choose_Views import choose_Views


class ChannelSelect(discord.ui.ChannelSelect):
    def __init__(self):
        super().__init__(
            placeholder="Kanal für Willkommensnachrichten wählen",
            min_values=1,
            max_values=1,
            channel_types=[discord.ChannelType.text],
        )

    async def callback(self, interaction: discord.Interaction):
        selected_channel = self.values[0]
        await interaction.response.send_message(
            f"Willkommenskanal gesetzt auf **{selected_channel.name}**.",
            ephemeral=True,
        )


class WelcomeChannel_View(discord.ui.View):
    def __init__(self, author_id: int):
        super().__init__(timeout=None)
        self.author_id = author_id
        self.add_item(ChannelSelect()) 

    @discord.ui.button(label="Zurück", style=discord.ButtonStyle.primary, emoji="◀️", row=1)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Nicht dein Button!", ephemeral=True)
            return
        await interaction.response.send_message("Zurück zum Hauptmenü.", ephemeral=True)