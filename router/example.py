import asyncio
import os
import time
from typing import Sequence
from fastapi import APIRouter, Request, Header, Body
from fastapi import Depends
from fastapi.responses import (
    RedirectResponse,
    FileResponse,
    StreamingResponse,
)
# from sqlalchemy import table

from walrus import Database as RedisDatabase
from laorm.core.stream import FieldDescriptor, table

from laorm.fastapi import PPA


from server.generate.dao import Config

from util.base import Common, jinjaEngine


from sqlmodel import create_engine, Session, select


router = APIRouter(
    prefix="/example",
    tags=["示例代码"],
    responses={404: {"description": "Not found"}},
)


db = RedisDatabase(host="localhost", port=6379)
rate = db.rate_limit("speedlimit", limit=5, per=60)  # 每分钟只能调用5次


@router.get("/dynamicConnect")
async def dynamicConnect():
    sql = """SELECT TB.TABLE_NAME as dbName,TB.TABLE_COMMENT as tableComment, COL.COLUMN_NAME as columnName,COL.COLUMN_COMMENT as columnComment,COL.DATA_TYPE   as dataType
FROM INFORMATION_SCHEMA.TABLES TB,INFORMATION_SCHEMA.COLUMNS COL
Where TB.TABLE_SCHEMA ='study' AND TB.TABLE_NAME = COL.TABLE_NAME"""
    DB_URL = "mysql+pymysql://root:root@localhost:3306/study?charset=utf8mb4"
    engine = create_engine(DB_URL)
    with Session(engine) as session:
        # list:List[Table] = session.execute(sql).fetchall()
        # list:List[Table]  = session.exec(select(text(sql))).all()
        pass
    return []

@table("config")
class Config1:
    id:str = FieldDescriptor(primary=True)
    name:str = FieldDescriptor()

@router.get("/config2")
async def get_config2():
    res = await  Config1.get(1)
    return res

@router.get("/config")
async def get_config():
    start_time = time.time()
    # 创建并发任务
    tasks = [
        PPA.exec("SELECT * FROM config where id=1"),
        # PPA.exec("SELECT * FROM config where id!={name}",{"name":1}),
        # PPA.exec("SELECT * FROM config where id!=?",[1]),
        # PPA.exec("SELECT * FROM config where id!=?", (1,)),
    ]

    # 并发执行并获取结果
    results = await asyncio.gather(*tasks)
    print(results)
    end_time = time.time()
    execution_time = end_time - start_time
    for i in results:
        print(i[0].get('id'))
    print(f"代码执行时间aio: {execution_time} 秒")
    return results[0]


@router.get("/dependSession")
async def dependSession(session: Session = Depends(Common.get_session)):
    print(id(session))
    config: Sequence[Config] = session.exec(select(Config)).all()
    return config


# 预览图片
@router.get("/preview")
async def preview(data: Config = Body(Config)):
    url = os.path.join(os.getcwd(), "static", "1.png")
    file_like = open(url, mode="rb")
    return StreamingResponse(file_like, media_type="image/jpg")


# 获取路径参数
@router.get("/user/{id}")
async def root(id):
    return {"code": 200, "msg": f"用户{id}"}


# 获取查询字符串
@router.get("/user")
async def user(id):
    return {"code": 200, "msg": f"用户{id}"}


# 请求头
@router.get("/token")
async def token(id, token=Header(None)):
    return {"code": 200, "msg": f"token:{token}"}


# post参数获取
@router.post("/post")
def body(data=Body(None)):
    return {"code": 200, "msg": f"username:{data.username}"}


# 多请求合并
@router.api_route("/mulreq", methods=["get", "post"])
def mulreq():
    return "success"


# 流操作
@router.get("/zipfile")
async def zipfile():
    Common.zipfile("./dao", "dao2")
    url = "./dao2.zip"
    return FileResponse(url, filename="dao2.zip")


@router.get("/avator")
def avator():
    avator = "static/img"
    # fileName不写会默认打开到这个图片页面
    return FileResponse(avator, filename="beauty.jpg")


# jinja 到浏览器
@router.get("/html")
def html(username, request: Request):
    list = ["音乐", "游戏", "编码"]
    content = jinjaEngine.TemplateResponse(
        "1.html", {"request": request, "username": username, "list": list}
    )
    print(content.body)
    return content


# jinja到文件
@router.get("/render")
def render():
    content = {"username": "larry", "list": ["音乐", "游戏", "编码"]}
    template = jinjaEngine.get_template("1.html")
    template.stream(content).dump("my_new_file.html")

    return "success"


# 重定向
@router.get("/redirect")
async def redirect(id):
    return RedirectResponse("/html", status_code=302)


# 限流
@router.get("/com")
@rate.rate_limited(lambda request: request.client.host)
def com(request: Request):
    return {"code": 200, "msg": "success"}
