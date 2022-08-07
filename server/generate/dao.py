
from typing import List
from pydantic import BaseModel
class Column(BaseModel):
  label:str
  value:str
  
class Config(BaseModel):
  id:str =None
  cacheKey:str=None
  pk:str=None
  name:str=None
  column: List[Column] = None
  