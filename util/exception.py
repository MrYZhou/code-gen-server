
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


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
                    status_code=e.status_code,
                    content={"detail": e.detail}
                )
            elif isinstance(e, CustomException):
                return JSONResponse(
                    status_code=e.status_code,
                    content={"detail": e.detail}
                )
            else:
                return JSONResponse(
                    status_code=500,
                    content={"detail": "Internal Server Error"}
                )
        
        return response