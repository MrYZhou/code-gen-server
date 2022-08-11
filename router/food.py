

from fastapi import APIRouter
router = APIRouter(
    prefix="/food",
    tags=["代码生成"],
    responses={404: {"description": "Not found"}},
)
