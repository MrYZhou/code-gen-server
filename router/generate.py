import os
import time
from typing import List

from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from nanoid import generate
from sqlmodel import Session, select
from laorm.core.PPA import PPA

from server.connect.dao import DataBase, getTable, dyConnect
from server.generate.dao import Config
from server.generate.index import configGen, configParse
from util.base import Common

engine = None

rate = Common.rate()

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
async def downloadbycachekey(data: Config = Config()):
    # 解析模板
    if not data.cacheKey:
        data.cacheKey = Common.randomkey()
        configParse(data.cacheKey, data)

    # 压缩模板
    name = "模板" + data.cacheKey
    url = os.path.join(os.getcwd(), "static", name + ".zip")
    return FileResponse(url, filename=name + ".zip", status_code=200)


# 预览
@router.get("/preview")
async def preview():
    try:
        url = os.path.join(os.getcwd(), "static", "logo.ico")
        file_like = open(url, mode="rb")

        return StreamingResponse(file_like, media_type="image/jpg")
    except FileNotFoundError:
        return {"msg": "文件不存在"}


# 获取数据库的列表
@router.get("/list", status_code=200)
async def list():
    with Session(engine) as session:
        start_time = time.time()
        for _ in range(10):
            list = session.exec(select(Config).offset(0).limit(1)).all()
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"代码执行时间: {execution_time} 秒")
        return list


@router.get("/config")
async def get_config():
    start_time = time.time()
    for _ in range(1):
        result: List[Config] = await PPA.exec("SELECT * FROM config")
        print(result[0].get("id"))
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"代码执行时间aio: {execution_time} 秒")
    return result


# 保存生成的配置
@router.post("/saveConfig")
async def saveConfig(data: Config):
    with Session(engine) as session:
        data.id = generate()
        session.add(data)
        session.commit()
        session.refresh(data)
        return data


# 获取生成的配置根据id
@router.get("/config/{id}")
async def configid(id):
    with Session(engine) as session:
        data = session.get(Config, id)
        if not data:
            raise HTTPException(status_code=404, detail="data not found")
        return data


# 删除生成的配置根据id
@router.delete("/config/{id}")
async def configdelete(id):
    with Session(engine) as session:
        data = session.get(Config, id)
        if not data:
            raise HTTPException(status_code=404, detail="data not found")
        session.delete(data)
        session.commit()
        return {"ok": True}


# v2
# 下载对应单表的代码,并且下载限流
@router.post("/code")
@rate.rate_limited(lambda request: request.client.host)
async def codedown(dataBase: DataBase = Body(DataBase)) -> FileResponse:
    # 获取表的字段信息
    list = getTable(dyConnect(dataBase), dataBase.get("name"), dataBase.get("table"))
    fieldPrefix = dataBase["prefix"]["field"]
    dataList = []
    for item in list:
        columnBase = item[1]
        column = item[1].replace(fieldPrefix, "")
        columnName = column[:1].lower() + column[1:]
        dataList.append(
            {**item, **{"columnName": columnName, "columnBase": columnBase}}
        )

    # 模块解析
    path = await configGen(dataList, dataBase)
    url = f"./static/{path}.zip"
    return FileResponse(url, filename=f"{url}.zip")


@router.get("/zipfile")
async def root():
    Common.zipfile("./template/java", "./template/java")
    url = "./template/java.zip"
    return FileResponse(url, filename="java.zip")
