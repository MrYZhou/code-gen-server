import os
from dotenv import load_dotenv
from fastapi import FastAPI
from laorm import PPA


class PPAFastAPI(PPA):
    _instance = None

    # 集成主要就是注册对应框架的开启和结束的生命周期
    @classmethod
    def init_app(cls, app: FastAPI, *args):
        if cls._instance is None:
            load_dotenv()
            default_values = {
                "host": os.getenv("DB_HOST", "192.168.20.143"),
                "port": int(os.getenv("DB_PORT", 3306)),
                "user": os.getenv("DB_USER", "root"),
                "password": os.getenv("DB_PASSWORD", "root"),
                "db": os.getenv("DB_NAME", "study"),
                "charset": "utf8mb4",
                "autocommit": True,
            }
            args = {**default_values, **args[0]} if len(args) == 1 else default_values
            cls._instance = cls()
            # 将更新后的args传递给startup方法以便初始化数据库连接池
            cls.startup_params = args
            app.add_event_handler("startup", cls.startup)
            app.add_event_handler("shutdown", cls.shutdown)
