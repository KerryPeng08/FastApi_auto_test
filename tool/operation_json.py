#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: operation_json.py
@Time: 2022/8/19-23:55
"""

import json


class OperationJson:

    @staticmethod
    async def write(path: str, data: dict):
        with open(path, 'w', encoding='utf-8') as w:
            w.write(json.dumps(data, indent=2, ensure_ascii=False))
