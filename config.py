import os
import json

CONFIG_FILE = "steam_woa_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"steam_paths":[], "language": "zh"}

def save_config(cfg_dict):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(cfg_dict, f, indent=4)