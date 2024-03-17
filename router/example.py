import asyncio
import time
from typing import List
from fastapi import APIRouter, Request, Header, Body
from fastapi.responses import (
    RedirectResponse,
    FileResponse,
)

from walrus import Database as RedisDatabase
from laorm.stream import FieldDescriptor, sql, table
from laorm.PPA import PPA


from util.base import Common, jinjaEngine


from util.exception import exception

from util.response import AppResult


router = APIRouter(
    prefix="/example",
    tags=["示例代码"],
    responses={404: {"description": "Not found"}},
)


db = RedisDatabase(host="localhost", port=6379)
rate = db.rate_limit("speedlimit", limit=5, per=60)  # 每分钟只能调用5次


@table("config")
class Config1:
    id: str = FieldDescriptor(primary=True)
    name: str = FieldDescriptor()

    @sql
    def selectByName(name: str) -> list["Config1"]:
        pass

    @sql
    def selectOneByName(name:str)->'Config1':pass

@table()
class Users:
    id: str = FieldDescriptor(primary=True)
    username: str = FieldDescriptor()
# 读取自定义方法的返回类型
@router.get("/config2/getdy")
async def getdy2():
    res: List[Config1] = await Config1.selectByName(22)
    res:Config1 = await Config1.selectOneByName(22)
    return AppResult.success(res)


# dynamic 都是查询数组回来
@router.get("/config2/getdy2")
async def getdy():
    res = await Config1.dynamic("selectByIdAndName", [2, 456])
    res = await Config1.dynamic('selectByName',123)
    return AppResult.success(res)


# 默认get是查询首个对象, getList自动为数组
@router.get("/config2/get")
@exception
async def get_config2():
    res = await Config1.where(name=22).get()
    res = await Users.get(407)
    res = await Config1.where(name=22).getList()
    return AppResult.success(res)


@router.post("/config2/add")
async def addone():
    await Config1.delete(1)
    await Config1.delete(2)
    config1 = Config1()
    config1.id = 1
    config1.name = 123
    config12 = Config1()
    config12.id = 2
    config12.name = 456
    configlist = [config12]
    await Config1.post(config1)
    await Config1.post(configlist)
    return AppResult.success()


@router.delete("/config2/delete")
async def deleteone():
    await Config1.delete(1)
    # res = await Config1.where(name=22).delete()
    return AppResult.success()


@router.delete("/config2/deletedy")
async def deletedy():
    config1 = Config1()
    config1.id = 1
    config1.name = 123
    await Config1.post(config1)
    await Config1.dynamic("deleteById", 1)
    return AppResult.success()


@router.put("/config2/update")
async def updateone():
    config1 = Config1()
    config1.id = 1
    config1.name = 123
    res = await Config1.where(name=22).update(config1)
    return AppResult.success(res)


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
        print(i[0].get("id"))
    print(f"代码执行时间aio: {execution_time} 秒")
    return AppResult.success(results[0])


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
