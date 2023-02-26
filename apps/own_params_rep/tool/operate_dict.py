#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: operate_dict.py
@Time: 2023/2/26-9:43
"""

from typing import Any


def dict_add(json_path: str, dict_data: dict, value: Any = None):
    """
    对字典进行添加操作
    :param json_path:
    :param value:
    :param dict_data:
    :return:
    """
    key_list = [x for x in json_path.split('.') if x and x != '$']


def dict_edit(old_key: str, new_key: str, dict_data: dict, value: Any = None):
    """
    对字典进行修改操作
    :param old_key:
    :param new_key:
    :param dict_data:
    :param value:
    :return:
    """

    def handle_value(data_json):
        target = {}
        for k, v in data_json.items():
            if not isinstance(v, (list, dict)):
                if k == old_key:
                    target[new_key] = value if value else v
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

    return handle_value(dict_data)


def dict_del(old_key: str, dict_data: dict):
    """
    对字典进行删除操作
    :param old_key:
    :param dict_data:
    :return:
    """

    def handle_value(data_json):
        target = {}
        for k, v in data_json.items():
            if not isinstance(v, (list, dict)):
                if k == old_key:
                    pass
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

    return handle_value(dict_data)
