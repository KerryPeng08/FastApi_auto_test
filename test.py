#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: test.py
@Time: 2022/8/16-16:41
"""
import json
import re

print(json.dumps([{'id': 1, 'project_name': '商城系统', 'temp_name': '满减优惠券', 'api_count': 41, 'created_at': 11111,
                   'updated_at': 1111, 'case_count': 2, 'case_info': [{'case_name': '满减优惠券-创建2', 'mode': 'service'},
                                                                      {'case_name': '满减优惠券-创建1', 'mode': 'service'}]}]
                 ))

import jsonpath

b = {
    'list': [
        {'status': 1}
    ]
}

a = jsonpath.jsonpath(b, '$.list.[0].status')

print(a)
import requests

ccc = {'method': 'POST', 'url': 'http://cloud.sales-staging.liweijia.com/security/lv_check', 'headers': {'Host': 'cloud.sales-staging.liweijia.com', 'Connection': 'keep-alive', 'Content-Length': '56', 'Cache-Control': 'no-cache', 'Upgrade-Insecure-Requests': '1', 'Origin': 'http://cloud.sales-staging.liweijia.com', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Referer': 'http://cloud.sales-staging.liweijia.com/security/auth/login?returnUrl=http%3A%2F%2Fcloud.sales-staging.liweijia.com%2F%23%2Fdashboard', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-HK,zh;q=0.9,zh-CN;q=0.8,en-US;q=0.7,en;q=0.6,zh-TW;q=0.5,ja;q=0.4', 'Pragma': 'no-cache'}, 'params': {}, 'data': {}}

res = requests.request(**ccc)
print(res)


# aaa = 'http://cloud.sales-staging.liweijia.com/services/tenant/copyright/currentCopyRight/{{2.$.result.extend.tenantId}}'
# bbb = "{{" + f"{'2.$.result.extend.tenantId'}" + "}}"
# new_url = re.sub(bbb, 'asdaasd ', aaa)
# print(new_url)