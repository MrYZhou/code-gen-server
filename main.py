from fastapi import FastAPI, Request


from util.system import Init


app = FastAPI()
Init.do(app)


@app.get("/")
def root():
    return "https://www.baidu.com"
