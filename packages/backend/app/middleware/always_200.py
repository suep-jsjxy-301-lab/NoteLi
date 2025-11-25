from typing import Callable, Awaitable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.core.logger import logger


class Always200Middleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        logger.trace("INTO Always200Middleware")
        response: Response = await call_next(request)
        response.headers["X-Original-Status"] = str(object=response.status_code)
        response.status_code = 200
        logger.trace("OUT Always200Middleware")
        return response
