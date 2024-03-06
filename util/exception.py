import functools
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from util.response import AppResult


def exception(f):
    async def wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except CustomException:
            return AppResult.fail("遇到错误")
        except Exception as e:
            return AppResult.fail("遇到错误:" + e.__doc__)

    return functools.update_wrapper(wrapper, f)


class CustomException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

    # 异常处理器
    async def custom_exception_middleware(request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception as e:
            if isinstance(e, HTTPException):
                return JSONResponse(
                    status_code=e.status_code, content={"detail": e.detail}
                )
            elif isinstance(e, CustomException):
                return JSONResponse(
                    status_code=e.status_code, content={"detail": e.detail}
                )
            else:
                return JSONResponse(
                    status_code=500, content={"detail": "Internal Server Error"}
                )

        return response
