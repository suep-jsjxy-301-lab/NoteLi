# app/core/config.py
from pathlib import Path
from typing import Final
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


class Config(BaseModel):
    common: CommonCfg = CommonCfg()
    # db: DbCfg = DbCfg()
    log: LogCfg = LogCfg()


# ------------------ 单例 ------------------
def load_cfg() -> Config:
    import tomllib

    with TOML_PATH.open("rb") as f:
        return Config.model_validate(tomllib.load(f))


cfg: Config = load_cfg()  # 全局可直接导入
