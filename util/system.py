import importlib
import os
import sys

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from walrus import RateLimitException
from util.auth import AuthenticationMiddleware
from util.response import AppResult

from util.PPAFastAPI import PPAFastAPI


class Env:
    home_dir: str
    log_path: str
    log_config: dict

    # 路由注册
    def initRouter(app: FastAPI):
        # 解析规则:放在router模块下面的文件 (文件夹下文件)
        # 是否为已打包环境
        if getattr(sys, "frozen", False):
            base_path = os.path.join(sys._MEIPASS, "router")
        else:
            base_path = os.path.join(os.getcwd(), "router")

        # 获取当前目录下所有非目录项（即文件）
        files_in_current_dir = [
            f
            for f in os.listdir(base_path)
            if os.path.isfile(os.path.join(base_path, f))
        ]

        for file in files_in_current_dir:
            file = file.replace(".py", "")
            if file in ["__init__", ".pyc"]:
                continue
            module = importlib.import_module("router." + file)
            if hasattr(module, "router"):
                app.include_router(module.router)

    def initHttp(app: FastAPI):
        # 允许的跨域来源
        origins = [
            "http://localhost",
        ]

        # 限流处理器
        @app.exception_handler(RateLimitException)
        async def handle(request: Request, exc: RateLimitException):
            msg = {"code": 400, "msg": f"太快了哟!,{request.client.host}"}
            return AppResult.fail(412, msg)

        @app.exception_handler(HTTPException)
        async def handle2(request: Request, exc: HTTPException):
            return AppResult.fail(exc.status_code, exc.detail)

        # 添加 CORS 中间件
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # 添加认证中间件
        app.add_middleware(AuthenticationMiddleware)

    def initDataBase(app):
        PPAFastAPI.init_app(app)
        PPAFastAPI.showSql(True)

    def initStaticDir(app):
        path = Env.getPath("resources")
        app.mount("/static", StaticFiles(directory=path), name="static")

    def initEnv():
        Env.home_dir = os.path.join(os.path.expanduser("~"), "code-gen-server")
        Env.log_path = Env.getFilePath("logfile.log")
        print("资源目录:", Env.home_dir)
        print("日志文件:", Env.log_path)
        Env.getPath("resources")
        Env.log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {"format": "%(asctime)s - %(levelname)s - %(message)s"},
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
                "handlers": ["file_handler", "console_handler"],
                "level": "INFO",
            },
        }

    @staticmethod
    def init():
        Env.initEnv()
        app = FastAPI(docs_url=None)
        Env.initDataBase(app)
        Env.initHttp(app)
        Env.initRouter(app)
        Env.initStaticDir(app)
        return app

    def getPath(*path):
        path = os.path.join(os.path.expanduser("~"), "code-gen-server", *path)
        if not os.path.exists(path):
            os.makedirs(
                os.path.dirname(path) if os.path.isfile(path) else path, exist_ok=False
            )
        return path

    def getFilePath(*path):
        return os.path.join(Env.home_dir, *path)
