from PyInstaller import __main__ as pyi

# 打包快捷设置,避免手动输入命令

params = [
    # "-F", #  是否单文件
    # '-w', #是否隐藏控制台
    "--hidden-import=aiomysql",
    "--hidden-import=nanoid",
    "--hidden-import=sqlmodel",
    "--hidden-import=pysqlite2",
    "--hidden-import=MySQLdb",
    "--hidden-import=laorm.core.stream",
    "--hidden-import=fastapi.templating",
    
    # 额外目录纳入打包
    '--add-data', 'util;util',
    '--add-data', 'router;router',
    '--add-data', 'server;server',
    # 每次打包前清楚build 和 dist目录
    # "--clean",
    # 无需用户确认
    "--noconfirm",
    "main.py",
]
pyi.run(params)
