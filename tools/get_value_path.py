#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: get_value_path.py
@Time: 2023/2/14-12:58
"""

import re
import jsonpath
from typing import Any


class ExtractParamsPath:
    """
    通过value提取json路径
    """

    @classmethod
    def get_url_path(cls, extract_contents: str, my_data: list):
        """
        从url字段中获取数据
        :param extract_contents:
        :param my_data:
        :return:
        """

        return {
            'extract_contents': [{'jsonpath': f"{x.number}.{x.path}"} for x in my_data if extract_contents in x.path]
        }

    @classmethod
    def get_value_path(cls, extract_contents: Any, my_data: list, type_: str) -> dict:
        """
        获取value的json路径
        :param extract_contents:
        :param my_data:
        :param type_:
        :return:
        """
        if type_ not in ['params', 'data', 'response']:
            raise TypeError('type_字段不满足要求')

        path_list = []
        for data in my_data:
            if type_ == 'params':
                key_list = cls._out_function(extract_contents, data.params)
                value_path_list = cls._get_json_path(
                    extract_contents,
                    key_list=key_list,
                    response=data.params,
                    number=data.number
                )
            elif type_ == 'data':
                key_list = cls._out_function(extract_contents, data.data)
                value_path_list = cls._get_json_path(
                    extract_contents,
                    key_list=key_list,
                    response=data.data,
                    number=data.number
                )
            else:
                key_list = cls._out_function(extract_contents, data.response)
                value_path_list = cls._get_json_path(
                    extract_contents,
                    key_list=key_list,
                    response=data.response,
                    number=data.number
                )

            path_list += value_path_list
        if type_ == 'response':
            return {'extract_contents': path_list[:5]}
        return {'extract_contents': path_list}

    @classmethod
    def _out_function(cls, extract_contents: Any, data: dict) -> list:
        """
        提取出和value值相等的key
        :param extract_contents:
        :param data:
        :return:
        """
        target = []

        def in_function(response):
            if isinstance(response, dict):
                for k, v in response.items():
                    if extract_contents == v:
                        target.append(k)
                    else:
                        in_function(v)

            elif isinstance(response, list):
                for x in range(len(response)):
                    if extract_contents == response[x]:
                        target.append(x)
                    else:
                        in_function(response[x])

            return target

        return in_function(data)

    @classmethod
    def _get_json_path(cls, extract_contents: Any, key_list: list, response: dict, number) -> list:
        """
        通过提取出来的key，获取多个ipath，再通过value判断那个ipath是正确的
        :param extract_contents:
        :param key_list:
        :param response:
        :param number:
        :return:
        """
        new_path_list = []
        for key_ in key_list:

            value_list = jsonpath.jsonpath(response, f"$..{key_}")
            path_list = jsonpath.jsonpath(response, f"$..{key_}", result_type='IPATH')

            for k, v in zip(value_list, path_list):
                if k == extract_contents:
                    new_path_list.append({'jsonpath': "{{" + f"{number}.$.{'.'.join(v)}" + "}}"})

        return new_path_list


class RepData:
    """
    替换数据
    """

    @classmethod
    def rep_url(cls, url_list: dict, new_str: str, extract_contents: str):
        """
        替换数据预览
        :param url_list:
        :param new_str:
        :param extract_contents:
        :return:
        """
        # new_url_list = []
        for url in url_list['extract_contents']:
            number, json_path = url['jsonpath'].split('.', 1)
            url['old_data'] = extract_contents
            url['new_data'] = new_str
            url['jsonpath'] = 're.sub(extract_contents, jsonpath, old_data)'
            url['number'] = int(number)
        return url_list

    @classmethod
    def rep_json(cls, json_data: dict, case_data: list, new_str: str, type_: str):
        """
        替换数据预览
        :param json_data:
        :param case_data:
        :param new_str:
        :return:
        """
        for data in json_data['extract_contents']:
            bb = re.sub('}}', '', re.sub('{{', '', data['jsonpath']))
            number, json_path = bb.split('.', 1)

            if type_ == 'params':
                old_data = jsonpath.jsonpath(case_data[int(number)].params, f"{json_path}")
                data['old_data'] = old_data[0] if len(old_data) > 0 else False
            else:
                old_data = jsonpath.jsonpath(case_data[int(number)].data, f"{json_path}")
                data['old_data'] = old_data[0] if len(old_data) > 0 else False
            data['new_data'] = new_str
            data['number'] = int(number)

        return json_data
