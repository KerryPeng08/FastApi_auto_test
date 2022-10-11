#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: get_case_data_info.py
@Time: 2022/10/11-11:13
"""

from setting import TIPS


class GetCaseDataInfo:
    """
    获取测试数据
    """

    async def service(self, case_info: tuple, case_data_info: tuple):
        """
        业务流程测试用例
        :param case_info:
        :param case_data_info:
        :return:
        """
        new_case_data = []
        for data in case_data_info:
            case_data = {
                'number': data.number,
                'path': data.path,
                'headers': data.headers,
                'params': data.params,
                'data': data.data,
                'file': data.file,
                'check': data.check,
                'description': data.description,
                'config': data.config
            }
            new_case_data.append(case_data)

        return {
            'tips': TIPS,
            'case_name': case_info[0].case_name,
            'mode': case_info[0].mode,
            'data': new_case_data
        }
