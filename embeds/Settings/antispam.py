import discord 





Antispam_embed = discord.Embed(title="**Antispam**",
                      description="The anti-spam system automatically detects spam messages. A report is then sent either to a designated channel, to a responsible individual, or, if preferred, not forwarded at all. Administrators are subsequently able to take immediate action and delete the relevant messages with the click of a button.",
                      colour=0x00f531)

Antispam_embed.add_field(name="**Currently**",
                value="Disabled",
                inline=False)
Antispam_embed.add_field(name="**Interval**",
                value="When should the bot detect spamming?\nIn messages per second\n\n3 messages per second\n\n\n**after three pings in 120s**\n\n\n**ignored channels:**\nnone",
                inline=False)