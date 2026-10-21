import logging
import os
import allure
from utils.ocr_utils import get_res_sn_captcha

@allure.step("1.解析请求数据")
def analyse_case(case):
    method = case["method"]
    # 从环境变量中获取url
    url = os.environ["URL"] + case["path"]
    hearders = eval(case["headers"]) if isinstance(case["headers"], str) else None
    params = eval(case["params"]) if isinstance(case["params"], str) else None
    data = eval(case["data"]) if isinstance(case["data"], str) else None
    # data = {"username":"1000@admin","password":"admin","sn":get_res_sn_captcha()[0],"captcha":get_res_sn_captcha()[1]}
    json = eval(case["json"]) if isinstance(case["json"], str) else None
    files = eval(case["files"]) if isinstance(case["files"], str) else None
    request_data = {
        "method": method,
        "url": url,
        "headers": hearders,
        "params": params,
        "data": data,
        "json": json,
        "files": files,
    }
    logging.info(f"1.解析请求数据, 请求数据为: {request_data}")
    allure.attach(f"{request_data}", name="解析数据结果")
    return request_data
