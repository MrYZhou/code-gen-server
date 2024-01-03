import uvicorn
# 使用idea和打包使用,reload=False否则打包exe会无限reload。
# vscode默认可以在main.py按f5启动

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=False, workers=1)

