#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: test.py
@Time: 2022/8/16-16:41
"""
import json
import re

# print(json.dumps([{'id': 1, 'project_name': '商城系统', 'temp_name': '满减优惠券', 'api_count': 41, 'created_at': 11111,
#                    'updated_at': 1111, 'case_count': 2, 'case_info': [{'case_name': '满减优惠券-创建2', 'mode': 'service'},
#                                                                       {'case_name': '满减优惠券-创建1', 'mode': 'service'}]}]
#                  ))

import jsonpath

b = {
    'list': [
        {'status': 1},
        {'status': 2},
        {'status': 3},
        {'status': 4},
    ]
}

a = jsonpath.jsonpath(b, '$.list.3.status', result_type='IPATH')

print(a)

# aaa = 'http://cloud.sales-staging.liweijia.com/services/tenant/copyright/currentCopyRight/{{2.$.result.extend.tenantId}}'
# bbb = "{{" + f"{'2.$.result.extend.tenantId'}" + "}}"
# new_url = re.sub(bbb, 'asdaasd ', aaa)
# print(new_url)