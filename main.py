import uvicorn
from fastapi import FastAPI

from util.system import Init
from util.base import Common
from fastapi.responses import FileResponse
app = FastAPI()


Init.do(app)

@app.get("/")
async def index():
    return "index"
@app.get("/zipfile")
async def root():
    Common.zipfile("./template/java", "./template/java")
    url = "./template/java.zip"
    return FileResponse(url, filename="java.zip")
if __name__ == '__main__':
    uvicorn.run('main:app',host='0.0.0.0',port= 8000, reload=True, workers=1)
    

