import os
import json

CONFIG_FILE = "steam_woa_config.json"

def load_config():
    """读取本地配置文件"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"steam_paths":[]}

def save_config(paths):
    """保存 Steam 库路径到本地"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump({"steam_paths": paths}, f, indent=4)