from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Coroutine, List, Optional
from starlette.middleware.base import BaseHTTPMiddleware


# 配置 JWT
SECRET_KEY = "laAuth"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 模拟用户数据库
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "password": "secret",
    }
}

# OAuth2 密码模式
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        return None
    return token_data    


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

        token = token.replace("Bearer ", "")
        token_data = verify_token(token)
        if not token_data:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        request.state.user = get_user(fake_users_db, username=token_data.username)
        response = await call_next(request)
        return response
    
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)
    return None