import discord
from io import BytesIO
from funktionen.economy import gib_guthaben
from funktionen.utils import kombiniere_kartenbilder

def berechne_punkte(karten):
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

async def erstelle_start_embed(user, spiel_id, einsatz, karten):
    kartenbilder = [k["image"] for k in karten]
    bild = kombiniere_kartenbilder(kartenbilder)
    byte = BytesIO()
    bild.save(byte, format="PNG")
    byte.seek(0)
    file = discord.File(byte, filename="hand.png")

    embed = discord.Embed(
        title="♠️ Blackjack gestartet",
        description=f"Punkte: {berechne_punkte(karten)}",
        color=discord.Color.green()
    )
    embed.set_image(url="attachment://hand.png")
    embed.set_footer(text=f"Spiel-ID: {spiel_id} | Einsatz: {einsatz} | Guthaben: {gib_guthaben(user.id)} Münzen")

    return embed, file