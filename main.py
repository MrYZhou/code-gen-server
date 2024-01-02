
import uvicorn
from fastapi import FastAPI

from util.system import Init

app = None

def init():
    app = FastAPI()
    Init.do(app)

if __name__ == "__main__":
    init()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, workers=1)
    