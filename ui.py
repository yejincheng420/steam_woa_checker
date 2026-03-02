import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import threading
import csv
import webbrowser
import re
from datetime import datetime

import config
import steam_utils
import epic_utils
import woa_utils
from i18n import tr, set_lang, CURRENT_LANG  # <--- 导入 i18n

class SteamWoaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steam/Epic WoA Checker V5.4")
        self.root.geometry("1000x750")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'1000x750+{int((screen_width - 1000) / 2)}+{int((screen_height - 750) / 2)}')
        
        self.cfg = config.load_config()
        self.steam_paths = self.cfg.get("steam_paths",[])
        self.woa_data, self.last_update = woa_utils.load_database()
        
        self.setup_modern_styles()
        self.setup_ui()
        
        if self.woa_data:
            self.status_var.set(tr("📦 已加载本地数据库 | 共收录 {count} 款游戏 | 最后更新: {date}").format(count=len(self.woa_data), date=self.last_update))
        else:
            self.update_database()
            
        if not self.steam_paths:
            self.auto_detect_steam()

    def setup_modern_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.bg_color = "#F3F4F6"
        self.card_bg = "#FFFFFF"
        self.text_main = "#1F2937"
        self.text_muted = "#6B7280"
        self.primary_color = "#2563EB"
        self.primary_hover = "#1D4ED8"
        self.success_color = "#10B981"
        self.success_hover = "#059669"
        
        self.root.configure(bg=self.bg_color)
        self.style.configure('Main.TFrame', background=self.bg_color)
        self.style.configure('Card.TFrame', background=self.card_bg)
        self.style.configure('Title.TLabel', background=self.bg_color, foreground=self.text_main, font=("Microsoft YaHei", 18, "bold"))
        self.style.configure('Subtitle.TLabel', background=self.bg_color, foreground=self.text_muted, font=("Microsoft YaHei", 10))
        self.style.configure('CardTitle.TLabel', background=self.card_bg, foreground=self.text_main, font=("Microsoft YaHei", 11, "bold"))
        self.style.configure('Primary.TButton', font=("Microsoft YaHei", 10, "bold"), background=self.primary_color, foreground="white", borderwidth=0, padding=6, focuscolor="none")
        self.style.map('Primary.TButton', background=[('active', self.primary_hover)])
        self.style.configure('Success.TButton', font=("Microsoft YaHei", 10, "bold"), background=self.success_color, foreground="white", borderwidth=0, padding=6, focuscolor="none")
        self.style.map('Success.TButton', background=[('active', self.success_hover)])
        self.style.configure('Secondary.TButton', font=("Microsoft YaHei", 10), background="#E5E7EB", foreground=self.text_main, borderwidth=0, padding=6, focuscolor="none")
        self.style.map('Secondary.TButton', background=[('active', '#D1D5DB')])
        self.style.configure('Treeview', font=("Microsoft YaHei", 10), rowheight=38, borderwidth=0, background=self.card_bg, fieldbackground=self.card_bg, foreground=self.text_main)
        self.style.configure('Treeview.Heading', font=("Microsoft YaHei", 10, "bold"), background="#F9FAFB", foreground=self.text_muted, borderwidth=0, padding=8)
        self.style.map('Treeview.Heading', background=[('active', '#F3F4F6')])
        self.style.map('Treeview', background=[('selected', '#DBEAFE')], foreground=[('selected', '#1E40AF')])

    def setup_ui(self):
        # 每次重建 UI 时定义主容器 (便于热切换语言)
        self.main_container = ttk.Frame(self.root, style='Main.TFrame')
        self.main_container.pack(fill="both", expand=True, padx=25, pady=20)

        # 顶部标题区
        header_frame = ttk.Frame(self.main_container, style='Main.TFrame')
        header_frame.pack(fill="x", pady=(0, 20))
        
        # 切换语言按钮
        btn_lang = ttk.Button(header_frame, text="🌐 English / 中文", style='Secondary.TButton', command=self.switch_language)
        btn_lang.pack(side="right", anchor="n")
        
        ttk.Label(header_frame, text=tr("🎮 ARM on Windows 游戏兼容性检测"), style='Title.TLabel').pack(anchor="w")
        ttk.Label(header_frame, text=tr("读取 Steam 与 Epic 本地库并与 works-on-woa.com 数据库进行比对"), style='Subtitle.TLabel').pack(anchor="w", pady=(2, 0))

        # 路径管理卡片
        path_card = tk.Frame(self.main_container, bg=self.card_bg, bd=0, highlightthickness=1, highlightbackground="#E5E7EB")
        path_card.pack(fill="x", pady=(0, 20))
        path_inner = ttk.Frame(path_card, style='Card.TFrame')
        path_inner.pack(fill="both", expand=True, padx=15, pady=15)
        path_left = ttk.Frame(path_inner, style='Card.TFrame')
        path_left.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        ttk.Label(path_left, text=tr("📂 Steam 游戏库路径 (Epic 将自动全盘扫描，无需配置)"), style='CardTitle.TLabel').pack(anchor="w", pady=(0, 8))
        self.path_listbox = tk.Listbox(path_left, height=3, bg="#F9FAFB", fg=self.text_main, font=("Microsoft YaHei", 10), bd=0, highlightthickness=1, highlightbackground="#E5E7EB", selectbackground="#DBEAFE", selectforeground="#1E40AF", activestyle="none")
        self.path_listbox.pack(fill="both", expand=True)
        self.refresh_path_listbox()

        path_right = ttk.Frame(path_inner, style='Card.TFrame')
        path_right.pack(side="right", fill="y", pady=(25, 0))
        ttk.Button(path_right, text=tr("🔍 自动检测 Steam 库"), style='Secondary.TButton', command=self.auto_detect_steam).pack(fill="x", pady=(0, 8))
        btn_row = ttk.Frame(path_right, style='Card.TFrame')
        btn_row.pack(fill="x")
        ttk.Button(btn_row, text=tr("➕ 手动添加"), style='Secondary.TButton', command=self.add_path).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(btn_row, text=tr("🗑️ 清空"), style='Secondary.TButton', command=self.clear_paths).pack(side="right", expand=True, fill="x")

        # 操作区
        action_frame = ttk.Frame(self.main_container, style='Main.TFrame')
        action_frame.pack(fill="x", pady=(0, 10))
        self.btn_check = ttk.Button(action_frame, text=tr("🚀 开始检测本地游戏"), style='Primary.TButton', command=self.run_check)
        self.btn_check.pack(side="right", padx=(10, 0))
        self.btn_manual = ttk.Button(action_frame, text=tr("🔍 手动查询单款"), style='Success.TButton', command=self.manual_query)
        self.btn_manual.pack(side="right", padx=(10, 0))
        self.btn_update = ttk.Button(action_frame, text=tr("🔄 更新云端数据库"), style='Secondary.TButton', command=self.update_database)
        self.btn_update.pack(side="right")

        self.status_var = tk.StringVar(value=tr("正在初始化系统组件..."))
        status_label = ttk.Label(action_frame, textvariable=self.status_var, background=self.bg_color, foreground=self.primary_color, font=("Microsoft YaHei", 10, "bold"))
        status_label.pack(side="left", fill="y", pady=5)

        # 表格区
        table_card = tk.Frame(self.main_container, bg=self.card_bg, bd=0, highlightthickness=1, highlightbackground="#E5E7EB")
        table_card.pack(fill="both", expand=True, pady=(0, 15))
        cols = ("Game", "Status", "Match")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings", selectmode="browse")
        
        self.tree.heading("Game", text=tr("🎮 本地游戏名称"), command=lambda: self.sort_tree("Game", False))
        self.tree.heading("Status", text=tr("⚡ ARM 兼容性状态"), command=lambda: self.sort_tree("Status", False))
        self.tree.heading("Match", text=tr("🎯 匹配详情"), command=lambda: self.sort_tree("Match", False))
        self.tree.column("Game", width=400, anchor="w")
        self.tree.column("Status", width=200, anchor="center")
        self.tree.column("Match", width=250, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        
        self.tree.bind("<Double-1>", self.open_website)

        self.tree.tag_configure("perfect", background="#D1FAE5", foreground="#065F46")
        self.tree.tag_configure("playable", background="#FEF3C7", foreground="#92400E")
        self.tree.tag_configure("runs", background="#DBEAFE", foreground="#1E40AF")
        self.tree.tag_configure("unplayable", background="#FEE2E2", foreground="#991B1B")
        self.tree.tag_configure("unknown", background="#F3F4F6", foreground="#4B5563")

        # 底部提示
        bottom_frame = ttk.Frame(self.main_container, style='Main.TFrame')
        bottom_frame.pack(fill="x")
        ttk.Label(bottom_frame, text=tr("💡 提示: 双击列表中的游戏可跳转至官网查看详情。点击表头进行排序。"), style='Subtitle.TLabel').pack(side="left")
        ttk.Button(bottom_frame, text=tr("💾 导出报告为 CSV"), style='Secondary.TButton', command=self.export_csv).pack(side="right")

    # ---------------- 语言切换逻辑 ----------------
    def switch_language(self):
        """实时无缝切换界面语言"""
        import i18n
        new_lang = "en" if i18n.CURRENT_LANG == "zh" else "zh"
        set_lang(new_lang)
        self.cfg["language"] = new_lang
        config.save_config(self.cfg)
        
        # 销毁旧界面，重新渲染新界面
        self.main_container.destroy()
        self.setup_ui()
        
        # 恢复状态栏显示
        if self.woa_data:
            self.status_var.set(tr("📦 已加载本地数据库 | 共收录 {count} 款游戏 | 最后更新: {date}").format(count=len(self.woa_data), date=self.last_update))
        
        # 自动触发一次检测刷新表格内容
        if self.steam_paths:
            self.run_check()

    # ---------------- 功能逻辑部分 ----------------
    def manual_query(self):
        if not self.woa_data:
            return messagebox.showwarning(tr("警告"), tr("本地数据库为空，请先点击【更新云端数据库】！"))
        game_name = simpledialog.askstring(tr("手动查询游戏"), tr("请输入要查询的游戏名称：\n(支持中英文，内置模糊匹配算法)"), parent=self.root)
        if not game_name or not game_name.strip(): return
            
        results = woa_utils.match_local_games([game_name.strip()], self.woa_data)
        if results:
            res = results[0]
            tag_manual = tr("[手动查询]")
            self.tree.insert("", "0", values=(f"  {tag_manual} {res['local_name']}", res["status"], res["match_type"]), tags=(res["tag"],))
            msg = tr("🎮 查询内容: {name}\n\n⚡ 兼容性状态: {status}\n🎯 匹配详情: {match}").format(name=res['local_name'], status=res['status'], match=res['match_type'])
            messagebox.showinfo(tr("查询结果"), msg)

    def refresh_path_listbox(self):
        self.path_listbox.delete(0, "end")
        for p in self.steam_paths: self.path_listbox.insert("end", f"  {p}")

    def auto_detect_steam(self):
        new_paths = steam_utils.auto_detect_steam_paths(self.steam_paths)
        if len(new_paths) > len(self.steam_paths):
            self.steam_paths = new_paths
            self.refresh_path_listbox()
            self.cfg["steam_paths"] = self.steam_paths
            config.save_config(self.cfg)
            messagebox.showinfo(tr("成功"), tr("自动检测到 {count} 个 Steam 游戏库路径！").format(count=len(self.steam_paths)))

    def add_path(self):
        path = filedialog.askdirectory()
        if path and path not in self.steam_paths:
            self.steam_paths.append(path)
            self.refresh_path_listbox()
            self.cfg["steam_paths"] = self.steam_paths
            config.save_config(self.cfg)

    def clear_paths(self):
        self.steam_paths =[]
        self.refresh_path_listbox()
        self.cfg["steam_paths"] = self.steam_paths
        config.save_config(self.cfg)

    def sort_tree(self, col, reverse):
        l =[(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        self.tree.heading(col, command=lambda: self.sort_tree(col, not reverse))

    def open_website(self, event):
        selected = self.tree.selection()
        if not selected: return
        item_data = self.tree.item(selected[0])['values']
        if tr("未收录") in item_data[1]: return
        
        match_info = item_data[2]
        original_name = item_data[0].replace(tr("[手动查询]"), "").strip()
        m = re.search(r'\((.*?)\)', match_info)
        if m: original_name = m.group(1)
            
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', original_name).strip('-').lower()
        webbrowser.open(f"https://www.worksonwoa.com/games/{slug}/")

    def export_csv(self):
        items = self.tree.get_children()
        if not items: return messagebox.showinfo(tr("提示"), tr("没有可导出的数据。"))
            
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")], initialfile="WoA_Report.csv")
        if path:
            with open(path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([tr("🎮 本地游戏名称"), tr("⚡ ARM 兼容性状态"), tr("🎯 匹配详情")])
                for item in items: writer.writerow(self.tree.item(item)['values'])
            messagebox.showinfo(tr("成功"), tr("报告已导出！"))

    def update_database(self):
        self.btn_update.config(state="disabled")
        self.btn_check.config(state="disabled")
        self.btn_manual.config(state="disabled")
        self.status_var.set(tr("⏳ 正在从 GitHub 拉取最新数据，这可能需要几秒钟..."))
        threading.Thread(target=self._thread_update_db, daemon=True).start()

    def _thread_update_db(self):
        try:
            self.woa_data = woa_utils.fetch_latest_database()
            self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            woa_utils.save_database(self.woa_data, self.last_update)
            msg = tr("✅ 更新成功！共收录 {count} 款游戏 | 最后更新: {date}").format(count=len(self.woa_data), date=self.last_update)
            self.root.after(0, lambda m=msg: self.status_var.set(m))
        except Exception as e:
            self.root.after(0, lambda err=str(e): self.status_var.set(tr("❌ 更新失败: {err}").format(err=err)))
        finally:
            self.root.after(0, lambda: self.btn_update.config(state="normal"))
            self.root.after(0, lambda: self.btn_check.config(state="normal"))
            self.root.after(0, lambda: self.btn_manual.config(state="normal"))

    def run_check(self):
        if not self.woa_data: return messagebox.showwarning(tr("警告"), tr("本地数据库为空，请更新！"))

        self.tree.delete(*self.tree.get_children())
        steam_games = steam_utils.get_installed_games(self.steam_paths) if self.steam_paths else[]
        epic_games = epic_utils.get_installed_epic_games()
        local_games = list(set(steam_games + epic_games))
        
        if not local_games: return messagebox.showinfo(tr("提示"), tr("未找到任何已安装的 Steam 或 Epic 游戏，请检查库路径。"))
            
        self.status_var.set(tr("🔍 正在极速比对 {count} 款游戏...").format(count=len(local_games)))
        self.root.update_idletasks()
        
        results = woa_utils.match_local_games(local_games, self.woa_data)
        for res in results:
            self.tree.insert("", "end", values=(f"  {res['local_name']}", res["status"], res["match_type"]), tags=(res["tag"],))
            
        self.status_var.set(tr("✅ 比对完成！您的电脑中共检测了 {count} 款游戏 (包含 Steam 与 Epic)。").format(count=len(local_games)))