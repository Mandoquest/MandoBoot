import discord

from funktionen.choose_Embeds import choose_Embeds
from funktionen.choose_Views import choose_Views


class Prefix_View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Zurück", style=discord.ButtonStyle.primary, emoji="◀️")
    async def back_button_callback(
        self, interaction: discord.Interaction, button: discord.ui.button
    ):
        await interaction.response.edit_message(
            embed=choose_Embeds("Main"), view=choose_Views("Main")
        )

    @discord.ui.button(
        label="change Prefix", style=discord.ButtonStyle.primary, emoji="✏️"
    )
    async def second_button_callback(
        self, interaction: discord.Interaction, button: discord.ui.button
    ):
        member = interaction.user
        if isinstance(member, discord.Member):
            if member.guild_permissions.administrator:
                await interaction.response.send_message(
                    "Du bist ein Admin!", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "Du bist kein Admin.", ephemeral=True
                )
        else:
            await interaction.response.send_message(
                "Konnte Mitglied nicht ermitteln.", ephemeral=True
            )
