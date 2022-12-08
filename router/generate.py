import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from nanoid import generate
from sqlmodel import Session, select

from db import engine
from server.generate.dao import Config
from server.generate.index import configParse
from util.base import Common

router = APIRouter(
    prefix="/generate",
    tags=["代码生成"],
    responses={404: {"description": "Not found"}},
)

# 直接生成一个预览代码,返回一个缓存的key
@router.post("/")
async def index(data: Config):
    if not data.cacheKey:
        data.cacheKey = Common.randomkey()

    res = configParse(data.cacheKey, data)

    return {"cacheKey": data.cacheKey, "res": res}


# 通过缓存下载
@router.post("/download")
async def index(data: Config = Config()):
    # 解析模板
    if not data.cacheKey:
        data.cacheKey = Common.randomkey()
        configParse(data.cacheKey, data)

    # 压缩模板
    name = "模板" + data.cacheKey
    url = os.path.join(os.getcwd(), "static", name + ".zip")
    return FileResponse(url, filename=name + ".zip", status_code=200)



    
# 获取数据库的列表


@router.get("/list", status_code=200)
async def index():
    with Session(engine) as session:
        list = session.exec(select(Config).offset(0).limit(100)).all()
        return list


# 保存生成的配置
@router.post("/saveConfig")
async def index(data: Config):
    with Session(engine) as session:
        data.id = generate()
        session.add(data)
        session.commit()
        session.refresh(data)
        return data


# 获取生成的配置根据id
@router.get("/config/{id}")
async def index(id):
    with Session(engine) as session:
        data = session.get(Config, id)
        if not data:
            raise HTTPException(status_code=404, detail="data not found")
        return data


# 删除生成的配置根据id
@router.delete("/config/{id}")
async def index(id):
    with Session(engine) as session:
        data = session.get(Config, id)
        if not data:
            raise HTTPException(status_code=404, detail="data not found")
        session.delete(data)
        session.commit()
        return {"ok": True}
