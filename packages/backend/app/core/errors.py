# app/core/errors.py
import orjson
from typing import Dict, Callable, Any, List
from fastapi import FastAPI, Request, status
from fastapi.responses import Response
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

from app.core.logger import logger
from app.utils.response import (
    fail_not_found,
    fail_unauthorized,
    fail_forbidden,
    fail_conflict,
    fail_bad_request,
    fail_validation_error,
    fail_internal_error,
)
from app.schemas.response import ResponseModel

# 状态码 → 快捷失败函数
STATUS_MAP: dict[
    int, Callable[[Dict[str, Any] | List[Any] | str | None], ResponseModel[Any]]
] = {
    400: fail_bad_request,
    401: fail_unauthorized,
    403: fail_forbidden,
    404: fail_not_found,
    409: fail_conflict,
    422: fail_validation_error,
    500: fail_internal_error,
}


async def http_exception_handler(request: Request, exc: Exception) -> Response:
    """
    统一处理 StarletteHTTPException（含 FastAPI 主动抛出的 HTTPException）。
    按状态码自动匹配 fail_* 函数；若未在 STATUS_MAP 中定义，则统一用 500。
    """
    assert isinstance(exc, StarletteHTTPException)
    fail_func: Callable[
        [Dict[str, Any] | List[Any] | str | None], ResponseModel[Any]
    ] = STATUS_MAP.get(exc.status_code, fail_internal_error)
    logger.warning(f"HTTPException {exc.status_code} {request.url.path} - {exc.detail}")
    return Response(
        status_code=exc.status_code,
        media_type="application/json",
        content=orjson.dumps(fail_func(exc.detail).model_dump()),
    )


async def validation_exception_handler(request: Request, exc: Exception) -> Response:
    """处理请求体校验失败（422）"""
    assert isinstance(exc, RequestValidationError)
    message = "; ".join(
        [f"{'.'.join(map(str, err['loc']))}: {err['msg']}" for err in exc.errors()]
    )
    logger.info("Validation error %s - %s", request.url.path, message)
    return Response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        media_type="application/json",
        content=orjson.dumps(fail_validation_error(details=message).model_dump()),
    )


async def all_exception_handler(request: Request, exc: Exception) -> Response:
    """兜底：捕获任何未处理的 Python 异常，返回 500"""
    logger.exception("Unhandled exception at %s", request.url.path)
    return Response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        media_type="application/json",
        content=orjson.dumps(
            fail_internal_error(details="Internal server error").model_dump()
        ),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """在 FastAPI 实例上注册所有异常处理器"""
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, all_exception_handler)
