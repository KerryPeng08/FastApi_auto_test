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
        :param mode:
        :param template_data:
        :return:
        """
        response = [x.response for x in template_data]

        case_data_list = []
        for num in range(len(template_data)):
            if num == 0:
                params = template_data[num].params
                data = template_data[num].data
            else:
                params = await self._extract_params_keys(param=template_data[num].params, response=response[:num])
                data = await self._extract_params_keys(param=template_data[num].data, response=response[:num])

            case_data = {
                'number': f'${template_data[num].number}',
                'path': template_data[num].path,
                'headers': {},
                'params': params,
                'data': data,
                'file': True if template_data[num].file else False,
                'check': {'status_code': template_data[num].code},
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
                    '2.若value数据类型为: string/integer/float/bool/dict, 按 == 直接进行校验',
                    '3.若value数据类型为: list, 索引0应填写比较符: <,<=,==,!=,>=,>,in,not in; 索引1填写比较的值'
                ]},
                'description: 单接口用例描述信息',
                'mode: 运行模式, 支持: service/ddt/perf',
                'config: 单接口的配置信息',
                {'假数据工具': {
                    'name': '名称',
                    'ssn': '身份证',
                    'phone_number': '电话',
                    'credit_card_number': '银行卡',
                    'city': '城市',
                    'address': '地址',
                    'random_int': {
                        ':param 1': '长度为1的随机数字',
                        ':param 5': '长度为5的随机数字'
                    },
                    'time_int': {
                        ':param 0': '当前时间',
                        ':param -1': '当前时间前一天',
                        ':param 1': '当前时间后一天',
                        ':param -2': '前一天00:00:00',
                        ':param 2': '后一天23:59:59',
                    },
                    'time_str': '时间字符串, 同上',
                }}
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
                for x in range(len(response)):
                    value = jsonpath.jsonpath(response[x], f"$..{key}")
                    if isinstance(value, list):
                        ipath = jsonpath.jsonpath(response[x], f"$..{key}", result_type='IPATH')[0]
                        if key.lower() == ipath[-1].lower() and data[key] == value[0] and value[0]:
                            value = "{{" + f"{x}.$.{'.'.join(ipath)}" + "}}"
                            target[key] = value
                            break
                        else:
                            target[key] = data[key]
                    else:
                        target[key] = data[key]
                else:
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

            return target

        return header_key(param)

    async def read_template_to_ddt(self):
        pass

    async def read_template_to_perf(self):
        pass
