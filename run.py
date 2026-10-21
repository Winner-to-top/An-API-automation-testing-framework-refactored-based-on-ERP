import os
import sys
import logging

import pytest

from config.env_manager import apply_environment

SUPPORTED_ENVS = ("test", "prod")
USAGE = "请传入正确的执行命令：python run.py test 或者 python run.py prod"

if __name__ == "__main__":

    print(sys.argv)

    if len(sys.argv) != 2 or sys.argv[1] not in SUPPORTED_ENVS:
        logging.error(USAGE)
        sys.exit(1)

    try:
        # 从 config/local_config.py 或环境变量中注入 URL / DB / ENV
        apply_environment(sys.argv[1])
    except RuntimeError as e:
        logging.error(e)
        sys.exit(1)

    pytest.main(["-vs", "./testcases/test_runner.py", "--alluredir", "./report/json_report", "--clean-alluredir"])
    os.system("allure generate ./report/json_report -o ./report/html_report --clean")

    from utils.send_feishu_msg import send_feishu_message
    # 发送测试报告消息
    send_feishu_message()
