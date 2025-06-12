import discord 


Prefix_Embed=discord.Embed(title="Prefix",
                      description="The Prefix is the command that you use to interact with the bot. You can change it to whatever you like, but make sure it's not already in use by another bot or command.",
                      colour=0x4900f5)
Prefix_Embed.add_field(name="Current Prefix", value='"!"', inline=False)
                