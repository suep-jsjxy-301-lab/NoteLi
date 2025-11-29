# app/schemas/token.py
from datetime import datetime, timezone, timedelta
from typing import Literal
from pydantic import BaseModel, Field
import uuid


def _now_ts() -> int:
    return int(datetime.now(timezone.utc).timestamp())


def _default_exp() -> int:
    # 例如：access token 15 分钟过期
    return int((datetime.now(tz=timezone.utc) + timedelta(minutes=15)).timestamp())


def _default_refresh_exp() -> int:
    # 例如：refresh token 7 天过期
    return int((datetime.now(tz=timezone.utc) + timedelta(days=7)).timestamp())


class Token(BaseModel):
    access_token: str = Field(default=...)
    refresh_token: str = Field(default=...)


class AccessToken(BaseModel):
    access_token: str = Field(default=...)


class RefreshToken(BaseModel):
    refresh_token: str = Field(default=...)


class AccessTokenData(BaseModel):
    sub: str = Field(default=...)
    iat: int = Field(default_factory=_now_ts)
    exp: int = Field(default_factory=_default_exp)
    scope: Literal["admin", "user"] = Field(default="user")


class RefreshTokenData(BaseModel):
    sub: str = Field(default=...)
    iat: int = Field(default_factory=_now_ts)
    exp: int = Field(default_factory=_default_refresh_exp)
    type: str = Field(default="refresh")
    jti: str = Field(default_factory=lambda: str(object=uuid.uuid4()))
