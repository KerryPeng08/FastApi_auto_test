#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: collect_data.py
@Time: 2022/8/23-15:20
"""

import time
from typing import List
from apps.template import schemas as temp
from apps.case_service import schemas as service
from tools import OperationJson


class CollectData:

    @classmethod
    async def fo_service(
            cls,
            case_name: str,
            temp_data: List[temp.TemplateDataOut],
            case_data: List[service.TestCaseData]
    ):
        """
        集合模板用例和测试数据
        :param case_name:
        :param temp_data:
        :param case_data:
        :return:
        """

        run_case_data = []
        for num in range(len(temp_data)):
            data = {
                'host': temp_data[num].host,
                'path': temp_data[num].path,
                'code': case_data[num].check['status_code'],
                'method': temp_data[num].method,
                'params': case_data[num].params,
                'json_body': temp_data[num].json_body,
                'data': case_data[num].data,
                'headers': {**temp_data[num].headers, **case_data[num].headers},
                'description': case_data[num].description,
                'config': case_data[num].config,
                'check': case_data[num].check,
            }
            run_case_data.append(data)

        path = f'./files/run_case/{123}.json'
        await OperationJson.write(path=path, data={'name': case_name, 'data': run_case_data})
