from glob import iglob
import uvicorn
from fastapi import FastAPI

from util.system import Init

app = FastAPI()

Init.do(app)


@app.get("/")
async def index():
    return "index"


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, workers=1)
