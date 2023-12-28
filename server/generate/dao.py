from typing import List

from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel


class Column(SQLModel):
    label: str = ""
    value: str = ""


class Config(SQLModel, table=True):
    __tablename__: str = "config"
    id: str = Field(primary_key=True)
    cacheKey: str = None
    pk: str = None
    name: str = None
    columnList: str = None
