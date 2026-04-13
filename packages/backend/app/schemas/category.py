# app/schemas/category.py
from pydantic import BaseModel, Field
from uuid import UUID

class CategoryIn(BaseModel):
    user_id: UUID = Field(default=...)
    category_id: int = Field(default=..., ge=1, le=24)
    category_name: str = Field(default=..., max_length=6)

class CategoryOut(BaseModel):
    category_id: int
    category_name: str

    class Config:
        orm_mode = True