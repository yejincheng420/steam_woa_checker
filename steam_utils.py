import os
import re

def auto_detect_steam_paths(current_paths):
    """自动通过 Windows 注册表和 vdf 文件寻找所有 Steam 游戏库"""
    paths_found = set(current_paths)
    try:
        import winreg
        # 寻找主安装目录
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
        steam_path, _ = winreg.QueryValueEx(key, "InstallPath")
        paths_found.add(steam_path)
        
        # 解析 libraryfolders.vdf 寻找其他磁盘的库
        vdf_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
        if os.path.exists(vdf_path):
            with open(vdf_path, 'r', encoding='utf-8') as f:
                matches = re.finditer(r'"path"\s+"([^"]+)"', f.read())
                for match in matches:
                    clean_path = match.group(1).replace('\\\\', '\\')
                    paths_found.add(clean_path)
    except Exception:
        pass
    return list(paths_found)

def get_installed_games(paths):
    """从提供的路径列表中解析 .acf 文件，获取所有已安装游戏的名字"""
    games = set()
    # 预编译正则，提升检索速度
    name_pattern = re.compile(r'"name"\s+"([^"]+)"')
    
    for base_path in paths:
        apps_dir = os.path.join(base_path, "steamapps") if not base_path.endswith("steamapps") else base_path
        if not os.path.exists(apps_dir):
            continue
        
        for file in os.listdir(apps_dir):
            if file.startswith('appmanifest_') and file.endswith('.acf'):
                try:
                    with open(os.path.join(apps_dir, file), 'r', encoding='utf-8', errors='ignore') as f:
                        match = name_pattern.search(f.read())
                        if match:
                            games.add(match.group(1))
                except Exception:
                    pass
    return list(games)