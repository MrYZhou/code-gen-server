from typing import List

from fastapi import APIRouter, HTTPException
from nanoid import generate
from sqlalchemy import Engine
from sqlmodel import Session, select
from fastapi import Body
from server.connect.dao import (
    DataBase,
    Table,
    dyConnect,
    getAllTable,
    getTable,
    savedb,
)
from db import DB

engine = DB()

router = APIRouter(
    prefix="/connect",
    tags=["代码生成"],
    responses={404: {"description": "Not found"}},
)


# 保存连接的数据库信息
@router.post("/database", status_code=200)
async def databasein(dataBase: DataBase):
    dataBase.id = generate()
    savedb(dataBase)
    return dataBase


# 编辑连接的数据库信息
@router.post("/database/edit")
async def database(dataBase: DataBase):
    with Session(engine.get_db()) as session:
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
async def tableList(dataBase: DataBase):
    list: List[Table] = getAllTable(engine, dataBase.name)
    map = {}
    for item in list:
        key = item.dbName
        if key not in map:
            map[key] = []
        map[key].append(item)
    return map


# 读取单表信息
@router.post("/tableInfo")
async def tableInfo(dataBase: dict = Body(None)):
    return getTable(dyConnect(dataBase), dataBase.get("name"), dataBase.get("table"))


# 获取数据库的列表
@router.get("/list", status_code=200)
async def list():
    with Session(engine.get_db()) as session:
        list = session.exec(select(DataBase).offset(0).limit(100)).all()
        return list


# 删除
@router.delete("/database/{id}", status_code=200)
async def index(id):
    with Session(engine.get_db()) as session:
        data = session.get(DataBase, id)
        if not data:
            raise HTTPException(status_code=404, detail="data not found")
        session.delete(data)
        session.commit()
        return {"ok": True}
