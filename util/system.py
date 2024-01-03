import importlib
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
from walrus import RateLimitException

from fastapi.responses import JSONResponse


# 路由注册
def initRouter(app: FastAPI):
    # 解析规则:server模块下面的带router字符的文件
    # modulesServer = __import__("server")
    # for root, dirs, files in os.walk(os.path.join(os.getcwd(), "server")):
    #     for file in files:
    #         if not file.find("router") == -1:
    #             file = file.replace(".py", "")
    #             parentModule = getattr(modulesServer, os.path.basename(root))
    #             module = getattr(parentModule, file)
    #             app.include_router(module.router)
    # 解析规则:放在router模块下面的文件
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), "router")):
        for file in files:
            if file.find("__init__") > -1 or file.find(".pyc") > -1:
                continue
            file = file.replace(".py", "")
            m = importlib.import_module("router." + file)
            app.include_router(m.router)


def initHttp(app: FastAPI):
    # 资源访问
    origins = [
        "http://localhost",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 限流处理器
    @app.exception_handler(RateLimitException)
    async def handle(request: Request, exc: RateLimitException):
        msg = {"code": 400, "msg": f"太快了哟!,{request.client.host}"}
        return JSONResponse(status_code=412, content=msg)


def initDataBase():
    from db import engine

    SQLModel.metadata.create_all(engine)


def initStaticDir(app):
    app.mount("/static", StaticFiles(directory="resources/static"), name="static")


def initEnv():
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("DB_HOST=127.0.0.1\n")
            f.write("DB_PORT=3306\n")
            f.write("DB_USER=root\n")
            f.write("DB_PASSWORD=root\n")
            f.write("DB_NAME=study\n")
            f.write("DB_DRIVER=mysql+pymysql\n")
            f.write("SQLMODEL_ECHO=False\n")

    if not os.path.exists("resources/static"):
        os.makedirs("resources/static")


class Init:
    @staticmethod
    def do(app: FastAPI):
        initEnv()
        initDataBase()
        initHttp(app)
        initRouter(app)
        initStaticDir(app)
