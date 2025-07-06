import discord
from discord.ext import commands
import asyncio

from funktionen.choose_Embeds import choose_Embeds
from funktionen.choose_Views import choose_Views
from views.Settings.MainButtons import MainButtons
from embeds.Settings.WelcomeChannel import welcome_channel

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Settings cog is ready")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        if ctx.author.guild_permissions.administrator:
            embed= await choose_Embeds("Main", guild=ctx.guild)
            view = choose_Views("Main", author_id=ctx.author.id)
            await ctx.send(embed=embed, view=view)
        else:
            message = await ctx.send("you dont have the permission, the message will be deleted in 5 seconds")
            await asyncio.sleep(5)
            await message.delete()
            await ctx.message.delete()

async def setup(client):
    await client.add_cog(Settings(client))