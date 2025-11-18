from datetime import datetime
import pytz

from langchain.tools import tool

from app.core.config import cfg


@tool
def get_current_time_tool(
    timezone: str = cfg.common.timezone, fmt: str = "default"
) -> str:
    """
    获取指定时区的当前时间，支持多种格式。

    Args:
        timezone (str): 时区字符串，如 'Asia/Shanghai'。
        fmt (str): 预设格式名，可选值：
                   default | iso | date | time | datetime_cn | datetime_en | rfc2822 | unix
                   也可直接传 strftime 自定义格式，例如 "%Y年%m月%d日 %H:%M"

    Returns:
        str: 格式化后的当前时间字符串。
    """
    return get_current_time(timezone, fmt)


def get_current_time(timezone: str = cfg.common.timezone, fmt: str = "default") -> str:
    """
    获取指定时区的当前时间，支持多种格式。

    Args:
        timezone (str): 时区字符串，如 'Asia/Shanghai'。
        fmt (str): 预设格式名，可选值：
                   default | iso | date | time | datetime_cn | datetime_en | rfc2822 | unix
                   也可直接传 strftime 自定义格式，例如 "%Y年%m月%d日 %H:%M"

    Returns:
        str: 格式化后的当前时间字符串。
    """
    try:
        tz = pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        return f"未知时区: {timezone}"

    now = datetime.now(tz)

    # 预设格式表
    presets = {
        "default": "%Y-%m-%d %H:%M:%S %Z",  # 2025-11-17 23:08:05 CST
        "iso": "%Y-%m-%dT%H:%M:%S%z",  # 2025-11-17T23:08:05+0800
        "date": "%Y-%m-%d",  # 2025-11-17
        "time": "%H:%M:%S",  # 23:08:05
        "datetime_cn": "%Y年%m月%d日 %H:%M",  # 2025年11月17日 23:08
        "datetime_en": "%d %b %Y %H:%M:%S",  # 17 Nov 2025 23:08:05
        "rfc2822": "%a, %d %b %Y %H:%M:%S %z",  # Sun, 17 Nov 2025 23:08:05 +0800
        "unix": str(int(now.timestamp())),  # 1742466485
    }

    fmt_str = presets.get(fmt, fmt)
    try:
        return now.strftime(fmt_str)
    except Exception as e:
        return f"格式错误: {e}"


if __name__ == "__main__":
    # 测试示例
    print(get_current_time("Asia/Shanghai", "default"))
    print(get_current_time("America/New_York", "iso"))
    print(get_current_time("Europe/London", "%Y/%m/%d %H-%M-%S"))
    print(get_current_time("Invalid/Timezone", "default"))
