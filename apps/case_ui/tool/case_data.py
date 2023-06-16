#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: case_data.py
@Time: 2023/6/16-10:23
"""

import re
from apps.case_ui import schemas


async def get_row_data(temp_info: schemas.PlaywrightOut):
    """
    处理text文本数据
    :param temp_info:
    :return:
    """
    data_list = temp_info.text.split('\n')

    result = []
    for i, data in enumerate(data_list):
        if '{{' in data and "}}" in data:
            for x in re.findall(r"{{(.*?)}}", data):
                result.append({'row': i, 'data': x})

    return result
