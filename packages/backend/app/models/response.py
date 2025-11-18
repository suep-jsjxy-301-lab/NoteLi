# app/models/response.py
"""
app.models.response 的 Docstring

该模块定义了响应模型，用于标准化API响应格式。
"""

from datetime import datetime, timezone
from typing import Any, Optional
from pydantic import BaseModel, Field


class ErrorModel(BaseModel):
    """
    标准API错误响应模型

    Attributes:
        error_code (int): 错误代码
        error_message (str): 错误消息内容
        details (Optional[Any]): 错误详情信息
    """

    error_code: int = Field(..., description="错误代码", alias="code")
    error_message: str = Field(..., description="错误消息内容", alias="message")
    details: Optional[Any] = Field(None, description="错误详情信息")


class PaginationModel(BaseModel):
    """
    分页响应模型

    Attributes:
        total_item (int): 总记录数
        total_pages (int): 总页数
        page (int): 当前页码
        size (int): 每页记录数
    """

    total_item: int = Field(..., description="总记录数")
    total_pages: int = Field(..., description="总页数")
    page: int = Field(..., description="当前页码")
    size: int = Field(..., description="每页记录数")


class ResponseModel(BaseModel):
    """
    标准API响应模型

    Attributes:
        success (bool): 操作是否成功
        message (str): 响应消息内容
        data (Optional[Any]): 响应数据内容
        error (Optional[ErrorModel]): 错误信息(可选)
        pagination (Optional[PaginationModel]): 分页信息(可选)
        timestamp (datetime): 响应时间戳
    """

    success: bool = Field(..., description="操作是否成功")
    message: str = Field(..., description="响应消息内容")
    data: Optional[Any] = Field(default=None, description="响应数据内容")
    error: Optional[ErrorModel] = Field(
        default=None, description="错误信息(可选)", alias="error_info"
    )
    pagination: Optional[PaginationModel] = Field(
        default=None, description="分页信息(可选)"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now(timezone.utc), description="响应时间戳"
    )
