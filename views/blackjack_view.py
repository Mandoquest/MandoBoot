import discord
from funktionen.utils import kombiniere_kartenbilder
from io import BytesIO
from funktionen.economy import gib_guthaben, ändere_guthaben
import aiohttp

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
                return (await resp.json())["cards"][0]

    def punkte(self, karten):
        punkte, asse = 0, 0
        for karte in karten:
            v = karte["value"]
            if v in ['KING', 'QUEEN', 'JACK']:
                punkte += 10
            elif v == "ACE":
                punkte += 11
                asse += 1
            else:
                punkte += int(v)
        while punkte > 21 and asse:
            punkte -= 10
            asse -= 1
        return punkte

    def kartenbilder(self, karten):
        return [k["image"] for k in karten]

    async def sende_embed(self, interaction, titel, text, karten, farbe):
        bild = kombiniere_kartenbilder(self.kartenbilder(karten))
        byte = BytesIO()
        bild.save(byte, format="PNG")
        byte.seek(0)
        file = discord.File(byte, filename="hand.png")

        embed = discord.Embed(title=titel, description=text, color=farbe)
        embed.set_image(url="attachment://hand.png")
        embed.set_footer(text=f"Spiel-ID: {self.spiel_id} | Guthaben: {gib_guthaben(self.user_id)} Münzen")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=self)

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Nicht dein Spiel!", ephemeral=True)
            return

        karte = await self.ziehe_karte()
        self.player_cards.append(karte)

        if self.punkte(self.player_cards) > 21:
            self.clear_items()
            await self.sende_embed(interaction, "💥 BUST!", "Du hast verloren.", self.player_cards, discord.Color.red())
        else:
            await self.sende_embed(interaction, "♠️ Deine Karten", f"Punkte: {self.punkte(self.player_cards)}", self.player_cards, discord.Color.green())

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.red)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Nicht dein Spiel!", ephemeral=True)
            return

        self.clear_items()
        while self.punkte(self.dealer_cards) < 17:
            self.dealer_cards.append(await self.ziehe_karte())

        sp, dp = self.punkte(self.player_cards), self.punkte(self.dealer_cards)

        if dp > 21 or sp > dp:
            ändere_guthaben(self.user_id, self.einsatz * 2)
            titel = "✅ Du gewinnst!"
            farbe = discord.Color.green()
            text = f"Du: {sp} | Dealer: {dp}"
        elif sp == dp:
            ändere_guthaben(self.user_id, self.einsatz)
            titel = "➖ Unentschieden"
            farbe = discord.Color.greyple()
            text = f"Beide: {sp} Punkte"
        else:
            titel = "❌ Verloren"
            farbe = discord.Color.red()
            text = f"Du: {sp} | Dealer: {dp}"

        await self.sende_embed(interaction, titel, text, self.player_cards, farbe)