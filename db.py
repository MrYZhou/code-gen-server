import os

from sqlmodel import create_engine
from starlette.config import Config

if not os.path.exists(".env"):
    with open(".env", "w") as f:
        f.write("DB_HOST=127.0.0.1\n")
        f.write("DB_PORT=3306\n")
        f.write("DB_USER=root\n")
        f.write("DB_PASSWORD=123456\n")
        f.write("DB_NAME=study\n")
        f.write("DB_DRIVER=mysql+pymysql\n")
        f.write("SQLMODEL_ECHO=False\n")

config = Config(".env")

DB_HOST = config.get("DB_HOST", default="127.0.0.1")
DB_PORT = config.get("DB_PORT", default="3306")
DB_USER = config.get("DB_USER", default="root")
DB_PASSWORD = config.get("DB_PASSWORD", default="123456")
DB_NAME = config.get("DB_NAME", default="study")
DB_DRIVER = config.get("DB_DRIVER", default="mysql+pymysql")
SQLMODEL_ECHO = True if config.get("SQLMODEL_ECHO") == "True" else False

DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
print(f"连接地址 : {DB_URL}")
print(f"打印sql  : {SQLMODEL_ECHO}")
engine = create_engine(DB_URL, echo=SQLMODEL_ECHO)
