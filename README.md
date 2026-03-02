\# 🎮 Steam WoA Checker (ARM on Windows 游戏兼容性检测工具)



!\[Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)

!\[License](https://img.shields.io/badge/license-MIT-green.svg)

!\[Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)



\*\*Steam WoA Checker\*\* 是一款专为 \*\*Windows on ARM (骁龙 X Elite / 掌机等设备)\*\* 用户打造的轻量级开源工具。

它能一键读取你本地的 Steam 游戏库，并与 \[Works on WoA](https://www.worksonwoa.com/) 官方数据库进行极速比对，告诉你库中有哪些游戏可以完美运行，哪些存在兼容性问题。



\## ✨ 核心特性



\- \*\*🔍 智能检测\*\*：自动读取 Windows 注册表，免手动配置寻找你的 Steam 安装库。

\- \*\*⚡ 极速比对\*\*：采用内存解压与多线程异步拉取 GitHub 云端最新数据库，比对上百款游戏仅需不到 1 秒。

\- \*\*🎯 模糊匹配算法\*\*：内置 `difflib` 算法，无惧特殊字符与大小写，精准识别游戏名。

\- \*\*🎨 现代扁平化 UI\*\*：告别简陋的古典界面，采用类似 Web Dashboard 的卡片化设计与状态徽章。

\- \*\*📊 报告导出\*\*：一键导出为 `.csv` 报表，方便分享与查阅。

\- \*\*🔗 官网直达\*\*：双击任意游戏即可直达 Works on WoA 查看详细测试报告。



\## 📸 界面预览





!\[screenshot](截图链接)



\## 🚀 下载与使用



如果你不想配置 Python 环境，可以直接下载打包好的免安装版本：

1\. 前往右侧的 \[Releases 页面](../../releases)。

2\. 下载最新版本的 `SteamWoaChecker.exe`。

3\. 双击运行即可。



\## 💻 源码运行 (开发者)



本项目使用纯 Python 标准库编写，\*\*无需安装任何第三方依赖\*\*。



```bash

\# 1. 克隆仓库

git clone https://github.com/yejincheng420/SteamWoaChecker.git



\# 2. 进入目录

cd SteamWoaChecker



\# 3. 运行主程序

python main.py


将一个本地脚本转化为一个成熟、受欢迎的 GitHub 开源项目，需要经历代码整理、文档编写、打包发布这几个标准流程。

以下是一份保姆级的详细操作指南，涵盖了你所需的所有内容（包含完整的 README.md 模板和 LICENSE）：

第一步：在本地准备好项目文件夹
在你的电脑上新建一个文件夹，命名为 SteamWoaChecker，并确保里面有以下文件（之前的 5 个代码文件，加上即将创建的文档）：

code
Text
SteamWoaChecker/
 ├── main.py              # 程序入口
 ├── ui.py                # 现代扁平化界面
 ├── config.py            # 配置管理
 ├── steam_utils.py       # Steam 本地库检测
 ├── woa_utils.py         # 云端数据下载与算法
 ├── README.md            # 项目说明文档 (待创建)
 ├── LICENSE              # 开源许可证 (待创建)
 └── .gitignore           # 忽略不需要上传的文件 (待创建)
创建 .gitignore 文件（防止把你本地生成的缓存和打包文件传到 GitHub）：

code
Text
# .gitignore
__pycache__/
*.py[cod]
*$py.class
*.json
build/
dist/
*.spec
第二步：编写高逼格的 README.md
README.md 是别人进入你仓库的第一眼印象，直接决定了别人会不会给你点 Star (⭐)。请在文件夹中新建 README.md，复制以下模板并根据你的实际情况修改：

code
Markdown
# 🎮 Steam WoA Checker (ARM on Windows 游戏兼容性检测工具)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

**Steam WoA Checker** 是一款专为 **Windows on ARM (骁龙 X Elite / 掌机等设备)** 用户打造的轻量级开源工具。
它能一键读取你本地的 Steam 游戏库，并与 [Works on WoA](https://www.worksonwoa.com/) 官方数据库进行极速比对，告诉你库中有哪些游戏可以完美运行，哪些存在兼容性问题。

## ✨ 核心特性

- **🔍 智能检测**：自动读取 Windows 注册表，免手动配置寻找你的 Steam 安装库。
- **⚡ 极速比对**：采用内存解压与多线程异步拉取 GitHub 云端最新数据库，比对上百款游戏仅需不到 1 秒。
- **🎯 模糊匹配算法**：内置 `difflib` 算法，无惧特殊字符与大小写，精准识别游戏名。
- **🎨 现代扁平化 UI**：告别简陋的古典界面，采用类似 Web Dashboard 的卡片化设计与状态徽章。
- **📊 报告导出**：一键导出为 `.csv` 报表，方便分享与查阅。
- **🔗 官网直达**：双击任意游戏即可直达 Works on WoA 查看详细测试报告。

## 📸 界面预览

*(提示：在此处贴上一张你软件运行时的截图，可以将截图拖入 GitHub 编辑框自动生成链接)*
![screenshot](在这里插入你的截图链接)

## 🚀 下载与使用 (普通用户)

如果你不想配置 Python 环境，可以直接下载打包好的免安装版本：
1. 前往右侧的 [Releases 页面](../../releases)。
2. 下载最新版本的 `SteamWoaChecker.exe`。
3. 双击运行即可。

## 💻 源码运行 (开发者)

本项目使用纯 Python 标准库编写，**无需安装任何第三方依赖**。

```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/SteamWoaChecker.git

# 2. 进入目录
cd SteamWoaChecker

# 3. 运行主程序
python main.py
📦 如何打包成 EXE
如果你修改了源码并希望自己打包：

code
Bash
pip install pyinstaller
pyinstaller --noconsole --onefile --windowed --icon=icon.ico main.py -n SteamWoaChecker
打包成功后，可执行文件将生成在 dist/ 目录下。

🤝 致谢 (Acknowledgments)
感谢Linaro 以及 Works on WoA 开源社区提供的 ARM 游戏兼容性测试数据库。本项目的数据强依赖于该社区的无私贡献。

感谢广大 ARM on Windows 先驱玩家的测试反馈。

🤖 AI 辅助声明 (AI-Assisted Declaration)
本项目的核心架构重构、现代 UI 扁平化设计以及部分正则表达式的优化，均在 AI 大语言模型 (LLM) 的辅助下完成。AI 极大地提高了本开源工具的开发效率与代码可读性。

📄 许可证 (License)
本项目采用 MIT License 开源协议。你可以自由地使用、修改和分发，但请保留原作者版权声明。
