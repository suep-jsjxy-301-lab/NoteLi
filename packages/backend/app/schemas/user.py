# app/schemas/user.py
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class UserIn(BaseModel):
    username: str = Field(default=..., min_length=3, max_length=64)
    password: str = Field(default=..., min_length=6, max_length=128)
    role: Optional[str] = Field(default="user", max_length=32)


class UserOut(BaseModel):
    id: UUID
    username: str
    role: str

    class Config:
        orm_mode = True
