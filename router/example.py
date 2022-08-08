from asyncio.windows_events import NULL
import imp
from msilib.schema import tables
import os
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import FileResponse
from server.generate.dao import Config

from server.generate.index import configParse
from util.base import Common, registe
import time


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


# todo 2022.8.15
# 直接下载模板通过id.这时候要在解析一下
@router.get("/download/{id}")
async def index(data=Body(None)):
    return


# 保存连接的数据库信息
@router.post("/database")
async def index(data=Body(None)):
    pass


# 读取所有表信息,可以采用临时直接连接的,或者数据库的
@router.get("/tableList")
async def index(data=Body(None)):
    pass


# 预览文档根据id
@router.get("/{id}", tags=["web", "app"])
async def index(id):
    pass


# todo 2022.8.20
# 获取所有生成的配置列表
@router.get("/configList")
async def index(id):
    pass


# 保存生成的配置
@router.post("/saveConfig")
async def index(data=Body(None)):
    pass


# 获取生成的配置
@router.get("/config/{id}")
async def index(id):
    pass
