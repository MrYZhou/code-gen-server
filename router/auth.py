from fastapi import APIRouter, Body, HTTPException, status
from laorm import FieldDescriptor, table
from util.response import AppResult
from util.auth import create_access_token, UserContext
from util.redis import redisTool

router = APIRouter(
    prefix="/auth",
    tags=["认证授权"],
    responses={404: {"description": "Not found"}},
)


@table()
class Users:
    id: str = FieldDescriptor(primary=True)
    username: str = FieldDescriptor()
    password: str = FieldDescriptor()


@router.post("/login")
async def login(data: Users = Body(Users)):
    # 1.获取yo
    user = await Users.where(username=data.username).get()
    # 2.校验密码
    if user is None or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    access_token = redisTool.get(user["id"])
    if access_token is not None:
        return AppResult.success({"access_token": access_token})
    # 3.生成token
    access_token = create_access_token(user)
    # 4.返回token
    return AppResult.success({"access_token": access_token})


@router.get("/info")
async def read_users_me():
    user = UserContext.getUser()
    if user is None:
        return AppResult.fail(status.HTTP_401_UNAUTHORIZED, "用户未登录")
    return AppResult.success(user, "操作成功")
