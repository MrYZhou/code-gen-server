##### End #####
from fastapi import FastAPI
from TestAirSpider import AirSpiderTest
app = FastAPI()
@app.get("/")
async def root():
    AirSpiderTest().start()
    return {'code':200,'msg':'success'}

