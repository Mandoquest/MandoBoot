import json
import os

FILE_PATH = "welcome_messages.json"

def load_welcome_messages():
    if not os.path.exists(FILE_PATH):
        return {}
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_welcome_messages(welcome_messages):
    with open(FILE_PATH, "w") as f:
        json.dump(welcome_messages, f, indent=4)

def get_welcome_message(guild_id):
    data = load_welcome_messages()
    return data.get(str(guild_id))

def set_welcome_message(guild_id, message):
    data = load_welcome_messages()
    data[str(guild_id)] = message
    save_welcome_messages(data)