import contextvars
from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Coroutine, List, Optional
from starlette.middleware.base import BaseHTTPMiddleware

# 创建一个上下文变量来存储 request 对象
current_request_var = contextvars.ContextVar('current_request')
# 配置 JWT
SECRET_KEY = "laAuth"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta   
    
    encoded_jwt = jwt.encode({"username": data.get("username")}, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 从redis获取缓存，key是token，value是user
def verify_token(token: str):
    user = '123'
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user    


whitePath=["/","/docs", "/redoc", "/openapi.json","/auth/login", "register"]
class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Coroutine[Any, Any, Response]]
    ) -> Response:
        path = request.url.path
        if path in whitePath:
            response = await call_next(request)
            return response

        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        
        user = verify_token(token)
        request.state.user = user
        current_request_var.set(request)  # 设置上下文变量
        response = await call_next(request)
        return response
    
class UserContext:
    @staticmethod
    def getUser():
        request = current_request_var.get(None)  # 获取上下文变量
        if request is None:
            raise HTTPException(status_code=400, detail="Request context not found")
        user = getattr(request.state, 'user', None)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user