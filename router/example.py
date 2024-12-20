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
from jinja2 import Template

router = APIRouter(
    prefix="/example",
    tags=["示例代码"],
    responses={404: {"description": "Not found"}},
)


class Page:
    page: int = 1
    size: int = 20


db = RedisDatabase(host="localhost", port=6379)

rate = db.rate_limit("speedlimit", limit=5, per=60)  # 每分钟只能调用5次


@table("config")
class Config1:
    id: str = FieldDescriptor(primary=True)
    name: str = FieldDescriptor()
    age: int = FieldDescriptor()

    @sql
    def selectByName(name: str) -> list["Config1"]:
        pass

    @sql
    def selectOneByName(name: str) -> "Config1":
        pass


@table()
class Users:
    id: str = FieldDescriptor(primary=True)
    username: str = FieldDescriptor()


# 读取自定义方法的返回类型
@router.get("/config2/getdy")
async def getdy2():
    res: List[Config1] = await Config1.selectByName(22)
    res: Config1 = await Config1.selectOneByName(22)
    return AppResult.success(res)


# dynamic 都是查询数组回来
@router.get("/config2/getdy2")
async def getdy():
    res = await Config1.dynamic("selectByIdAndName", [2, 456])
    res = await Config1.dynamic("selectByName", 123)
    return AppResult.success(res)


@router.get("/config2/getdy3")
async def getdy3():
    res: Config1 = await Config1.selectById(1)
    return AppResult.success(res)


# 分页查询
@router.post("/config2/page")
async def body(page=Body(Page)):
    data = (
        await Config1.where(name="邱桂珍").match("age", ">30", "age", "<32").page(page)
    )
    return AppResult.success(data)


# 默认get是查询首个对象, getList自动为数组
@router.get("/config2/get")
@exception
async def get_config2():
    res = await Config1.where(name=22).get()
    res = await Users.get(407)
    res = await Config1.where(name=22).getList([1, 2, 3])
    return AppResult.success(res)


@router.get("/config2/addBatch")
async def addBatch():
    configlist = []
    for i in range(0, 20000):
        config1 = Config1()
        config1.id = Common.uid()
        config1.name = Common.randomName()
        config1.age = Common.randomAge()
        configlist.append(config1)
    await Config1.post(configlist)
    return AppResult.success(configlist)


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
async def deleteconfig():
    await Config1.delete([1, 2])
    config1 = Config1()
    config1.id = 1
    config1.name = 123
    await Config1.post(config1)

    return AppResult.success("删除成功")


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
def postbody(data=Body(None)):
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
def html(request: Request, username: str = ""):
    list = ["音乐", "游戏", "编码"]
    content = jinjaEngine.TemplateResponse(
        "1.html", {"request": request, "username": username, "list": list}
    )
    return content


# jinja到文件
@router.get("/render")
def render():
    content = {"username": "larry", "list": ["音乐", "游戏", "编码"]}
    template = jinjaEngine.get_template("1.html")
    template.stream(content).dump("template/new_file.html")
    return content


# 列表去重
def removeSame(data):
    return list(set(data))


@router.get("/renderStr")
def renderStr():
    template_str = """
    <p>Hello, {{ name }}!
    You have {{ num }} new messages.</p>
    {{removeSame(arr)}}
    """
    data = {"name": "Larry", "num": 3}
    template = Template(template_str)
    template.globals["removeSame"] = removeSame
    template.globals["arr"] = [1, 2, 3, 2]

    return template.render(data)


# 重定向
@router.get("/redirect")
async def redirect(id):
    return RedirectResponse("/html", status_code=302)


# 限流
@router.get("/com")
@rate.rate_limited(lambda request: request.client.host)
def com(request: Request):
    return {"code": 200, "msg": "success"}
