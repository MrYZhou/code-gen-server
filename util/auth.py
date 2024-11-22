import contextvars
from fastapi import FastAPI, HTTPException, Request, Response, status
import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Coroutine
from starlette.middleware.base import BaseHTTPMiddleware
from util.redis import redisTool
from util.response import AppResult

# 创建一个上下文变量来存储 request 对象
current_request_var = contextvars.ContextVar("current_request")
# 配置 JWT
SECRET_KEY = "laAuth"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    encoded_jwt = jwt.encode(
        {"id": data.id, "username": data.username, "exp": expire},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    # 保存在auth目录下的key
    redisTool.set(encoded_jwt, data.id, ex=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    redisTool.set(data.id, encoded_jwt, ex=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    return encoded_jwt


def verify_token(token: str):
    # 从 Redis 中检查 token 是否存在
    if not redisTool.exists(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="未登录")
    # 解析token后再次验证是否过期
    user = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if not user or user.get("exp", 0) < datetime.now(timezone.utc).timestamp():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return user


whitePath = ["/", "/docs", "/redoc", "/openapi.json", "/auth/login", "register"]


class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Coroutine[Any, Any, Response]],
    ) -> Response:
        try:
            # 1. 判断当前请求的路径是否在白名单中
            path = request.url.path
            if path in whitePath:
                response = await call_next(request)
                return response
            # 2. 获取请求头中的token，如果没有，则返回401
            token = request.headers.get("Authorization")
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="未登录"
                )
            # 3. 解析token，如果解析失败，则返回401
            user = verify_token(token)
            # 4. 设置当前请求的用户信息到上下文变量中，并返回响应
            request.state.user = user
            # 5.设置上下文变量
            current_request_var.set(request)
            response = await call_next(request)
            return response
        except HTTPException as e:
            return AppResult.fail(e.status_code, e.detail)


class UserContext:
    @staticmethod
    def getUser():
        request = current_request_var.get(None)  # 获取上下文变量
        if request is None:
            raise HTTPException(status_code=400, detail="未知错误")
        user = getattr(request.state, "user", None)
        if user is None:
            raise HTTPException(status_code=401, detail="用户未登录")
        return user
