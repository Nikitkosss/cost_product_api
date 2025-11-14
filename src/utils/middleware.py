from typing import Any

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class CatchExceptionsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next) -> Any:
        """
        Мидлварь, который ловит все исключения и возвращает json-ответ
        со статусом и текстом ошибки.
        """
        try:
            response = await call_next(request)
            return response
        except HTTPException as e:
            return JSONResponse({"error": str(e)}, status_code=e.status_code)
        except Exception as e:
            return JSONResponse({"code": "ERROR", "errorText": str(e)}, status_code=500)
