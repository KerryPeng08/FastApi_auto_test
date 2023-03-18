#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: test.py
@Time: 2022/8/16-16:41
"""

import json
import base64
# import requests
import aiohttp
import asyncio

from aiohttp import FormData


# def read_har():
#     with open('C:\\Users\\My_Jie\\Desktop\\自动化文件\\文件上传.har', 'r') as r:
#         a = json.loads(r.read())
#         return a['log']['entries'][0]['request']['postData']['params'][0]
#
#
# file_data = read_har()
# # print(file_data['name'])
#
#
# data_ = FormData()
#
# file_data2 = {
#     'name': file_data['name'],
#     # 'value': base64.b64decode(file_data['value'].encode('utf-8')),
#     'value': file_data['value'],
#     'content_type': file_data['contentType'],
#     'filename': file_data['fileName']
# }
#
# # file_data2 = {
# #     'file': 'file',
# #     'title': open('C:\\Users\\My_Jie\\Desktop\\oms2.2.2\\test-11-01.json', 'rb')
# # }
#
# # print(file_data2)
# data_.add_field(**file_data2)
#
# data = {
#     "url": "http://cloud.sales-staging.liweijia.com/services/upload/order",
#     "method": "POST",
#     "headers": {
#         "Host": "cloud.sales-staging.liweijia.com",
#         "Connection": "keep-alive",
#         # "Content-Length": "92",
#         "Site-key": "liweijia",
#         "Accept": "*/*",
#         # "SUMBIT-SITE-KEY": "xingpankeji",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
#         # "Content-Type": "multipart/form-data;",
#         "Origin": "http://cloud.sales-staging.liweijia.com",
#         "Referer": "http://cloud.sales-staging.liweijia.com/",
#         "Accept-Encoding": "gzip, deflate",
#         "Accept-Language": "zh-HK,zh;q=0.9,zh-CN;q=0.8,en-US;q=0.7,en;q=0.6,zh-TW;q=0.5,ja;q=0.4",
#         "Cookie": "sid=sales1akvhim14q4ym1p8xmbqbhzakm.sales; LX-WXSRF-JTOKEN=80d039ae-3c9d-4508-8bc6-6f4891683011; ",
#         # "Pragma": "no-cache",
#         # "Cache-Control": "no-cache"
#     },
#     "data": data_,
#     # "data": {
#     #     'file': open('C:\\Users\\My_Jie\\Desktop\\oms2.2.2\\test-11-01.json', 'rb'),
#     #     'title': 'test-11-01.json'
#     # },
# }

#
# async def test():
#     async with aiohttp.ClientSession() as sess:
#         async with sess.request(
#                 **data
#         ) as res:
#             print(res.status)
#             # print(res.headers)
#             print(await res.json(content_type=None))
#             # res.text()
#             # print(res.get_encoding())
#             print(res.cookies.items())


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

# import requests
# import re
#
# headers = {
#     'cookie': 'JSESSIONID=C1EADCBF531E0EB2D34775559625C5AC'
# }
#
# res = requests.post(url='http://test.allinpay.com/yunst-boss/amsVerificationcode',
#                     data={
#                         "isQuery": 'isQuery',
#                         "createTimeBegin": '2022-10-27',
#                         "phone": '17388829992',
#                         'pageNum': '1',
#                         'numPerPage': '1'
#                     },
#                     headers=headers
#                     )
#
# print(res.status_code)
# print(res.text)
# print(re.findall('<td width="130" align="center">(.*?)</td>	', res.text))
# import time
# import hashlib
# import secrets
#
# secret_generator = secrets.SystemRandom()
# secret_generator.randint(1, 100)
#
# a = []
# for x in range(100):
#     t = time.time()
#     # print(t)
#     tr = str(t + secret_generator.randint(1, 100))
#     m = hashlib.md5(tr.encode('utf-8')).hexdigest()
#     if m not in a:
#         a.append(m)
#     else:
#         print(m)
#     # print(m)

import ast

# print(ast.literal_eval('1 + 2'))
print(eval('(1%2)*3.333333'))