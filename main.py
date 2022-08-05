from typing import List
from fastapi import FastAPI, Request, Header, Body
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from walrus import Database as RedisDatabase, RateLimitException

from fastapi.middleware.cors import CORSMiddleware

from util.index import Common
from server.connect.dao import Table

from db import engine
from sqlmodel import create_engine,SQLModel,Session
app = FastAPI()

# 资源访问
origins = [
    "http://localhost",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 模板初始化
jinjaEngine = Jinja2Templates("template")
#redis
db = RedisDatabase(host="localhost", port=6379)
rate = db.rate_limit("speedlimit", limit=5, per=60)  # 每分钟只能调用5次

@app.get("/")
async def index():
    return 'index'
