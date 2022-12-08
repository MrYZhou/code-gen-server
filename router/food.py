

import os

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from server.generate.dao import Config

router = APIRouter(
    prefix="/food",
    tags=["代码生成"],
    responses={404: {"description": "Not found"}},
)


# 预览
@router.get("/preview")
async def preview(data: Config = Config()):
    url = os.path.join(os.getcwd(), "static", "1.png" )
    file_like = open(url, mode="rb")
    return StreamingResponse(file_like, media_type="image/jpg")