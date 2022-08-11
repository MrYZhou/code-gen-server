import os
from db import engine
from fastapi import APIRouter, Body
from fastapi.responses import FileResponse
from server.generate.dao import Config

from server.generate.index import configParse
from util.base import Common
from sqlmodel import Session
from sqlmodel import select

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

# 预览代码文档根据id
@router.get("/{id}", tags=["web", "app"])
async def index(id):
    pass

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


# 保存生成的配置
@router.get("/saveConfig")
async def index(data=Body(None)):
    return 1

    
# 获取数据库的列表
@router.get("/list",status_code=200)
async def index():
    with Session(engine) as session:
        list = session.exec(select(Config).offset(0).limit(100)).all()
        return list    
    

# 保存生成的配置
@router.post("/saveConfig")
async def index(data=Body(None)):
    print(1)
    return 1


# 获取生成的配置
@router.get("/config/{id}")
async def index(id):
    pass
