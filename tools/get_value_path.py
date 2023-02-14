#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: get_value_path.py
@Time: 2023/2/14-12:58
"""

from typing import Any
import jsonpath


class ExtractParamsPath:
    """
    通过value提取json路径
    """

    @classmethod
    def get_value_path(cls, extract_contents: Any, temp_data: list) -> dict:
        """
        获取value的json路径
        :param extract_contents:
        :param temp_data:
        :return:
        """

        path_list = []
        for temp_info in temp_data:
            key_list = cls._out_function(extract_contents, temp_info.response)
            value_path_list = cls._get_json_path(
                extract_contents,
                key_list=key_list,
                response=temp_info.response,
                number=temp_info.number
            )
            path_list += value_path_list

        return {extract_contents: path_list}

    @classmethod
    def _out_function(cls, extract_contents: Any, response: dict) -> list:
        """
        提取出和value值相等的key
        :param extract_contents:
        :param response:
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

        return in_function(response)

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
                    new_path_list.append("{{" + f"{number}.$.{'.'.join(v)}" + "}}")

        return new_path_list
