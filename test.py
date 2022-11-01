#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: test.py
@Time: 2022/8/16-16:41
"""
import requests
import aiohttp
import asyncio

data = {
    "url": "http://xpkj.sales.liweijia.com/services/member/distributor/pageSelection",
    "method": "POST",
    "headers": {
        "Host": "xpkj.sales.liweijia.com",
        "Connection": "keep-alive",
        "Content-Length": "92",
        "Site-key": "xingpankeji",
        "Accept": "application/json, text/plain, */*",
        "SUMBIT-SITE-KEY": "xingpankeji",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "http://xpkj.sales.liweijia.com",
        "Referer": "http://xpkj.sales.liweijia.com/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-HK,zh;q=0.9,zh-CN;q=0.8,en-US;q=0.7,en;q=0.6,zh-TW;q=0.5,ja;q=0.4",
        "Cookie": "LX-WXSRF-JTOKEN=cff99dd2-c77f-4b21-98bc-69009bc326a7; sid=node_sales_api13pe8wcqdwx4t11f8c5nptl6h5.node_sales_api; ",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    },
    "params": {},
    "json": {
        "start": 0,
        "limit": 1,
        "order": "DESC",
        "sort": "id",
        "siteOpenStatus": None,
        "queryCustomer": False
    }
}


async def test():
    async with aiohttp.ClientSession() as sess:
        async with sess.request(
                **data
        ) as res:
            print(res.status)
            # print(res.headers)
            print(await res.json())
            # print(res.get_encoding())
            print(res.cookies.items())


# loop = asyncio.get_event_loop()
# result = loop.run_until_complete(test())
#
# res = requests.request(
#     **data
# )
# print(res.status_code)
# print(res.json())
# print(res.cookies.get_dict())


# from apps.case_service.tool.docr import ocr_code
#
# code = ocr_code(url='http://test.allinpay.com/sso/captcha.jpg')
# print(code)

import requests
import re

headers = {
    'cookie': 'JSESSIONID=C1EADCBF531E0EB2D34775559625C5AC'
}

res = requests.post(url='http://test.allinpay.com/yunst-boss/amsVerificationcode',
                    data={
                        "isQuery": 'isQuery',
                        "createTimeBegin": '2022-10-27',
                        "phone": '17388829992',
                        'pageNum': '1',
                        'numPerPage': '1'
                    },
                    headers=headers
                    )

print(res.status_code)
print(res.text)
print(re.findall('<td width="130" align="center">(.*?)</td>	', res.text))
