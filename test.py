import discord
from discord.ext import commands
from discord.ui import View, Button
import asyncio
import os
from dotenv import load_dotenv


prefix = "!"

intents = discord.Intents.default()
intents.message_content = True  # Wichtig!
bot = commands.Bot(command_prefix= prefix, intents=intents)


@bot.command()
async def delete(ctx):
    async for message in ctx.channel.history(limit=100):
        await message.delete()
        await asyncio.sleep(0.3)


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
        self.add_item(ChannelSelect())  # Erste Zeile: Menü

    @discord.ui.button(label="Zurück", style=discord.ButtonStyle.primary, emoji="◀️", row=1)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Nicht dein Button!", ephemeral=True)
            return
        await interaction.response.send_message("Zurück zum Hauptmenü.", ephemeral=True)
        
        
@bot.command()
async def test(ctx):
    view = WelcomeChannel_View(ctx.author.id)
    await ctx.send("Wähle einen Kanal für Willkommensnachrichten:", view=view)



load_dotenv()
token = os.getenv("DISCORD_TOKEN")
bot.run(token)
