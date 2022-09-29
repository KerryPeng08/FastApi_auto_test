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
from setting import TIPS


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
            'tips': TIPS,
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
