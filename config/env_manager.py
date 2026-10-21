# -*- coding: utf-8 -*-
"""执行环境管理：从本地配置读取环境信息并注入环境变量。"""

import os

try:
    from config.local_config import ENVIRONMENTS
except ImportError:  # 未创建本地配置时，仅允许通过环境变量运行
    ENVIRONMENTS = {}


def apply_environment(env_name):
    """将指定环境的 URL / DB / ENV 写入环境变量。

    优先级：已存在的环境变量 > config/local_config.py > 报错提示。
    这样在 CI 中可以直接通过环境变量注入，无需本地配置文件。
    """
    env_config = ENVIRONMENTS.get(env_name, {})

    if not env_config and not (os.environ.get("URL") and os.environ.get("DB")):
        raise RuntimeError(
            f"未找到环境 [{env_name}] 的配置。\n"
            f"请先复制 config/local_config.example.py 为 config/local_config.py 并填写实际配置，\n"
            f"或通过环境变量 URL / DB 注入连接信息。"
        )

    if "URL" in env_config:
        os.environ.setdefault("URL", env_config["URL"])
    if "DB" in env_config:
        os.environ.setdefault("DB", str(env_config["DB"]))

    os.environ["ENV"] = env_name
