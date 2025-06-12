import discord
from discord.ext import commands
import asyncio

from funktionen.choose_Embeds import choose_Embeds
from funktionen.choose_Views import choose_Views
from views.Settings.MainButtons import MainButtons

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Settings cog is ready")

    @commands.command()
    async def settings(self, ctx):
        if ctx.author.guild_permissions.administrator:
            await ctx.send(embed=choose_Embeds("Main",), view=choose_Views("Main", author_id=ctx.author.id))
        else:
            message = await ctx.send("you dont have the permission, the message will be deleted in 5 seconds")
            await asyncio.sleep(5)
            await message.delete()
            await ctx.message.delete()



async def setup(client):
    await client.add_cog(Settings(client))