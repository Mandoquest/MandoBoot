import discord
from discord.ui import View, Button

from funktionen.choose_Embeds import choose_Embeds
from funktionen.choose_Views import choose_Views
from funktionen.check_admin import AuthorView


class MainButtons(AuthorView):
    def __init__(self, author_id):
        super().__init__(author_id=author_id, timeout=None)
        self.author_id = author_id

    

    @discord.ui.button(
        label="Welcome Channel", style=discord.ButtonStyle.primary, emoji="1️⃣"
    )
    async def first_button_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        print("button pressed")
        embed= await choose_Embeds("Welcome_channel", guild=interaction.guild)
        print("embed received:", embed)
        view= choose_Views("Welcome_channel", author_id=self.author_id)
        print("view received:", view)
        await interaction.response.edit_message(view=view, embed=embed)


    @discord.ui.button(label="Antispam", style=discord.ButtonStyle.primary, emoji="3️⃣")
    async def second_button_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "Du hast den Button gedrückt!", ephemeral=True
        )

    @discord.ui.button(
        label="Swear word filter", style=discord.ButtonStyle.primary, emoji="4️⃣"
    )
    async def third_button_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Its not your Button!", ephemeral=True)
            return
        await interaction.response.send_message(
            "Du hast den Button gedrückt!", ephemeral=True
        )

    @discord.ui.button(
        label="Voice Channel System", style=discord.ButtonStyle.primary, emoji="5️⃣"
    )
    async def fourth_button_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Its not your Button!", ephemeral=True)
            return
        
        await interaction.response.send_message(
            "Du hast den Button gedrückt!", ephemeral=True
        )




#await interaction.response.edit_message(embed=choose_Embeds("Welcome_channel"), view=choose_Views("Welcome_channel"))