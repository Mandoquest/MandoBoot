import discord

from funktionen.choose_Embeds import choose_Embeds
from funktionen.choose_Views import choose_Views
from funktionen.check_admin import AuthorView
from funktionen.welcome_message_Datenbank import set_welcome_channel

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
        guild_id = interaction.guild.id
        channel_id = selected_channel.id
        set_welcome_channel(guild_id, channel_id)
        await interaction.response.send_message(f"Welcome channel set to **{selected_channel.name}**. Reload the menu to see the change.",ephemeral=True)


class WelcomeChannel_View(AuthorView):
    def __init__(self, author_id: int):
        super().__init__(timeout=None, author_id = author_id)
        
        self.add_item(ChannelSelect()) 

    @discord.ui.button(label="Back", style=discord.ButtonStyle.primary, emoji="◀️", row=1)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = await choose_Embeds("Main", guild=interaction.guild)
        view = choose_Views("Main", author_id=self.author_id)
        await interaction.response.edit_message(embed=embed, view=view)