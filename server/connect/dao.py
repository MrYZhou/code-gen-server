from typing import List

from sqlmodel import Field, Session, SQLModel, create_engine
from db import engine


class Table:
    dbName: str
    tableComment: str
    columnName: str
    columnComment: str
    dataType: str


class DataBase(SQLModel, table=True):
    __tablename__: str = "database"
    id: str = Field(primary_key=True)
    host: str = ""
    port: str = ""
    user: str = ""
    password: str = ""
    name: str = ""
    driver: str = "mysql+pymysql"
    echo: bool = True


def savedb(dataBase):
    with Session(engine) as session:
        session.add(dataBase)
        session.commit()
        session.refresh(dataBase)


def dyConnect(dataBase: DataBase):
    DB_HOST = dataBase.get("host")
    DB_PORT = dataBase.get("port")
    DB_USER = dataBase.get("user")
    DB_PASSWORD = dataBase.get("password")
    DB_NAME = dataBase.get("name")
    DB_DRIVER = dataBase.get("driver") if dataBase.get("driver") else "mysql+pymysql"
    DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    engine = create_engine(DB_URL, echo=True)
    return engine


def getAllTable(engine, name):
    with Session(engine) as session:
        sql: str = f"""SELECT TB.TABLE_NAME as dbName,TB.TABLE_COMMENT as tableComment, COL.COLUMN_NAME as columnName,COL.COLUMN_COMMENT as columnComment,COL.DATA_TYPE   as dataType
                FROM INFORMATION_SCHEMA.TABLES TB,INFORMATION_SCHEMA.COLUMNS COL
                Where TB.TABLE_SCHEMA ='{name}' AND TB.TABLE_NAME = COL.TABLE_NAME"""

        list = session.execute(sql).fetchall()
        return list


def getTable(engine, name, table):
    with Session(engine) as session:
        sql = f"""SELECT TB.TABLE_COMMENT as tableComment, COL.COLUMN_NAME as columnName,COL.COLUMN_COMMENT as columnComment,COL.DATA_TYPE   as dataType
                FROM INFORMATION_SCHEMA.TABLES TB,INFORMATION_SCHEMA.COLUMNS COL
                Where TB.TABLE_SCHEMA ='{name}' AND TB.TABLE_NAME = COL.TABLE_NAME 
                and TB.TABLE_NAME='{table}'"""
        list: List[Table] = session.execute(sql).fetchall()
        return list
