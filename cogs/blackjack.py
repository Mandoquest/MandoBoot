from discord.ext import commands
from funktionen.economy import gib_guthaben, ändere_guthaben
from embeds.blackjack_embed import erstelle_start_embed
from views.blackjack_view import BlackjackView
import aiohttp
import uuid

aktive_spiele = {}

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def blackjack(self, ctx, einsatz: int = 100):
        user_id = ctx.author.id
        if gib_guthaben(user_id) < einsatz:
            await ctx.send("❌ Du hast nicht genug Münzen.")
            return

        ändere_guthaben(user_id, -einsatz)

        async with aiohttp.ClientSession() as session:
            async with session.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1") as resp:
                deck_id = (await resp.json())["deck_id"]
            async with session.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=3") as resp:
                cards = (await resp.json())["cards"]
                player_cards = [cards[0], cards[1]]
                dealer_cards = [cards[2]]

        spiel_id = str(uuid.uuid4())[:8]
        view = BlackjackView(user_id, deck_id, player_cards, dealer_cards, einsatz, spiel_id)
        aktive_spiele[spiel_id] = {"user_id": user_id, "view": view}

        embed, file = await erstelle_start_embed(ctx.author, spiel_id, einsatz, player_cards)
        await ctx.send(embed=embed, file=file, view=view)

    @commands.command()
    async def guthaben(self, ctx):
        stand = gib_guthaben(ctx.author.id)
        await ctx.send(f"💰 Dein Guthaben: **{stand} Münzen**")

async def setup(bot):
    await bot.add_cog(Blackjack(bot))