import os
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from util.base import routeList
from util import router

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
    modules = __import__("router")
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), "router")):
        for file in files:
            if file.find("__init__") > -1 or file.find(".pyc") > -1:
                continue
            file = file.replace(".py", "")
            module = getattr(modules, file)
            app.include_router(module.router)

    # 解析规则:在模板里面手动注册的方式,需要自行导包到util.router,并且在路由文件使用registe注册
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


class Init:
    def do(app: FastAPI):
        initHttp(app)
        initRouter(app)
