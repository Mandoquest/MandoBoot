import discord

def choose_Views(name, **kwargs):
    if name == "Main":
        from views.Settings.MainButtons import MainButtons
        print("Main Buttons View loaded")
        return MainButtons(**kwargs)
    
    elif name == "Welcome_channel":
        from views.Settings.WelcomeChannel import WelcomeChannel_View
        print("Welcome Channel View loaded")
        return WelcomeChannel_View(**kwargs)
