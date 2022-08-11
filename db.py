from sqlmodel import create_engine
import os
from dotenv import load_dotenv
load_dotenv()
env = os.environ
DB_HOST = os.getenv("DB_HOST") if os.getenv("DB_HOST") else "localhost"
DB_PORT = os.getenv("DB_PORT") if os.getenv("DB_PORT") else "3306"
DB_USER = os.getenv("DB_USER") if os.getenv("DB_USER") else "root"
DB_PASSWORD = os.getenv("DB_PASSWORD") if os.getenv("DB_PASSWORD") else "123456"
DB_NAME = os.getenv("DB_NAME") if os.getenv("DB_NAME") else "study"
DB_DRIVER = os.getenv("DB_DRIVER") if os.getenv("DB_DRIVER") else "mysql+pymysql"
SQLMODEL_ECHO = (
    bool(os.getenv("SQLMODEL_ECHO")) if bool(os.getenv("SQLMODEL_ECHO")) else False
)


DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(DB_URL, echo=SQLMODEL_ECHO)
