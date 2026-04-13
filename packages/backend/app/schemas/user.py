# app/schemas/user.py
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from typing import Optional


class UserIn(BaseModel):
    username: str = Field(default=..., min_length=3, max_length=64)
    password: str = Field(default=..., min_length=6, max_length=128)
    email: EmailStr = Field(default=..., max_length=255)
    phone: Optional[str] = Field(default=None, max_length=16)


class UserOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    phone: Optional[str]

    class Config:
        from_attributes = True
