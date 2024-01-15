import os
from PyInstaller import __main__ as pyi

# 打包快捷设置,避免手动输入命令

params = [
    # "-F",
    # '-w',
    "--hidden-import=aiomysql",
    # static目录纳入打包
    # '--collect-submodules', 'util',
    # '--collect-submodules', 'router',
    # '--collect-submodules', 'server',
    # '--add-data', 'util;util',
    # '--add-data', 'router;router',
    # '--add-data', 'server;server',
    # 每次打包前清楚build 和 dist目录
    # "--clean",
    # 无需用户确认
    "--noconfirm",
    "main.py",
]
pyi.run(params)
