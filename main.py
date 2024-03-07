from fastapi import FastAPI
from util.response import AppResult


from util.system import Env


app = FastAPI()
Env.init(app)


@app.get("/")
def root():
    return AppResult.success("code-gen-server")


if __name__ == "__main__":
    import uvicorn

    # 输出无日志
    log_path = Env.getPath("logfile.log")

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "file_handler": {
                "class": "logging.FileHandler",
                "filename": log_path,
            },
        },
        "root": {
            "handlers": ["file_handler"],
            "level": "INFO",
        },
    }
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=8000,
        reload=False,
        workers=1,
        log_config=log_config,
    )
