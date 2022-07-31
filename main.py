from fastapi import FastAPI, Request,Header,Body
from fastapi.responses import JSONResponse,RedirectResponse,FileResponse
from fastapi.templating import Jinja2Templates
from walrus import Database, RateLimitException

app = FastAPI()

# 模板初始化
template = Jinja2Templates("pages")
 
db = Database(host='localhost',port=6379)
rate = db.rate_limit("speedlimit", limit=5, per=60)  # 每分钟只能调用5次



# 获取路径参数
@app.get("/user/{id}")
async def root(id):
    return {"code": 200, "msg": f"用户{id}"}
# 获取查询字符串
@app.get("/user")
async def root(id):
    return {"code": 200, "msg": f"用户{id}"}

# 请求头
@app.get("/token")
async def root(id,token=Header(None)):
    return {"code": 200, "msg": f"token:{token}"}

# post请求和参数获取
@app.post("/post")
def body(data = Body(None)):
   return {"code": 200, "msg": f"username:{data.username}"}


# 多请求
@app.api_route("/mulreq",methods=('get','post'))
def mulreq():
  return "success"

# html流
@app.get("/html")
def html(username,request: Request):
    list = ['音乐','游戏','编码']
    return template.TemplateResponse("1.html",{"request":request,'username':username,'list':list})
# 重定向
@app.get("/redirect")
async def root(id):
    return RedirectResponse('/html',status_code=302)    
# 文件流
@app.get("/avator")
def html():
    avator= 'static/img'
    # fileName不写会默认打开到这个图片页面
    return FileResponse(avator,fileName='beauty,jpg')

# 限流
@app.get("/com")
@rate.rate_limited(lambda request: request.client.host)
def root2(request: Request):
    return {"code": 200, "msg": "success"}
# 限流处理器
@app.exception_handler(RateLimitException)
async def handle(request: Request, exc: RateLimitException):

    msg = {'code':400,'msg':f'太快了哟!,{request.client.host}'}
    return JSONResponse(status_code=412, content=msg)
