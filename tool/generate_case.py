#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: generate_case.py
@Time: 2022/8/18-16:39
"""

import jsonpath
from typing import List
from apps.template import schemas


class GenerateCase:

    async def read_template_to_api(self, temp_name: str, mode: str, template_data: List[schemas.TemplateDataOut]):
        """
        读取模板生成准测试数据
        :param temp_name:
        :param template_data:
        :return:
        """
        response = [x.response for x in template_data]

        case_data_list = []
        for num in range(len(template_data)):
            case_data = {
                'number': f'${num}',
                'path': template_data[num].path,
                'headers': {},
                # 'headers': template_data[num].headers,
                'params': await self._extract_params_keys(param=template_data[num].params, response=response[:num + 1]),
                'data': await self._extract_params_keys(param=template_data[num].data, response=response[:num + 1]),
                'check': {'status_code': 200 if num == 0 else template_data[num].code},
                'description': '',
                'config': {
                    'is_login': True if num == 0 else None,
                    'sleep': 0.3
                }
            }
            case_data_list.append(case_data)

        return {
            'tips': [
                '1.编写用例时，只需关注params/data/check',
                '2.headers接受键值对输入，有内容则在执行时添加/替换请求头内容',
                '3.is_login标记登录接口，标记后自动获取token/cookie进行替换',
                {'参数check': [
                    '1.key为要校验的字段，value为校验的值',
                    '2.若value数据类型为: string/integer/bool, 按 == 直接进行校验',
                    '3.若value数据类型为: list, 索引0应填写比较符: <,<=,==,>=,>,in,not in; 索引1填写比较的值'
                ]},
                'description: 用例描述信息',
                'mode: 运行模式, 支持: service/ddt/perf',
                'config: 单接口的配置信息'
            ],
            'temp_name': temp_name,
            'mode': mode,
            'data': case_data_list
        }

    @staticmethod
    async def _extract_params_keys(param: dict, response: list) -> dict:
        """
        提取字典中的key
        :param param:
        :param response:
        :return:
        """

        def header_key(data: dict) -> dict:
            target = {}
            for key in data.keys():
                if isinstance(data[key], dict):
                    header_key(data[key])
                    continue

                if isinstance(data[key], list):
                    for k in data[key]:
                        if isinstance(k, (list, dict)):
                            header_key(k)
                        else:
                            target[key] = data[key]
                    continue

                for x in range(len(response)):
                    value = jsonpath.jsonpath(response[x], f"$..{key}")
                    if isinstance(value, list) and len(value) == 1:
                        target[key] = f"${x}.{'.'.join(GenerateCase._extract_response_key_path(key, response[x]))}"
                        break
                    else:
                        target[key] = data[key]

            return target

        return header_key(param)

    @staticmethod
    def _extract_response_key_path(key: str, response_data: dict) -> list:
        """
        从response里面提取key在json中的路径
        :param key:
        :param response_data:
        :return:
        """
        if key in response_data.keys():
            return [key]

        param_str = []

        def header_value(key, data):
            for k in data.keys():
                if k == key:
                    param_str.append(k)

                if isinstance(data[k], dict):
                    if jsonpath.jsonpath(data[k], f"$..{key}"):
                        param_str.append(k)
                        header_value(key, data[k])

                elif isinstance(data[k], list):
                    for x in range(len(data[k])):
                        if jsonpath.jsonpath(data[k][x], f"$..{key}"):
                            param_str.append(k)
                            param_str.append(str(x))
                            header_value(key, data[k][x])
                            break

            return param_str

        return header_value(key, response_data)

    async def read_template_to_ddt(self):
        pass

    async def read_template_to_perf(self):
        pass
