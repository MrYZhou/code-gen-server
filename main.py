
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from TestAirSpider import AirSpiderTest
from walrus import Database, RateLimitException

app = FastAPI()


#db = Database(host='localhost',port=6379)
# 默认连接loalhost:6379,所以记得启动本地redis服务哦
db = Database()
rate = db.rate_limit('speedlimit', limit=5, per=60) # 每分钟只能调用2次



@app.get("/")
async def root():
    AirSpiderTest().start()
    return {'code':200,'msg':'success'}

# 正常请求
@app.get("/com")
@rate.rate_limited(lambda request: request.client.host)
def root2(request: Request):
    print('请求',request.client.host)
    return {'code':200,'msg':'success'}

# 限流
@app.exception_handler(RateLimitException)
async def handle(request: Request, exc: RateLimitException):
    print('请求')
    msg = {'code':400,'msg':f'太快了哟!,{request.client.host}'}
    return JSONResponse(status_code=412, content=msg)

