# app/core/lifespan.py
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import asyncio

from fastapi import FastAPI

# from app.core.config import cfg  # 统一配置入口
from app.core.logger import logger  # 统一日志

from app.core.redis import init_redis, close_redis
from app.core.tortoise import init_db, close_db
from app.models.models import User
from app.core.security import get_password_hash


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    FastAPI 0.100+ 官方推荐的 lifespan 写法。
    启动阶段：初始化数据库、线程池、缓存等；
    关闭阶段：优雅释放资源。
    """
    # ────────────── 启动 ──────────────
    logger.info("🚀 服务启动")
    await init_db()
    await init_redis()

    # 创建默认管理员用户
    admin_username = "admin"
    admin_password = "admin"  # 建议在生产环境中通过环境变量设置
    
    # 检查是否已存在管理员用户
    existing_admin = await User.filter(username=admin_username).first()
    if not existing_admin:
        hashed_password = get_password_hash(admin_password)
        await User.create(
            username=admin_username,
            password=hashed_password,
            email="admin@email.com",
            phone=None,
        )
        logger.info(f"✅ 默认管理员用户已创建: {admin_username}")
    else:
        logger.info(f"✅ 管理员用户已存在: {admin_username}")


    try:
        yield  # 开始接收请求
    except asyncio.CancelledError:
        logger.info("⚠️ 收到退出信号，开始关闭...")
    finally:
        # ────────────── 关闭 ──────────────
        logger.info("🛑 服务关闭")
        await close_db()
        await close_redis()