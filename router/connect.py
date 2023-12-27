from typing import Dict, List

from fastapi import APIRouter, HTTPException
from nanoid import generate
from sqlmodel import Session, SQLModel, select, update
from fastapi import Body
from server.connect.dao import DataBase, Table, dyConnect, getAllTable, getTable, savedb
from db import engine

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


# 读取所有表信息,动态连接数据库
@router.post("/tableList")
async def index(dataBase: DataBase):
    engine = dyConnect(dataBase)
    list: List[Table] = getAllTable(engine, dataBase.name)
    map = {}
    for item in list:
        key = item.dbName
        if not key in map:
            map[key]: List = []
        map[key].append(item)
    return map


# 读取单表信息
@router.post("/tableInfo")
async def index(dataBase: dict = Body(None)):
    return getTable(dyConnect(dataBase), dataBase.get("name"), dataBase.get("table"))


# 获取数据库的列表
@router.get("/list", status_code=200)
async def index():
    with Session(engine) as session:
        list = session.exec(select(DataBase).offset(0).limit(100)).all()
        return list


# 删除
@router.delete("/database/{id}", status_code=200)
async def index(id):
    with Session(engine) as session:
        data = session.get(DataBase, id)
        if not data:
            raise HTTPException(status_code=404, detail="data not found")
        session.delete(data)
        session.commit()
        return {"ok": True}
