from fastapi import FastAPI

from util.system import Init

app = FastAPI()
Init.do(app)