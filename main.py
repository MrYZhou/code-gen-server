from util.response import AppResult
from util.system import Env

app = Env.init()


@app.get("/")
def root():
    return AppResult.success("服务启动成功")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000,reload=False,workers=1,log_config=Env.log_config)
