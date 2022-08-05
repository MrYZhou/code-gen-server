
from sqlmodel import create_engine,SQLModel
DB_HOST = "localhost"
DB_PORT = "3307"
DB_USER = "root"
DB_PASSWORD = "123456"
DB_NAME = "study"
DB_DRIVER = "mysql+pymysql"
DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
SQLMODEL_ECHO = True

print(DB_URL)
engine = create_engine(DB_URL, echo=SQLMODEL_ECHO)
