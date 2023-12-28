import uvicorn
from fastapi import FastAPI

from util.system import Init

app = FastAPI()

if __name__ == "__main__":
    Init.do(app)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, workers=1)
    