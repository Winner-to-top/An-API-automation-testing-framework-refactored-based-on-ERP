# -*- coding: utf-8 -*-
"""
本地环境配置模板。

使用方法：
1. 复制本文件为 config/local_config.py；
2. 按实际情况填写各环境的接口地址、数据库连接信息、飞书 Webhook 与报告地址；
3. config/local_config.py 已被 .gitignore 忽略，不会提交到 Git。

也可以通过环境变量覆盖这里的配置：
URL / DB / ENV / FEISHU_WEBHOOK / FEISHU_IS_SEND / PROJECT_NAME / REPORT_PATH
"""

# 各执行环境的配置
ENVIRONMENTS = {
    "test": {
        "URL": "http://your-test-host:9005",
        "DB": {
            "host": "your-mysql-host",
            "port": 3306,
            "database": "xingyun",
            "user": "root",
            "password": "your-password",
        },
    },
    "prod": {
        "URL": "http://your-prod-host:9002/api/cloud-api",
        "DB": {
            "host": "your-mysql-host",
            "port": 3306,
            "database": "xingyun",
            "user": "root",
            "password": "your-password",
        },
    },
}

# 飞书群机器人 Webhook 地址
FEISHU_WEBHOOK = ""

# 各环境的测试报告地址
REPORT_PATHS = {
    "test": "http://your-jenkins-host/view/all/job/your_job/allure/",
    "prod": "http://your-jenkins-host/job/your_prod_job/allure/",
}
