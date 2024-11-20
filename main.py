from fastapi import FastAPI
from util.response import AppResult


from util.system import Env


app = FastAPI()
Env.init(app)


@app.get("/")
def root():
    return AppResult.success("服务启动成功")


if __name__ == "__main__":
    import uvicorn

    # 输出日志

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(levelname)s - %(message)s"
            },
        },
        "handlers": {
            "file_handler": {
                "class": "logging.FileHandler",
                "filename": Env.log_path,
                "formatter": "standard",
            },
            "console_handler": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "standard",
            },
        },
        "root": {
            "handlers": ["file_handler","console_handler"],
            "level": "INFO",
        },
    }
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=8000,
        reload=False,
        workers=1,
        log_config=log_config
    )
