from PyInstaller import __main__ as pyi

#打包快捷设置,避免手动输入命令

params = [
    '-F',
    # '-w',
    '--hidden-import',
    'main'
    # static目录纳入打包
    # '--add-data', 'static:static',
    # 每次打包前清楚build 和 dist目录    
    '--clean',
    # 无需用户确认
    '--noconfirm',
    'start.py'
]
# pyinstaller -F main.py
pyi.run(params)