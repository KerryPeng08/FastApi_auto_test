#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: check_case_json.py
@Time: 2022/8/21-21:46
"""

# import base64
# import json
# from sqlalchemy.orm import Session
from apps.case_service import schemas
from typing import List


class CheckJson:
    """
    校验上传的测试json数据
    """

    @classmethod
    async def check_to_service(cls, case_data: List[schemas.TestCaseData]):
        keys = ['headers', 'params', 'data', 'check', 'description', 'config']
        msg_list = []
        for x in range(len(case_data)):
            # 校验字段
            msg = [key for key in keys if key not in dict(case_data[x]).keys()]
            if msg:
                msg_list.append(f"用例${x}缺少字段: {','.join(msg)}")
                continue

            # 校验check
            check = dict(case_data[x]).get('check')
            if not check:
                continue

            for k, v in check.items():
                if isinstance(v, (int, float, str, bool)):
                    continue

                if isinstance(v, list) and len(v) < 2:
                    msg_list.append(f"用例${x}比较符内容不足: {k}: {v}")
                    continue

                if v[0] not in ['<', '<=', '==', '>=', '>', 'in', 'not in']:
                    msg_list.append(f"用例${x}比较符填写错误: {k}: {v}")
                else:
                    if isinstance(v[1], (int, float)) and v[0] not in ['<', '<=', '==', '>=', '>']:
                        msg_list.append(f"用例${x}比较类型不匹配: {k}: {v}")
                        continue

                    if isinstance(v[1], list) and v[0] not in ['in', 'not in']:
                        msg_list.append(f"用例${x}比较类型不匹配: {k}: {v}")
                        continue

        if msg_list:
            return msg_list

    @classmethod
    async def check_to_ddt(cls):
        pass

    @classmethod
    async def check_to_perf(cls):
        pass
