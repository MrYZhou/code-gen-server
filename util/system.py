import importlib
import os
import sys

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from walrus import RateLimitException

from fastapi.responses import JSONResponse

from util.PPAFastAPI import PPAFastAPI


class Env:
    # 路由注册
    def initRouter(app: FastAPI):
        # 解析规则:server模块下面的带router字符的文件 (文件夹下特定文件)
        # modulesServer = __import__("server")
        # for root, dirs, files in os.walk(os.path.join(os.getcwd(), "server")):
        #     for file in files:
        #         if not file.find("router") == -1:
        #             file = file.replace(".py", "")
        #             parentModule = getattr(modulesServer, os.path.basename(root))
        #             module = getattr(parentModule, file)
        #             app.include_router(module.router)

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

        # 解析规则:放在router模块下面的文件 (文件夹下文件)
        for file in files_in_current_dir:
            file = file.replace(".py", "")
            if file in ["__init__", ".pyc"]:
                continue
            m = importlib.import_module("router." + file)
            app.include_router(m.router)

    def initHttp(app: FastAPI):
        # 资源访问
        origins = [
            "http://localhost",
        ]

        # 限流处理器
        @app.exception_handler(RateLimitException)
        async def handle(request: Request, exc: RateLimitException):
            msg = {"code": 400, "msg": f"太快了哟!,{request.client.host}"}
            return JSONResponse(status_code=412, content=msg)

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def initDataBase(app):
        PPAFastAPI.init_app(app)
        PPAFastAPI.showSql(True)

    def initStaticDir(app):
        path = Env.getPath("resources")
        app.mount("/static", StaticFiles(directory=path), name="static")

    def initEnv():
        Env.getPath("resources")

    @staticmethod
    def init(app: FastAPI):
        Env.initEnv()
        Env.initDataBase(app)
        Env.initHttp(app)
        Env.initRouter(app)
        Env.initStaticDir(app)

    def getPath(*path):
        path = os.path.join(os.path.expanduser("~"), "code-gen-server", *path)
        if not os.path.exists(path):
            os.makedirs(
                os.path.dirname(path) if os.path.isfile(path) else path, exist_ok=False
            )
        return path
