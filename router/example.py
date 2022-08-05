from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"gun": {"name": "Portal Gun"}}

@router.get("/")
async def read_items():
    return fake_items_db

@router.get("/{key}", tags=["custom", "base"])
async def read_item(key):
    return fake_items_db.get(key)
