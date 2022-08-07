
from fastapi import FastAPI


from router import example

from fastapi.middleware.cors import CORSMiddleware


# 路由注册
def initRouter(app: FastAPI):
    app.include_router(example.router)


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



