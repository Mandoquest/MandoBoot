import json
import os


FILE_PATH = "status.json"



def load_config():
    if not os.path.isfile(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump({}, f)
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_config(config):
    with open(FILE_PATH, "w") as f:
        json.dump(config, f, indent=4)

def get_welcome_status(guild_id: int) -> bool:
    config = load_config()
    return config.get(str(guild_id), {}).get("welcome_enabled", True)  # Standard: True

def toggle_welcome_status(guild_id: int) -> bool:
    config = load_config()
    guild_id_str = str(guild_id)
    if guild_id_str not in config:
        config[guild_id_str] = {}
    current = config[guild_id_str].get("welcome_enabled", True)
    config[guild_id_str]["welcome_enabled"] = not current
    save_config(config)
    return not current