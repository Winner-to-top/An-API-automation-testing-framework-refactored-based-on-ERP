import logging

import allure
import jsonpath
from utils.send_request import send_jdbc_request


@allure.step("3.HTTP响应断言")
def http_assert(case, res):
    expected = eval(case["expected"])
    if case["check"]:
        # 把断言的字段和预期结果转为列表
        print(2222222222)
        check = eval(case["check"])
        # 共同来遍历两个列表
        for c,e in zip(check,expected):
            # 获取实际结果
            result = jsonpath.jsonpath(res.json(), f"$..{c}")[0]
            logging.info(f"3.HTTP响应断言内容: 实际结果({result}) == 预期结果({e})")
            assert result == e

        # result = jsonpath.jsonpath(res.json(), case["check"])[0]
        # logging.info(f"3.HTTP响应断言内容: 实际结果({result}) == 预期结果({case['expected']})")
        # assert result == case["expected"]
    else:
        for e in expected:
            logging.info(f"3.HTTP响应断言内容: 预期结果({e}) in 实际结果({res.text})")
            assert str(e) in res.text


def jdbc_assert(case):
    if case["sql_check"] and case["sql_expected"]:
        with allure.step("3.JDBC响应断言"):
            result = send_jdbc_request(case["sql_check"])
            logging.info(f"3.JDBC响应断言内容: 实际结果({result}) == 预期结果({case['sql_expected']})")
            assert result == case["sql_expected"]
