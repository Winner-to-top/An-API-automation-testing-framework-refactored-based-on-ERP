# -*- coding: utf-8 -*-
"""全局配置。

敏感信息（数据库账号、飞书 Webhook、报告地址）优先从环境变量读取，
其次读取未提交到 Git 的 config/local_config.py。
"""

import os

try:
    from config.local_config import FEISHU_WEBHOOK as LOCAL_FEISHU_WEBHOOK
    from config.local_config import REPORT_PATHS as LOCAL_REPORT_PATHS
except ImportError:
    LOCAL_FEISHU_WEBHOOK = ""
    LOCAL_REPORT_PATHS = {}

# excel格式的测试用例文件配置
EXCEL_FILE = "./data/测试用例完整版.xlsx"
SHEET_NAME = "Sheet1"

# mysql资源销毁
SQL1 = 'SELECT * from base_data_product ORDER BY create_time desc;'
SQL2 = 'SELECT * from base_data_product ORDER BY create_time desc;'

# 飞书相关的配置文件
# webhook地址：优先环境变量 FEISHU_WEBHOOK
WEBHOOK = os.environ.get("FEISHU_WEBHOOK") or LOCAL_FEISHU_WEBHOOK

# 项目名称
PROJECT = os.environ.get("PROJECT_NAME", "星云ERP")

# 是否发送飞书消息的开关
FEISHU_IS_SEND = os.environ.get("FEISHU_IS_SEND", "true").lower() in ("1", "true", "yes")

# 当前执行环境
CURRENT_ENV = os.environ.get("ENV", "test")

# 测试报告的地址：优先环境变量 REPORT_PATH
REPORT_PATH = os.environ.get("REPORT_PATH") or LOCAL_REPORT_PATHS.get(CURRENT_ENV, "")
