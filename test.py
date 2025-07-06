import discord
from discord.ext import commands
import aiohttp
import uuid
from PIL import Image
import requests
from io import BytesIO
import os
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

konten = {}  # {user_id: guthaben}
aktive_spiele = {}  # {spiel_id: {"user_id": ..., "einsatz": ..., "view": ...}}

def gib_guthaben(user_id):
    if user_id not in konten:
        konten[user_id] = 1000
    return konten[user_id]

def ändere_guthaben(user_id, betrag):
    konten[user_id] = gib_guthaben(user_id) + betrag


# 🖼️ Bild aus Karten zusammenbauen
def kombiniere_kartenbilder(image_urls):
    kartenbilder = []
    for url in image_urls:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        kartenbilder.append(img)

    gesamtbreite = sum(img.width for img in kartenbilder)
    max_hoehe = max(img.height for img in kartenbilder)

    kombi_bild = Image.new("RGBA", (gesamtbreite, max_hoehe))
    x_offset = 0
    for img in kartenbilder:
        kombi_bild.paste(img, (x_offset, 0))
        x_offset += img.width

    return kombi_bild.convert("RGB")


# 🎮 Spielklasse mit Buttons
class BlackjackView(discord.ui.View):
    def __init__(self, user_id, deck_id, player_cards, dealer_cards, einsatz, spiel_id):
        super().__init__()
        self.user_id = user_id
        self.deck_id = deck_id
        self.player_cards = player_cards
        self.dealer_cards = dealer_cards
        self.einsatz = einsatz
        self.spiel_id = spiel_id

    async def ziehe_karte(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count=1") as resp:
                data = await resp.json()
                return data['cards'][0]

    def berechne_punkte(self, karten):
        punkte = 0
        asse = 0
        for karte in karten:
            wert = karte['value']
            if wert in ['KING', 'QUEEN', 'JACK']:
                punkte += 10
            elif wert == 'ACE':
                asse += 1
                punkte += 11
            else:
                punkte += int(wert)
        while punkte > 21 and asse:
            punkte -= 10
            asse -= 1
        return punkte

    def kartenbilder(self, karten):
        return [karte["image"] for karte in karten]

    async def sende_embed(self, interaction, titel, text, kartenbilder, farbe):
        kombibild = kombiniere_kartenbilder(kartenbilder)
        kombibild.save("hand.png")
        file = discord.File("hand.png", filename="hand.png")

        embed = discord.Embed(title=titel, description=text, color=farbe)
        embed.set_image(url="attachment://hand.png")
        embed.set_footer(text=f"Spiel-ID: {self.spiel_id} | Guthaben: {gib_guthaben(self.user_id)} Münzen")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=self)

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Das ist nicht dein Spiel!", ephemeral=True)
            return

        neue_karte = await self.ziehe_karte()
        self.player_cards.append(neue_karte)
        punkte = self.berechne_punkte(self.player_cards)

        if punkte > 21:
            self.clear_items()
            await self.sende_embed(interaction, "💥 BUST!", f"Du hast {punkte} Punkte und verloren.", self.kartenbilder(self.player_cards), discord.Color.red())
        else:
            await self.sende_embed(interaction, "♠️ Blackjack – Deine Runde", f"Punkte: {punkte}", self.kartenbilder(self.player_cards), discord.Color.green())

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.red)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Das ist nicht dein Spiel!", ephemeral=True)
            return

        self.clear_items()
        while self.berechne_punkte(self.dealer_cards) < 17:
            neue_karte = await self.ziehe_karte()
            self.dealer_cards.append(neue_karte)

        spieler_punkte = self.berechne_punkte(self.player_cards)
        dealer_punkte = self.berechne_punkte(self.dealer_cards)

        if dealer_punkte > 21 or spieler_punkte > dealer_punkte:
            gewinn = self.einsatz * 2
            ändere_guthaben(self.user_id, gewinn)
            titel = "✅ Du gewinnst!"
            farbe = discord.Color.green()
            text = f"Deine Punkte: {spieler_punkte}\nDealer: {dealer_punkte}\nGewinn: {gewinn} Münzen"
        elif spieler_punkte == dealer_punkte:
            ändere_guthaben(self.user_id, self.einsatz)
            titel = "➖ Unentschieden"
            farbe = discord.Color.greyple()
            text = f"Beide haben {spieler_punkte} Punkte. Dein Einsatz wurde zurückgegeben."
        else:
            titel = "❌ Du hast verloren"
            farbe = discord.Color.red()
            text = f"Deine Punkte: {spieler_punkte}\nDealer: {dealer_punkte}"

        del aktive_spiele[self.spiel_id]
        kombibild = kombiniere_kartenbilder(self.kartenbilder(self.player_cards))
        kombibild.save("hand.png")
        file = discord.File("hand.png", filename="hand.png")

        embed = discord.Embed(title=titel, description=text, color=farbe)
        embed.set_image(url="attachment://hand.png")
        embed.add_field(name="Deine Karten", value=f"{spieler_punkte} Punkte", inline=True)
        embed.add_field(name="Dealer", value=f"{dealer_punkte} Punkte", inline=True)
        embed.set_footer(text=f"Spiel-ID: {self.spiel_id} | Guthaben: {gib_guthaben(self.user_id)} Münzen")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=self)


@bot.command()
async def blackjack(ctx, einsatz: int = 100):
    user_id = ctx.author.id
    if gib_guthaben(user_id) < einsatz:
        await ctx.send("❌ Du hast nicht genug Münzen.")
        return

    ändere_guthaben(user_id, -einsatz)

    async with aiohttp.ClientSession() as session:
        async with session.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1") as resp:
            data = await resp.json()
            deck_id = data['deck_id']

        async with session.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=3") as resp:
            data = await resp.json()
            karten = data['cards']
            player_cards = [karten[0], karten[1]]
            dealer_cards = [karten[2]]

    spiel_id = str(uuid.uuid4())[:8]
    view = BlackjackView(user_id, deck_id, player_cards, dealer_cards, einsatz, spiel_id)
    aktive_spiele[spiel_id] = {"user_id": user_id, "einsatz": einsatz, "view": view}

    punkte = view.berechne_punkte(player_cards)
    kombibild = kombiniere_kartenbilder(view.kartenbilder(player_cards))
    kombibild.save("hand.png")
    file = discord.File("hand.png", filename="hand.png")

    embed = discord.Embed(title="♠️ Blackjack gestartet", description=f"Punkte: {punkte}", color=discord.Color.green())
    embed.set_image(url="attachment://hand.png")
    embed.set_footer(text=f"Spiel-ID: {spiel_id} | Einsatz: {einsatz} | Guthaben: {gib_guthaben(user_id)} Münzen")

    await ctx.send(embed=embed, file=file, view=view)



@bot.command()
async def guthaben(ctx):
    stand = gib_guthaben(ctx.author.id)
    await ctx.send(f"💰 Dein Guthaben: **{stand} Münzen**")



@bot.command()
async def abbrechen(ctx, spiel_id: str):
    if spiel_id in aktive_spiele and aktive_spiele[spiel_id]["user_id"] == ctx.author.id:
        del aktive_spiele[spiel_id]
        await ctx.send("🚫 Spiel abgebrochen.")
    else:
        await ctx.send("❌ Spiel nicht gefunden oder du bist nicht der Besitzer.")



load_dotenv()
token = os.getenv("DISCORD_TOKEN")
bot.run(token)
