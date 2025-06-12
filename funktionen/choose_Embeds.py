import discord 

def choose_Embeds(name):
    if name == "Main":
        from embeds.Settings.MainSettings import Mainsettings_Embed
        return Mainsettings_Embed
    elif name == "Prefix":
        from embeds.Settings.Prefix import Prefix_Embed
        return Prefix_Embed
    elif name == "Welcome_channel":
        from embeds.Settings.WelcomeChannel import WelcomeChannel
        return WelcomeChannel