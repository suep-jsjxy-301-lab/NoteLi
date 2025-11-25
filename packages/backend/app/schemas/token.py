# app/schemas/token.py
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(default=...)
    refresh_token: str = Field(default=...)


class AccessToken(BaseModel):
    access_token: str = Field(default=...)


class RefreshToken(BaseModel):
    refresh_token: str = Field(default=...)


class TokenData(BaseModel):
    sub: str = Field(
        default=...
    )  # Changed from UUID to str to support JSON serialization
    iat: datetime = Field(default=...)
    exp: datetime = Field(default=...)
    username: str = Field(default=...)
    scope: Literal["admin", "user"] = Field(default="user")
