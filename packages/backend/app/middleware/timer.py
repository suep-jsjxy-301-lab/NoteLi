# app/middleware/timer.py
import time
from typing import Callable, Awaitable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.core.logger import logger


class RequestTimerMiddleware(BaseHTTPMiddleware):
    """
    在日志中记录每次请求的处理耗时（毫秒）
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        logger.trace("INTO RequestTimerMiddleware")
        start: float = time.perf_counter()
        response: Response = await call_next(request)
        cost: float = (time.perf_counter() - start) * 1000
        logger.info(
            f"{request.method:>8} {request.url.path} -> {response.headers.get('X-Original-Status', default=response.status_code)}  "
            f"耗时: {cost:.2f}ms"
        )
        # 如果想让前端也能拿到，可写 header
        response.headers["X-Response-Time"] = f"{cost:.2f}ms"
        logger.trace("OUT RequestTimerMiddleware")
        return response
