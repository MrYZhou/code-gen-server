from datetime import timedelta
from fastapi import APIRouter, Body, HTTPException, Request,status
from laorm import FieldDescriptor, table
from util.response import AppResult
from util.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

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
async def login(data=Body(Users)):

    user = await Users.where(username=user.username).get()
    if user is None or user.password != data.password:
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return AppResult.success({"access_token": access_token})
@router.get("/users/me", response_model=Users)
async def read_users_me(request: Request):
    user = request.state.user
    if user is None:
        return AppResult.fail(status.HTTP_401_UNAUTHORIZED, "用户未登录")
    return user