from fastapi import FastAPI
from util.system import Init

from server.food.dao import addFood
app = FastAPI()

Init.do(app)

@app.get("/")
async def index():
    return "index"
