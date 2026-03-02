import os
import json

def get_installed_epic_games():
    """
    自动读取 Windows 系统下的 Epic 游戏清单文件 (Manifests)，
    获取所有已安装的 Epic 游戏名称。完全自动化，无需手动选择路径。
    """
    games = set()
    # 动态获取 ProgramData 环境变量，防止有些用户的系统不在 C 盘
    program_data = os.environ.get('PROGRAMDATA', r'C:\ProgramData')
    manifest_dir = os.path.join(program_data, 'Epic', 'EpicGamesLauncher', 'Data', 'Manifests')
    
    if not os.path.exists(manifest_dir):
        return list(games)
    
    for filename in os.listdir(manifest_dir):
        if filename.endswith(".item"):
            filepath = os.path.join(manifest_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    data = json.load(f)
                    game_name = data.get("DisplayName")
                    # 过滤掉 Epic 启动器本身和无用组件
                    if game_name and game_name not in ["Epic Games Launcher", "Unreal Engine"]:
                        games.add(game_name)
            except Exception:
                pass
                
    return list(games)