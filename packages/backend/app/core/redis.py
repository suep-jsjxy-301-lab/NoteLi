# app/core/redis.py
from typing import Annotated

from fastapi import Depends

from redis import asyncio as redis
from app.core.config import cfg
from app.core.logger import logger

r: redis.Redis | None = None


async def init_redis() -> None:
    global r
    r = redis.from_url( # type: ignore
        f"redis://:{cfg.redis.password}@{cfg.redis.host}:{cfg.redis.port}/0",
        encoding="utf-8",
        decode_responses=True,
        max_connections=20,
    )
    await r.ping() # type: ignore
    logger.info("Redis 连接池已创建")


async def close_redis() -> None:
    global r
    if r:
        await r.aclose()
        logger.info("Redis 连接池已关闭")


async def get_redis() -> redis.Redis:
    if r is None:
        raise RuntimeError("Redis 尚未初始化")
    return r


RedisDep = Annotated[redis.Redis, Depends(get_redis)]
