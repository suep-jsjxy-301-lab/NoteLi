# app/models/response.py
"""
app.models.response 的 Docstring

该模块定义了响应模型，用于标准化API响应格式。
"""

from datetime import datetime, timezone
from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel, Field, model_validator


class ErrorModel(BaseModel):
    """
    标准API错误响应模型

    Attributes:
        error_code (int): 错误代码
        error_message (str): 错误消息内容
        details (Optional[Any]): 错误详情信息
    """

    error_code: int = Field(..., description="错误代码")
    error_message: str = Field(..., description="错误消息内容")
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


T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
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
    data: Optional[T] = Field(default=None, description="响应数据内容")
    error: Optional[ErrorModel] = Field(
        default=None, description="错误信息(可选)"
    )
    pagination: Optional[PaginationModel] = Field(
        default=None, description="分页信息(可选)"
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="响应时间戳"
    )

    @model_validator(mode="after")
    def check_consistency(self):
        if self.success and self.error:
            raise ValueError("success=True 时不应包含 error")
        if not self.success and not self.error:
            raise ValueError("success=False 时应包含 error")
        return self
