# app/core/redis.py
from typing import Annotated

from fastapi import Depends

# import redis

from redis import asyncio as redis
from app.core.config import cfg
from app.core.logger import logger

# url = (f"redis://:{cfg.redis.password}@{cfg.redis.host}:{cfg.redis.port}/0",)
_redis_client = None


async def init_redis() -> None:
    global _redis_client
    _redis_client = redis.Redis(
        host=cfg.redis.host,
        port=cfg.redis.port,
        password=cfg.redis.password,
        db=0,
        encoding="utf-8",
        decode_responses=True,
        socket_timeout=5,
        max_connections=50,
    )
    await _redis_client.ping()  # type: ignore
    logger.info("Redis 连接池已创建")


async def close_redis() -> None:
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        logger.info("Redis 连接池已关闭")


async def get_redis() -> redis.Redis:
    if _redis_client is None:
        raise RuntimeError("Redis 尚未初始化")
    return _redis_client


RedisDep = Annotated[redis.Redis, Depends(dependency=get_redis)]
