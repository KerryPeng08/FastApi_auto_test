#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: test.py
@Time: 2022/8/16-16:41
"""
# import json
# import re
#
# # print(json.dumps([{'id': 1, 'project_name': '商城系统', 'temp_name': '满减优惠券', 'api_count': 41, 'created_at': 11111,
# #                    'updated_at': 1111, 'case_count': 2, 'case_info': [{'case_name': '满减优惠券-创建2', 'mode': 'service'},
# #                                                                       {'case_name': '满减优惠券-创建1', 'mode': 'service'}]}]
# #                  ))
#
# import jsonpath
#
# b = {
#     'list': [
#         {'status': 1},
#         {'status': 2},
#         {'status': 3},
#         {'status': 4},
#     ]
# }
#
# a = jsonpath.jsonpath(b, '$.list.3.status', result_type='IPATH')

# print(a)

# aaa = 'http://cloud.sales-staging.liweijia.com/services/tenant/copyright/currentCopyRight/{{2.$.result.extend.tenantId}}'
# bbb = "{{" + f"{'2.$.result.extend.tenantId'}" + "}}"
# new_url = re.sub(bbb, 'asdaasd ', aaa)
# print(new_url)

import requests
import aiohttp
import asyncio

url = 'http://cloud.sales-staging.liweijia.com/api/admin/promotion'
headers = {
    "Host": "cloud.sales-staging.liweijia.com",
    "Connection": "keep-alive",
    "Content-Length": "215",
    "Site-key": "liweijia",
    "Accept": "application/json, text/plain, */*",
    "SUMBIT-SITE-KEY": "liweijia",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "http://cloud.sales-staging.liweijia.com",
    "Referer": "http://cloud.sales-staging.liweijia.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-HK,zh;q=0.9,zh-CN;q=0.8,en-US;q=0.7,en;q=0.6,zh-TW;q=0.5,ja;q=0.4",
    "Cookie": "sid=salesj6yeyxz77lh61k6uj974b5ss7.sales; LX-WXSRF-JTOKEN=1be427b8-55a8-4100-b8ea-982724f45ae5;",
    # "Cookie": "user_is_login=false; MEIQIA_TRACK_ID=1pHnOlbcCI2KBqmDLBeFvrNqXDF; MEIQIA_VISIT_ID=283Aaw07Jj3S6uFCYbtqjXvsMMV; _dataflulx_an_id=ac88f777-5eb4-42d6-8879-eca8fa5b8547; Hm_lvt_1a37d6e50dc8404e45d7ab69adee8d9f=1659402141,1659489289,1659607228,1660898280; _ga=GA1.2.1500096981.1661308743; sid=sales1dqtajr02poxmjqxd3hqfr5l.sales; LX-WXSRF-JTOKEN=f125d4db-6d1d-437e-8069-f5c635f06c50; laravel_session=NAxkeVHAqF9po3yBPX6tMbpPk2J5gKgOLdZcpXmj; _dataflux_s=rum=1&id=819ed28e-c7d6-42be-9e09-b9f56cbdc5c6&created=1662114820568&expire=1662116821079",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}

data = {
    "type": "130",
    "name": "端用户-单品秒杀-测试",
    "target": [
        "c_platform"
    ],
    "is_limit_purchase": 1,
    "banner_type": "default",
    "promote_url": "",
    "buy_restrict": 1,
    "start_at": "2022-09-01 10:45:14",
    "end_at": "2022-09-10 10:45:17"
}

data2 = {
    "type": "130",
    "name": "测试啊",
    "target": [
        "c_platform"
    ],
    "is_limit_purchase": 1,
    "banner_type": "default",
    "promote_url": "",
    "buy_restrict": 1,
    "start_at": "2022-09-01 10:45:14",
    "end_at": "2022-09-10 10:45:17"
}

import ujson
import orjson
import json


async def test():
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as sess:
        async with sess.post(
                url=url,
                headers=headers,
                json=json.dumps(data)
        ) as res:
            print(res.status)
            # print(res.headers)
            print(await res.json())
            print(res.get_encoding())


# loop = asyncio.get_event_loop()
# result = loop.run_until_complete(test())
# #
# res = requests.post(
#     url=url,
#     headers=headers,
#     json=data
# )
# print(res.status_code)
# print(res.json())
# print(res.cookies.get_dict())

import os
from setting import ALLURE_PATH


def load_allure_reports(allure_dir: str):
    """
    加载所有的allures测试报告
    :param app: 主程序
    :param allure_dir: 测试报告目录
    :return:
    """
    try:
        files = os.listdir(os.path.join(allure_dir, 'allure_plus'))
    except FileNotFoundError:
        return
    for file in files:
        file_ = os.listdir(os.path.join(allure_dir, 'allure_plus', file))
        for f in file_:
            if f == 'history.json':
                continue
            print(f)


# load_allure_reports(ALLURE_PATH)

import re
a = 'asda,{sda}'
print(re.compile(r'{(.*?)}', re.S).findall(a)[0])
print(re.sub(r'{(.*?)}', 'aa', a))
