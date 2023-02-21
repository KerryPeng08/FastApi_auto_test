#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: rep_case_data_value.py
@Time: 2023/2/16-10:28
"""

import re


def rep_value(json_data: dict, old_str: str, new_str: str) -> dict:
    """

    :param json_data:
    :param old_str:
    :param new_str:
    :return:
    """

    def handle_value(data_json):
        target = {}
        for k, v in data_json.items():

            if not isinstance(v, (list, dict)):
                if v == old_str:
                    target[k] = new_str
                else:
                    target[k] = v
                continue
            if isinstance(v, dict):
                target[k] = handle_value(v)
                continue
            if isinstance(v, list):
                new_list = []
                for x in v:
                    new_list.append(handle_value(x))
                target[k] = new_list
                continue
        return target

    return handle_value(json_data)


def rep_url(url: str, old_str: str, new_str: str, ) -> str:
    """
    替换url
    :param old_str:
    :param new_str:
    :param url:
    :return:
    """
    if '$' in old_str:
        str1, str2 = old_str.split('$')
        old_str = str1 + '\$' + str2
    return re.sub(old_str, new_str, url)