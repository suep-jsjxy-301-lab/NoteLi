# app/utils/response.py
from typing import Optional, TypeVar, List, Any, Dict
from fastapi import status
from datetime import datetime, timezone
from app.schemas.response import ResponseModel, ErrorModel, PaginationModel

T = TypeVar("T")

# ---------------------  成功响应  --------------------- #


def ok(
    data: Optional[T] = None,
    message: str = "成功",
    pagination: Optional[PaginationModel] = None,
) -> ResponseModel[T]:
    """单条或任意 JSON 数据"""
    return ResponseModel[T](
        success=True,
        message=message,
        data=data,
        pagination=pagination,
        timestamp=datetime.now(timezone.utc),
    )


def ok_list(
    items: List[T], total: int, page: int = 1, size: int = 10, message: str = "成功"
) -> ResponseModel[List[T]]:
    """带分页的列表数据"""
    total_pages = (total + size - 1) // size
    pagination = PaginationModel(
        total_item=total, total_pages=total_pages, page=page, size=size
    )
    return ok(data=items, message=message, pagination=pagination)


def ok_created(data: Optional[T] = None, message: str = "已创建") -> ResponseModel[T]:
    """201 Created 响应"""
    return ResponseModel[T](
        success=True,
        message=message,
        data=data,
        timestamp=datetime.now(timezone.utc),
    )


def ok_no_content(message: str = "无内容") -> ResponseModel[None]:
    """204 No Content 响应"""
    return ResponseModel(
        success=True,
        message=message,
        data=None,
        timestamp=datetime.now(timezone.utc),
    )


# ---------------------  失败响应  --------------------- #


def fail(
    code: int = status.HTTP_400_BAD_REQUEST,
    message: str = "请求错误",
    error_code: int = 0,
    details: Optional[Dict[str, Any] | List[Any] | str] = None,
) -> ResponseModel[None]:
    """通用错误"""
    return ResponseModel(
        success=False,
        message=message,
        error=ErrorModel(error_code=error_code, error_message=message, details=details),
        timestamp=datetime.now(timezone.utc),
    )


def fail_not_found(
    details: Optional[Dict[str, Any] | List[Any] | str] = None,
    message: str = "资源未找到",
) -> ResponseModel[Any]:
    """404 快捷函数"""
    return fail(
        code=status.HTTP_404_NOT_FOUND,
        message=message,
        details=details,
        error_code=404,
    )


def fail_unauthorized(
    details: Optional[Dict[str, Any] | List[Any] | str] = None,
    message: str = "未授权",
) -> ResponseModel[Any]:
    """401 快捷函数"""
    return fail(
        code=status.HTTP_401_UNAUTHORIZED,
        message=message,
        details=details,
        error_code=401,
    )


def fail_forbidden(
    details: Optional[Dict[str, Any] | List[Any] | str] = None,
    message: str = "禁止访问",
) -> ResponseModel[Any]:
    """403 快捷函数"""
    return fail(
        code=status.HTTP_403_FORBIDDEN,
        message=message,
        details=details,
        error_code=403,
    )


def fail_conflict(
    details: Optional[Dict[str, Any] | List[Any] | str] = None,
    message: str = "冲突",
) -> ResponseModel[Any]:
    """409 快捷函数"""
    return fail(
        code=status.HTTP_409_CONFLICT,
        message=message,
        details=details,
        error_code=409,
    )


def fail_internal_error(
    details: Optional[Dict[str, Any] | List[Any] | str] = None,
    message: str = "服务器内部错误",
) -> ResponseModel[Any]:
    """500 快捷函数"""
    return fail(
        code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=message,
        details=details,
        error_code=500,
    )


def fail_bad_request(
    details: Optional[Dict[str, Any] | List[Any] | str] = None,
    message: str = "请求错误",
) -> ResponseModel[Any]:
    """400 快捷函数"""
    return fail(
        code=status.HTTP_400_BAD_REQUEST,
        message=message,
        details=details,
        error_code=400,
    )


def fail_validation_error(
    details: Optional[Dict[str, Any] | List[Any] | str] = None,
    message: str = "验证错误",
) -> ResponseModel[Any]:
    """422 验证错误快捷函数"""
    return fail(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message=message,
        details=details,
        error_code=422,
    )
