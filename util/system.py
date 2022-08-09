import os
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from util.base import routeList
from db import engine
import importlib
from sqlmodel import create_engine,SQLModel
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
            m = importlib.import_module('router.'+file)
            app.include_router(m.router)

    # 解析规则:在模板里面手动注册的方式,需要自行导包
    for route in routeList:
        app.include_router(route)


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

def initDataBase():
    SQLModel.metadata.create_all(engine)

class Init:
    def do(app: FastAPI):
        initHttp(app)
        initRouter(app)
        initDataBase()
