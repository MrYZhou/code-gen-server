from typing import List
from fastapi import APIRouter, HTTPException
from nanoid import generate
from db import engine
from server.connect.dao import DataBase
from sqlmodel import Session
from sqlmodel import SQLModel,select,update
from server.connect.dao import savedb

router = APIRouter(
    prefix="/connect",
    tags=["代码生成"],
    responses={404: {"description": "Not found"}},
)

# 数据库表自动创建
@router.get("/initDataBase")
async def method():
    SQLModel.metadata.create_all(engine)
    return "success"


# 保存连接的数据库信息
@router.post("/database", status_code=200)
async def index(dataBase: DataBase):
    dataBase.id = generate()
    savedb(dataBase)
    return dataBase

# 编辑连接的数据库信息
@router.post("/database/edit")
async def index(dataBase: DataBase):
    with Session(engine) as session:
        database = session.get(DataBase, dataBase.id)
        if not database:
            raise HTTPException(status_code=404, detail="数据不存在")
        data = dataBase.dict(exclude_unset=True)
        for key, value in data.items():
            setattr(database, key, value)
        session.add(database)
        session.commit()
        session.refresh(database)
        return database


# 读取所有表信息,可以采用临时直接连接的,或者数据库的
@router.post("/tableList")
async def index(dataBase: DataBase):
    pass


# 获取数据库的列表
@router.get("/list",status_code=200)
async def index():
    with Session(engine) as session:
        list = session.exec(select(DataBase).offset(0).limit(100)).all()
        return list


# 删除
@router.post("/database/{id}")
async def index(id):
    pass
