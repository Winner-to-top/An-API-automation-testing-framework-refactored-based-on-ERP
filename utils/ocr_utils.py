# -*- coding:utf-8 -*-
# 北梦测教育
# 课程咨询加微信：xiaobeiceshi
# pip install ddddocr
import os
import ddddocr
import base64
import requests
import jsonpath


def get_auth_captcha():
    """获取验证码的接口"""
    payload = {
        "method":"get",
        "url":os.environ["URL"] + "/auth/captcha"
    }
    response = requests.request(**payload).json()
    sn = jsonpath.jsonpath(response,"$..sn")[0]
    image = jsonpath.jsonpath(response,'$..image')[0]
    return sn,image

def dddd_ocr_text(image):
    # 步骤1.需要对image进行分割，得到头部和Base64编码的部分
    encode_data = image.split(",")[1]

    # 步骤2：解码Base64元数据
    decode_data = base64.b64decode(encode_data)

    # 步骤3：通过ddddocr来识别图片元数据
    ocr = ddddocr.DdddOcr()     # 实例化
    text = ocr.classification(decode_data)
    return text

# 存放全局的验证码文本和sn文本
sn_captcha_text = {}

# 执行次数
run_nums = 0


def get_res_sn_captcha():
    """获取验证码和sn的最终方法"""

    # 如果是生产环境，按照下面的逻辑走，先请求数据，再调用ocr识别
    if os.environ["ENV"] == "prod":
        global run_nums

        # 判断第一次执行的时候和失败重试的时候才会执行下面的获取验证码和sn的逻辑
        if not sn_captcha_text or run_nums % 2 == 0:
            sn,image = get_auth_captcha()
            captcha = dddd_ocr_text(image)
            sn_captcha_text["sn"] = sn
            sn_captcha_text["captcha"] = captcha

        run_nums += 1

        return sn_captcha_text

    # 测试环境按照下面的执行逻辑进行执行
    elif os.environ["ENV"] == "test":
        sn = get_auth_captcha()[0]
        # captcha = dddd_ocr_text(image)
        sn_captcha_text["sn"] = sn
        sn_captcha_text["captcha"] = "aaaa"
        return sn_captcha_text


if __name__ == '__main__':
    image = "data:image/jpeg;base64,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"
    # text = dddd_ocr_text(image)
    # print(text)

    str1 = "dddd_ocr_text(image)"
    print(str1)
    print(eval(str1))

    # print(get_auth_captcha())
    print(get_res_sn_captcha())
    print(get_res_sn_captcha())