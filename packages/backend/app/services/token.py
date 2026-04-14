"""
Token 服务 - 负责签发 access/refresh token
依赖：core/security 纯算法 + 业务 User 对象
"""

import time
from fastapi import HTTPException, status
from datetime import timedelta, timezone
from datetime import datetime
from typing import Any, Dict, Literal
from uuid import UUID

from redis.asyncio.client import Redis

from app.core.security import create_token, decode_token
from app.core.redis import get_redis
from app.core.config import cfg

# from app.core.logger import logger
from app.schemas.token import AccessTokenData, RefreshTokenData
from app.models.models import User  # 仅用于类型注解
from app.repositories import *

ACCESS_TOKEN_EXPIRE_MINUTES: int = cfg.jwt.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS: int = cfg.jwt.refresh_token_expire_days


class TokenService:
    @staticmethod
    async def create_access_token(
        user: User, expires_delta: timedelta | None = None
    ) -> str:
        """
        为指定用户签发 access-token
        :param user: 已查询出的 User 模型实例
        :param expires_delta: 自定义过期时长，默认读取配置
        :return: JWT 字符串
        """
        scope: Literal["admin", "user"] = "admin" if user.username == "admin" else "user"
        iat: datetime = datetime.now(tz=timezone.utc)
        exp: datetime = iat + (
            expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        data: dict[str, Any] = AccessTokenData(
            sub=str(object=user.id),
            iat=int(iat.timestamp()),
            exp=int(exp.timestamp()),
            scope=scope,
        ).model_dump()
        return create_token(payload=data, exp_delta=exp - iat)  # 已经计算好间隔

    @staticmethod
    async def create_refresh_token(sub: UUID | str) -> str:
        """
        签发 refresh-token
        :param sub: 用户主键（UUID 或 str）
        :return: JWT 字符串
        """
        iat: datetime = datetime.now(tz=timezone.utc)
        exp: datetime = datetime.now(timezone.utc) + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
        data: dict[str, Any] = RefreshTokenData(
            sub=str(object=sub) if isinstance(sub, UUID) else sub,
            iat=int(iat.timestamp()),
            exp=int(exp.timestamp()),
            type="refresh",  # 可额外声明类型，便于校验
        ).model_dump()
        return create_token(payload=data, exp_delta=exp - datetime.now(tz=timezone.utc))

    @staticmethod
    async def revoke_refresh_token(refresh_token: str) -> None:
        """
        把 refresh-token 加入 Redis 黑名单，过期时间与 token.exp 一致
        """
        try:
            payload: Dict[str, Any] = decode_token(refresh_token)
            data = RefreshTokenData(**payload)
        except Exception:
            return

        now = time.time()
        if data.exp <= now:
            # token 已过期，无需加入黑名单
            return
        ttl = data.exp - now
        try:
            r: Redis = await get_redis()
        except RuntimeError:
            # Redis 降级模式下，跳过 refresh token 黑名单写入
            return
        await r.setex(name=f"blacklist:rt:jti:{data.jti}", time=int(ttl), value=1)

    @staticmethod
    async def is_refresh_token_blacklisted_by_jti(jti: str) -> bool:
        """
        根据 jti 检查 refresh token 是否在黑名单中。
        """
        if not jti:
            return False
        try:
            r: Redis = await get_redis()
        except RuntimeError:
            # Redis 降级模式下，视为“未被拉黑”
            return False
        key = f"blacklist:rt:jti:{jti}"
        exists = await r.exists(key)
        return bool(exists)

    @staticmethod
    async def validate_refresh_token(refresh_token: str) -> User:
        """
        校验 refresh_token 并返回对应用户。
        只 decode 一次 token，避免重复解析。
        """
        from app.core.security import decode_token
        from app.services.token import TokenService

        exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

        # Step 1: 解码一次
        try:
            payload: Dict[str, Any] = decode_token(refresh_token)
        except Exception:
            raise exc

        # Step 2: 检查 type
        if payload.get("type") != "refresh":
            raise exc

        # Step 3: 提取 jti 和 sub
        jti = payload.get("jti")
        user_id = payload.get("sub")
        if not user_id or not isinstance(user_id, (str, UUID)):
            raise exc

        # Step 4: 检查黑名单（使用 jti）
        if jti and await TokenService.is_refresh_token_blacklisted_by_jti(jti):
            raise exc

        # Step 5: 查询用户
        user: User | None = await Repository.user.get_user_by_id(user_id)
        if user is None:
            raise exc

        return user
