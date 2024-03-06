from dataclasses import dataclass
from typing import List


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
class AppResult:
    code: int
    msg: str
    data: object = None

    @classmethod
    def success(cls, *args):
        if len(args) == 0:
            return {"code": 200, "msg": "Success"}
        if len(args) == 1:
            if isinstance(args[0], str):
                return {"code": 200, "msg": args[0]}
            return {"code": 200, "data": args[0], "msg": "Success"}
        if len(args) == 2:
            return {"code": 200, "data": args[0], "msg": args[1]}

    @classmethod
    def fail(cls, *args):
        if len(args) == 0:
            return AppResult(code=400, msg="Fail")
        if len(args) == 1:
            if isinstance(args[0], str):
                return {"code": 400, "msg": args[0]}
            return {"code": 400, "data": args[0], "msg": "Fail"}
        if len(args) == 2:
            return {"code": 400, "data": args[0], "msg": args[1]}

    @classmethod
    def page(cls, list: List, pagination: PaginationVO):
        vo = PageListVO(list=list, pagination=pagination)
        return {"code": 200, "data": vo, "msg": "Success"}
