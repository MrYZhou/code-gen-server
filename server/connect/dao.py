from typing import List, Optional
from db import engine
from sqlmodel import Field, Session
from sqlmodel import create_engine, SQLModel
from sqlmodel import Field, Session, SQLModel


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
    echo: str = True


def savedb(dataBase):

    with Session(engine) as session:
        session.add(dataBase)
        session.commit()
        session.refresh(dataBase)


def dyConnect(dataBase: DataBase):
    DB_HOST = dataBase.host
    DB_PORT = dataBase.port
    DB_USER = dataBase.user
    DB_PASSWORD = dataBase.password
    DB_NAME = dataBase.name
    DB_DRIVER = dataBase.driver
    SQLMODEL_ECHO = dataBase.echo
    DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    engine = create_engine(DB_URL)
    return engine


def getAllTable(engine):
    res={}
    with Session(engine) as session:
        sql = """SELECT TB.TABLE_NAME as dbName,TB.TABLE_COMMENT as tableComment, COL.COLUMN_NAME as columnName,COL.COLUMN_COMMENT as columnComment,COL.DATA_TYPE   as dataType
                FROM INFORMATION_SCHEMA.TABLES TB,INFORMATION_SCHEMA.COLUMNS COL
                Where TB.TABLE_SCHEMA ='study' AND TB.TABLE_NAME = COL.TABLE_NAME"""
        list:List[Table] = session.execute(sql).fetchall()
        return list        
