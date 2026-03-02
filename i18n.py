import config

# 获取默认或保存的语言 (zh 或 en)
cfg = config.load_config()
CURRENT_LANG = cfg.get("language", "zh")

def set_lang(lang):
    global CURRENT_LANG
    CURRENT_LANG = lang

# 英文翻译映射字典
DICT_EN = {
    "🎮 ARM on Windows 游戏兼容性检测": "🎮 ARM on Windows Game Compatibility Checker",
    "读取 Steam 与 Epic 本地库并与 works-on-woa.com 数据库进行比对": "Scan local Steam & Epic libraries and check against works-on-woa.com",
    "📂 Steam 游戏库路径 (Epic 将自动全盘扫描，无需配置)": "📂 Steam Library Paths (Epic is scanned automatically)",
    "🔍 自动检测 Steam 库": "🔍 Auto Detect",
    "➕ 手动添加": "➕ Add Path",
    "🗑️ 清空": "🗑️ Clear",
    "🚀 开始检测本地游戏": "🚀 Check Local Games",
    "🔍 手动查询单款": "🔍 Manual Query",
    "🔄 更新云端数据库": "🔄 Update Cloud DB",
    "正在初始化系统组件...": "Initializing system components...",
    "🎮 本地游戏名称": "🎮 Local Game Name",
    "⚡ ARM 兼容性状态": "⚡ ARM Compatibility Status",
    "🎯 匹配详情": "🎯 Match Details",
    "💡 提示: 双击列表中的游戏可跳转至官网查看详情。点击表头进行排序。": "💡 Tip: Double-click a game to view details on the website. Click headers to sort.",
    "💾 导出报告为 CSV": "💾 Export to CSV",
    
    # 弹窗提示与短语
    "警告": "Warning",
    "提示": "Info",
    "成功": "Success",
    "查询结果": "Query Result",
    "本地数据库为空，请更新！": "Local DB is empty, please update!",
    "本地数据库为空，请先点击【更新云端数据库】！": "Local DB is empty, click [Update Cloud DB] first!",
    "请先添加 Steam 库文件夹！": "Please add a Steam library folder first!",
    "未找到任何已安装的 Steam 或 Epic 游戏，请检查库路径。": "No installed Steam or Epic games found. Check your paths.",
    "没有可导出的数据。": "No data to export.",
    "报告已导出！": "Report exported successfully!",
    "手动查询游戏": "Manual Game Query",
    "请输入要查询的游戏名称：\n(支持中英文，内置模糊匹配算法)": "Enter game name to query:\n(Supports fuzzy matching algorithm)",
    "[手动查询]": "[Manual Query]",
    "未收录": "Not Listed",
    
    # 动态参数字符串 (使用 {} 占位符)
    "📦 已加载本地数据库 | 共收录 {count} 款游戏 | 最后更新: {date}": "📦 Local DB loaded | {count} games | Last update: {date}",
    "自动检测到 {count} 个 Steam 游戏库路径！": "Auto-detected {count} Steam library paths!",
    "⏳ 正在从 GitHub 拉取最新数据，这可能需要几秒钟...": "⏳ Pulling latest data from GitHub, this may take a few seconds...",
    "✅ 更新成功！共收录 {count} 款游戏 | 最后更新: {date}": "✅ Update successful! {count} games stored | Last update: {date}",
    "❌ 更新失败: {err}": "❌ Update failed: {err}",
    "🔍 正在极速比对 {count} 款游戏...": "🔍 Checking {count} games at high speed...",
    "✅ 比对完成！您的电脑中共检测了 {count} 款游戏 (包含 Steam 与 Epic)。": "✅ Check complete! Detected {count} games (Steam & Epic) on your PC.",
    "🎮 查询内容: {name}\n\n⚡ 兼容性状态: {status}\n🎯 匹配详情: {match}": "🎮 Query: {name}\n\n⚡ Status: {status}\n🎯 Match: {match}",
    "  [手动查询] {name}": "  [Manual Query] {name}",
    
    # 数据算法匹配词
    "Unknown (数据库未收录)": "Unknown (Not in database)",
    "未找到": "Not Found",
    "🎯 精确匹配": "🎯 Exact Match",
    "🔎 模糊匹配 ({name})": "🔎 Fuzzy Match ({name})"
}

def tr(text):
    """翻译函数，如果是英文环境则去字典找对应的翻译，否则原样返回"""
    if CURRENT_LANG == "en":
        return DICT_EN.get(text, text)
    return text