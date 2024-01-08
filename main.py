from fastapi import FastAPI, Request


from util.system import Init


app = FastAPI()
Init.do(app)




@app.get("/")
def root():
    return  {"code": 200, "msg": "success"}



