import discord 

async def choose_Embeds(name, **kwargs):
    if name == "Main":
        from embeds.Settings.MainSettings import Mainsettings_Embed
        print("Mainsettings_Embed loaded")
        return Mainsettings_Embed
    

    elif name == "Welcome_channel":
        from embeds.Settings.WelcomeChannel import welcome_channel
        guild = kwargs.get("guild")
        if guild is None:
            raise ValueError("Guild is required for 'Welcome_channel' embed.")
        print("Welcome_channel embed loaded")
        return await welcome_channel(guild)
