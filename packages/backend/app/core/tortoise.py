# app/core/tortoise.py
from typing import Any
from tortoise import Tortoise

# from app.core.config import cfg
from app.core.logger import logger


# 如果只想本地写死，也可以直接在这里写 CONFIG，但推荐走 settings。
TORTOISE_ORM: dict[str, Any] = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": "database/db.sqlite3"},
        }
    },
    "apps": {
        "models": {
            "models": [
                "app.models.models",
                # "aerich.models",
            ],  # ["app.models.models", "aerich.models"]
            "default_connection": "default",
        },
    },
}


async def init_db() -> None:
    """初始化 Tortoise ORM 并生成 schema（仅开发/测试环境自动建表）"""
    await Tortoise.init(config=TORTOISE_ORM)
    # if settings.auto_generate_schemas:
    #     await Tortoise.generate_schemas(safe=True)
    await Tortoise.generate_schemas(safe=True)
    logger.info("Tortoise-ORM 连接数据库成功")


async def close_db() -> None:
    await Tortoise.close_connections()
    logger.info("Tortoise-ORM 连接关闭")
