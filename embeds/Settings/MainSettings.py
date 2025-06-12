import discord


Mainsettings_Embed = discord.Embed(title="Settings", colour=0x5900FF)
Mainsettings_Embed.add_field(name="1️⃣: Prefix", value="Select the Prefix of the Bot", inline=False)

Mainsettings_Embed.add_field(
    name="2️⃣: Welcome Channel and Message",
    value="MandoBot sends a welcome message to the welcome chat if you want",
    inline=False,
)
Mainsettings_Embed.add_field(name="3️⃣: Antispam", value="Set up the antispam system", inline=False)

Mainsettings_Embed.add_field(
    name="4️⃣: Swear word filter",
    value="Set up the swear word filter systhem",
    inline=False,
)
Mainsettings_Embed.add_field(
    name="5️⃣: voice channel system",
    value="Set up the voice channel system",
    inline=False,
)