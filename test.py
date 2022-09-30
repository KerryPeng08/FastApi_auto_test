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


import jsonpath

a = '/MCH000143/JS000000195253'
b = '-14:'
start_index = int('a')
end_index = int(b.split(':')[1]) if b.split(':')[1] else None
print(start_index,end_index)
print(type(start_index), type(end_index))
print(a[start_index:end_index])