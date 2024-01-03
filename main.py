from fastapi import  FastAPI


from util.system import Init

app = FastAPI()
Init.do(app)

@app.get("/")
async def root() -> dict[str, str|int]:
  return {'code':200,'msg':'success'}