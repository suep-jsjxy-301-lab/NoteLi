# app/core/config.py
import os
import tomllib
from string import Template
from pathlib import Path
from typing import Final

import dotenv
from pydantic import BaseModel, Field, field_validator

TOML_PATH: Final = Path(__file__).parent.parent.with_name("config.toml")
LOG_LEVELS: Final = {
    "TRACE",
    "DEBUG",
    "INFO",
    "SUCCESS",
    "WARNING",
    "ERROR",
    "CRITICAL",
}


class CommonCfg(BaseModel):
    timezone: str = "Asia/Shanghai"


# class DbCfg(BaseModel):
#     url: str
#     pool_size: int = 10


class LogCfg(BaseModel):
    level: str = Field(default="INFO", description="控制台日志级别")
    file_level: str = Field(default="WARNING", description="磁盘日志级别")
    rotation: str = "10 MB"
    retention: int = 5

    # ---------- 统一校验 ----------
    @field_validator("level", "file_level", mode="before")
    @classmethod
    def _check_level(cls, v: str) -> str:
        lv = v.upper().strip()
        if lv not in LOG_LEVELS:
            raise ValueError(f"非法日志级别 {v!r}，允许值: {LOG_LEVELS}")
        return lv


class RedisCfg(BaseModel):
    host: str = Field(default="localhost", description="Redis 服务地址")
    port: int = Field(default=6379, description="Redis 端口")
    password: str = Field(
        default="${REDIS_PASSWORD}",
        description="Redis 密码；优先读取环境变量 ${REDIS_PASSWORD}",
    )


class JWTCfg(BaseModel):
    secret_key: str = "${JWT_SECRET_KEY}"  # 256-bit hex，openssl rand -hex 32
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


class Config(BaseModel):
    common: CommonCfg = CommonCfg()
    # db: DbCfg = DbCfg()
    log: LogCfg = LogCfg()
    redis: RedisCfg = RedisCfg()
    jwt: JWTCfg = JWTCfg()


# ------------------ 单例 ------------------
def load_cfg() -> Config:
    env_path = TOML_PATH.with_name(".env")
    dotenv.load_dotenv(env_path, override=True)
    raw = TOML_PATH.read_text(encoding="utf-8")
    # 把 ${REDIS_PASSWORD} 等全部替换
    resolved = Template(raw).safe_substitute(os.environ)
    return Config.model_validate(tomllib.loads(resolved))


cfg: Config = load_cfg()
