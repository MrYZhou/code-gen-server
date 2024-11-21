from dataclasses import dataclass
from typing import Any, List

from fastapi.responses import JSONResponse


@dataclass
class PaginationVO:
    size: str
    page: int
    pass


@dataclass
class PageListVO:
    list: List
    pagination: PaginationVO


@dataclass
@dataclass
class AppResult:
    code: int
    msg: str
    data: Any = None

    @classmethod
    def success(cls, *args):
        if len(args) == 0:
            return JSONResponse(status_code=200, content={"code": 200, "msg": "Success"})
        if len(args) == 1:
            if isinstance(args[0], str):
                return JSONResponse(status_code=200, content={"code": 200, "msg": args[0]})
            return JSONResponse(status_code=200, content={"code": 200, "data": args[0], "msg": "Success"})
        if len(args) == 2:
            return JSONResponse(status_code=200, content={"code": 200, "data": args[0], "msg": args[1]})

    @classmethod
    def fail(cls, *args):
        if len(args) == 0:
            return JSONResponse(status_code=400, content={"code": 400, "msg": "Fail"})
        if len(args) == 1:
            if isinstance(args[0], str):
                return JSONResponse(status_code=400, content={"code": 400, "msg": args[0]})
            return JSONResponse(status_code=400, content={"code": 400, "data": args[0], "msg": "Fail"})
        if len(args) == 2:
            if isinstance(args[0], int):
                return JSONResponse(status_code=args[0], content={"code": args[0], "msg": args[1]})
            return JSONResponse(status_code=400, content={"code": 400, "data": args[0], "msg": args[1]})

    @classmethod
    def page(cls, list: List, pagination: PaginationVO):
        vo = PageListVO(list=list, pagination=pagination)
        return JSONResponse(status_code=200, content={"code": 200, "data": vo, "msg": "Success"})
