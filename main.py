from fastapi import FastAPI, Request


from util.system import Init
from util.base import Common

app = FastAPI()
Init.do(app)

rate = Common.rate()


@app.get("/")
async def root() -> dict[str, str | int]:
    return {"code": 200, "msg": "success"}


# 限流
@app.get("/rate")
@rate.rate_limited(lambda request: request.client.host)
def root2(request: Request):
    return {"code": 200, "msg": "success"}
