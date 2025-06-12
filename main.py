import discord
import os
from discord.ext import commands
import asyncio
from dotenv import load_dotenv



intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())



@client.event
async def on_ready():
    print("Bot ist fertig")

@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await client.load_extension(f'cogs.{filename[:-3]}')
                print(f'Cog {filename} geladen.')
            except Exception as e:
                print(f'Fehler beim Laden von {filename}: {e}')


load_dotenv()
token = os.getenv("DISCORD_TOKEN")

async def main():
    async with client:
        await load()
        await client.start(token)


asyncio.run(main())