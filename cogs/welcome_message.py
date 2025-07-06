import discord 
from discord.ext import commands
import asyncio

class WelcomeMessage(commands.Cog):
    def __init__(self, client):
        super().__init__()
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print("WelcomeMessage cog is ready")
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        guild_id = guild.id

        from funktionen.welcome_channel_datenbank import get_welcome_message, get_welcome_channel

        msg = get_welcome_message(guild_id)
        if msg is None:
            msg = f"Welcome to the Server {member.mention}! We are glad to see you here in our community!"
        else:
            msg = msg.replace("{user}", member.mention)
            msg = msg.replace("{server}", guild.name)

        channel_id = get_welcome_channel(guild_id)
        if channel_id is None:  # Wenn kein Kanal gesetzt, dann abbrechen
            return

        channel = guild.get_channel(channel_id)
        if channel is None:  # Wenn Kanal nicht gefunden, abbrechen
            return

        await channel.send(msg)

        


    

    @commands.command()
    async def welcomemessage(self, ctx,*, message: str):
        if ctx.author.guild_permissions.administrator:
            from funktionen.welcome_channel_datenbank import set_welcome_message, get_welcome_message
            set_welcome_message(ctx.guild.id, message)
            nachricht = get_welcome_message(ctx.guild.id)
            nachricht = nachricht.replace("{user}", ctx.author.mention)
            nachricht = nachricht.replace("{server}", ctx.guild.name)
            await ctx.send(f"Willkommensnachricht gesetzt: **{nachricht}**")
        else:
            message = await ctx.send("You dont have the permission to do that, the message will be deleted in 5 seconds")
            await asyncio.sleep(5)
            await message.delete()
            await ctx.message.delete()
            

        







async def setup(client):
    await client.add_cog(WelcomeMessage(client))