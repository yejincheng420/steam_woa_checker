import os
import re
import json
import urllib.request
import zipfile
import io
import difflib

DB_FILE = "woa_database.json"

def load_database():
    """加载本地缓存的游戏兼容性数据库"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("games", {}), data.get("last_update", "未知")
        except Exception:
            pass
    return {}, "从未更新"

def save_database(games_dict, last_update):
    """将从云端拉取的数据保存在本地"""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump({"last_update": last_update, "games": games_dict}, f, indent=4, ensure_ascii=False)

def fetch_latest_database():
    """从 GitHub 直接下载 ZIP 并全内存解析，速度极快"""
    zip_url = "https://github.com/Linaro/works-on-woa/archive/refs/heads/main.zip"
    req = urllib.request.Request(zip_url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req, timeout=30) as response:
        zip_data = response.read()

    new_db = {}
    # 提前编译正则，极大提升循环内解析速度
    name_re = re.compile(r'^name:\s*["\']?(.*?)["\']?\s*$', re.MULTILINE)
    status_re = re.compile(r'^(?:display_result|compatibility):\s*["\']?(.*?)["\']?\s*$', re.MULTILINE | re.IGNORECASE)

    with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
        for info in z.infolist():
            if info.filename.endswith('.md') and ('src/content/games/' in info.filename or 'src/content/applications/' in info.filename):
                content = z.read(info.filename).decode('utf-8', errors='ignore')
                parts = content.split('---')
                if len(parts) >= 3:
                    yaml_text = parts[1]
                    name_match = name_re.search(yaml_text)
                    status_match = status_re.search(yaml_text)
                    
                    if name_match and status_match:
                        game_name = name_match.group(1).strip()
                        game_status = status_match.group(1).strip().capitalize()
                        new_db[game_name] = game_status
                        
    if not new_db:
        raise ValueError("未从压缩包中解析到数据，可能是 GitHub 仓库结构改变。")
    return new_db

def normalize_string(s):
    """字符串标准化清洗：去商标、转小写、去符号"""
    if not s: return ""
    s = s.replace("™", "").replace("®", "").replace("©", "")
    clean = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return clean if clean else s.lower()

def match_local_games(local_games, woa_data):
    """极速比对本地游戏与数据库，返回详细结果列表"""
    results =[]
    db_normalized_map = {normalize_string(k): k for k in woa_data.keys()}
    db_norm_keys = list(db_normalized_map.keys())

    for game in local_games:
        norm_local = normalize_string(game)
        status = "Unknown (数据库未收录)"
        match_type = "未找到"
        original_name = game
        tag = "unknown"

        if norm_local in db_normalized_map:
            original_name = db_normalized_map[norm_local]
            status = woa_data[original_name]
            match_type = "🎯 精确匹配"
        else:
            matches = difflib.get_close_matches(norm_local, db_norm_keys, n=1, cutoff=0.85)
            if matches:
                original_name = db_normalized_map[matches[0]]
                status = woa_data[original_name]
                match_type = f"🔎 模糊匹配 ({original_name})"

        # 匹配颜色标签
        status_lower = status.lower()
        if "perfect" in status_lower: tag = "perfect"
        elif "playable" in status_lower: tag = "playable"
        elif "runs" in status_lower: tag = "runs"
        elif "unplayable" in status_lower or "fail" in status_lower: tag = "unplayable"

        results.append({
            "local_name": game,
            "status": status,
            "match_type": match_type,
            "tag": tag,
            "db_name": original_name
        })
        
    return results