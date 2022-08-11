
from typing import List
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel
class Column(SQLModel):
  label:str=None
  value:str=None
  
class Config(SQLModel, table=True):
  __tablename__: str = "config"
  id:str =Field(primary_key=True)
  cacheKey:str=None
  pk:str=None
  name:str=None
  columnList: str = None
  