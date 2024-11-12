from PyInstaller import __main__ as pyi

# 打包快捷设置,避免手动输入命令

params = [
    "-F",  #  是否单文件
    # "-w",  # 是否隐藏控制台-w代表无,默认有
    "--hidden-import=fastapi.templating",
    "--hidden-import=nanoid",
    "--hidden-import=faker",
    # 额外目录纳入打包
    "--add-data=util;util",
    "--add-data=router;router",
    "--add-data=server;server",
    "--add-data=models;models",
    # 指定输出目录
    "--distpath=build",
    # 无需用户确认
    "--noconfirm",
    "-n=codegen",
    "main.py",
]
pyi.run(params)
