# -*- coding:utf-8 -*-
# 北梦测教育
# 课程咨询加微信：xiaobeiceshi
import logging

import requests
from config.config import *
import time

def send_feishu_message():
    message_data = [
        [
            {
                "tag": "text",
                "text": f"项目名称：{PROJECT}"
            }
        ],
        [
            {
                "tag": "text",
                "text": f"执行时间：{time.strftime('%Y-%m-%d %H:%M:%S')}"
            }
        ]
    ]

    # 配置了报告地址时才添加报告链接
    if REPORT_PATH:
        message_data.append([
            {
                "tag": "text",
                "text": "详细信息："
            },
            {
                "tag": "a",
                "text": "查看测试报告",
                "href": REPORT_PATH
            }
        ])

    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "自动化测试报告",
                    "content": message_data
                }
            }
        }
    }
    # 开关关闭或未配置 Webhook 时跳过发送
    if not FEISHU_IS_SEND:
        return None
    if not WEBHOOK:
        logging.warning("未配置飞书 Webhook（FEISHU_WEBHOOK），已跳过消息推送")
        return None

    response = requests.post(WEBHOOK, json=payload)
    return response


if __name__ == '__main__':
    send_feishu_message()

#
# # 1.导入requests
# import requests
#
# # 2.定义webhook地址
# webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/your-webhook-id"
#
# # 3.构造富文本消息
# # "tag":"text"表示文本内容
# #  "tag":"a", 表示的是超链接
# # "href":"https://www.baidu.com/"  表示超链接的跳转地址
# message_data = [
#     [
#         {
#             "tag": "text",
#             "text": "星云ERP项目"
#         }
#     ],
#     [
#         {
#             "tag": "a",
#             "text": "查看测试报告",
#             "href": "https://www.baidu.com/"
#         }
#     ]
# ]
#
# # 4.构建最终的消息体
# payload = {
#     "msg_type": "post",
#     "content": {
#         "post": {
#             "zh_cn": {
#                 "title": "自动化测试报告",
#                 "content": message_data
#             }
#         }
#     }
# }
#
# # 5.发送消息
# response = requests.post(webhook, json=payload)
#
# print(response)
# print(response.text)
