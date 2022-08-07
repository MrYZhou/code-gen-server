from asyncio.windows_events import NULL
import imp
from msilib.schema import tables
from fastapi import APIRouter, Depends, HTTPException, Body
from server.generate.dao import Config

from server.generate.index import configParse
from util.base import Common
import time

router = APIRouter(
    prefix="/generate",
    tags=["代码生成"],
    responses={404: {"description": "Not found"}},
)


configInfo = {
    "id": "",
    "info": {
        "pk": "id",
        "name": "Plan",
        "config": {},
        "column": [{"label": "名称", "value": "name"}],
    },
}

# todo 2022.8.7
# 直接生成一个预览同时,返回一个缓存的key
@router.post("/")
async def index(data:Config):
    # data:Config = config
    if data.cacheKey is None:
        data.cacheKey = Common.randomkey()
    a= time.time()    
    res = configParse(data.cacheKey, data)
    b= time.time()   
    print(a,b)
    
    return {"cacheKey": data.cacheKey, "res": res}




# 通过缓存下载
@router.post("/download")
async def index(data=Body(None)):
    return


# todo 2022.8.15
# 读取所有表信息,可以采用临时直接连接的,或者数据库的
@router.get("/tableList")
async def index(data=Body(None)):
    pass


# 保存连接的数据库信息
@router.post("/database")
async def index(data=Body(None)):
    pass


# 预览文档根据id
@router.get("/{id}", tags=["web", "app"])
async def index(id):
    pass


# 直接下载模板通过id.这时候要在解析一下
@router.get("/download/{id}")
async def index(data=Body(None)):
    return


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
