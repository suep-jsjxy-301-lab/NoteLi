from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteCreateIn(BaseModel):
    category_id: int = Field(..., ge=1, le=24, description="分类ID（业务ID，同图标编号）")
    title: str = Field("", max_length=255, description="笔记标题（可为空字符串）")
    content: str = Field("", description="笔记内容（可为空字符串）")
    tags: list[str] = Field(default_factory=list, description="标签列表")
    starred: bool = Field(default=False, description="是否星标")


class NoteOut(BaseModel):
    id: int
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    title: str
    content: str
    tags: list[str]
    starred: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NoteUpdateIn(BaseModel):
    id: int = Field(..., ge=1, description="笔记ID")
    category_id: int = Field(..., ge=1, le=24, description="分类ID（业务ID，同图标编号）")
    title: str = Field("", max_length=255, description="笔记标题")
    content: str = Field("", description="笔记内容")
    tags: list[str] = Field(default_factory=list, description="标签列表")
    starred: bool = Field(default=False, description="是否星标")

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteCreateIn(BaseModel):
    category_id: Optional[int] = Field(..., ge=1, le=24, description="分类ID（业务ID，同图标编号）")
    title: str = Field("", max_length=255, description="笔记标题（可为空字符串）")
    content: str = Field("", description="笔记内容（可为空字符串）")
    tags: list[str] = Field(default_factory=list, description="标签列表")
    starred: bool = Field(default=False, description="是否星标")


class NoteOut(BaseModel):
    id: int
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    title: str
    content: str
    tags: list[str]
    starred: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NoteUpdateIn(BaseModel):
    id: int = Field(..., ge=1, description="笔记ID")
    category_id: int = Field(..., ge=1, le=24, description="分类ID（业务ID，同图标编号）")
    title: str = Field("", max_length=255, description="笔记标题")
    content: str = Field("", description="笔记内容")
    tags: list[str] = Field(default_factory=list, description="标签列表")
    starred: bool = Field(default=False, description="是否星标")

