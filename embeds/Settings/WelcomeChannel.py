import discord


from funktionen.welcome_channel_datenbank import get_welcome_channels

async def welcome_channel(guild):
    print("Welcome channel function called with guild:", guild.id)
    channel_id = get_welcome_channels(guild.id)
    print("Channel ID retrieved:", channel_id)
    channel = guild.get_channel(channel_id)
    print("Channel object retrieved:", channel)
    if channel:
        embed = discord.Embed(title="Welcome Channel",
                      description='This is the setting for the welcome messages. If you want to change the setting, type !welkomemessage. ' \
                      'Where {user} is the username of the person who joined and {guild} is the server name.',
                      colour=0x00f531)

        embed.add_field(name="Corrent Channel",
                        value=f'The current channel is **{channel.mention}**. You can change it under "**!Settings**" and "**Welcome Chat**".',
                        inline=False)
    else:
        embed = discord.Embed(title="Welcome Channel",
                      description='This is the setting for the welcome messages. If you want to change the setting, type "**!welkomemessage**". ' \
                      'Where {user} is the username of the person who joined and {guild} is the server name.',
                      colour=0xf50000)

        embed.add_field(name="Corrent Channel",
                value='There is currently **no welcome** chat set up on this server. You can set it up under "**!Settings**" and "**Welcome Chat**".',
                inline=False)
    return embed