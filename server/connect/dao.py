from typing import Optional
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
