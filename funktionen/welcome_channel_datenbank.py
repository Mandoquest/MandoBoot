import json
import os

FILE_PATH = "welcome_chanel.json"


def load_channels():
    if not os.path.exists(FILE_PATH):
        return {}
    with open(FILE_PATH, "r") as f:
        return json.load(f)


def save_channels(welcome_channels):
    with open(FILE_PATH, "w") as f:
        json.dump(welcome_channels, f, indent=4)


def get_welcome_channels(guild_id):
    data = load_channels()
    return data.get(str(guild_id))

def set_welcome_channel(guild_id, channel_id):
    data = load_channels()
    data[str(guild_id)] = channel_id
    save_channels(data)
