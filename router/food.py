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
async def preview():
    try:
        url = os.path.join(os.getcwd(), "static", "logo.ico")
        file_like = open(url, mode="rb")
        
        return StreamingResponse(file_like, media_type="image/jpg")
    except FileNotFoundError:
        return {"msg": "文件不存在"}    
    
