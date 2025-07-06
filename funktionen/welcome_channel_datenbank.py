import json
import os

FILE_PATH = "welcome_settings.json"

def load_settings():
    if not os.path.exists(FILE_PATH):
        return {}
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(FILE_PATH, "w") as f:
        json.dump(settings, f, indent=4)

def get_welcome_enabled(guild_id):
    data = load_settings()
    guild_data = data.get(str(guild_id), {})
    return guild_data.get("welcome_enabled", False)  

def set_welcome_enabled(guild_id, enabled: bool):
    data = load_settings()
    if str(guild_id) not in data:
        data[str(guild_id)] = {}
    data[str(guild_id)]["welcome_enabled"] = enabled
    save_settings(data)

def get_welcome_message(guild_id):
    data = load_settings()
    guild_data = data.get(str(guild_id), {})
    return guild_data.get("welcome_message")

def set_welcome_message(guild_id, message):
    data = load_settings()
    if str(guild_id) not in data:
        data[str(guild_id)] = {}
    data[str(guild_id)]["welcome_message"] = message
    save_settings(data)

def get_welcome_channel(guild_id):
    data = load_settings()
    guild_data = data.get(str(guild_id), {})
    return guild_data.get("welcome_channel")

def set_welcome_channel(guild_id, channel_id):
    data = load_settings()
    if str(guild_id) not in data:
        data[str(guild_id)] = {}
    data[str(guild_id)]["welcome_channel"] = channel_id
    save_settings(data)