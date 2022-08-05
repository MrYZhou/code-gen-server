from sqlmodel import create_engine
import os

env = os.environ
DB_HOST = env.get("DB_HOST") if env.get("DB_HOST") else "localhost"
DB_PORT = env.get("DB_PORT") if env.get("DB_PORT") else "3306"
DB_USER = env.get("DB_USER") if env.get("DB_USER") else "root"
DB_PASSWORD = env.get("DB_PASSWORD") if env.get("DB_PASSWORD") else "123456"
DB_NAME = env.get("DB_NAME") if env.get("DB_NAME") else "study"
DB_DRIVER = env.get("DB_DRIVER") if env.get("DB_DRIVER") else "mysql+pymysql"
SQLMODEL_ECHO = (
    bool(env.get("SQLMODEL_ECHO")) if bool(env.get("SQLMODEL_ECHO")) else False
)


DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(DB_URL, echo=SQLMODEL_ECHO)
