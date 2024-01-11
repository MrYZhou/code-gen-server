from fastapi import FastAPI
from fastapi.responses import RedirectResponse


from util.system import Init


app = FastAPI()
Init.do(app)


@app.get("/")
def root():
    return RedirectResponse("https://www.baidu.com")
