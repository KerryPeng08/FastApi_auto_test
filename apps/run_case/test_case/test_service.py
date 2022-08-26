#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: test_service.py
@Time: 2022/8/23-21:29
"""

import asyncio
import allure
import pytest
import typing
from tools import OperationJson

loop = asyncio.get_event_loop()
run_data = loop.run_until_complete(OperationJson.read(path=f'./files/run_case/{123}.json'))

data_list = [
    [
        x,
        run_data['data'][x]['url'],
        run_data['data'][x]['method'],
        run_data['data'][x]['params'],
        run_data['data'][x].get('data') or run_data['data'][x].get('json'),
        run_data['data'][x]['expect'],
        run_data['data'][x]['actual'],
        run_data['data'][x]['response'],
        run_data['data'][x]['description'],
        run_data['data'][x]['config'],
        run_data['data'][x]['headers'],

    ] for x in range(len(run_data['data']))
]


class TestService:

    @pytest.mark.asyncio
    @allure.feature(run_data['name'])
    @pytest.mark.parametrize(
        'num,url,method,params,data,expect,actual,response,description,config,headers', data_list
    )
    async def test_service(self, num: int, url: str, method: str, params: dict, data: dict, expect: dict, actual: dict,
                           response: dict, description: str, config: dict, headers: dict):
        allure.dynamic.title(f"${str(num).rjust(3, '0')}-{description}\n{url}")

        for k, v in expect.items():
            await self.assert_value(k, v, actual_value=actual)

    @staticmethod
    async def assert_value(k: str, v: typing.Any, actual_value: dict):
        """
        校验内容
        :return:
        """
        allure.attach(f"expect: {v}，actual: {actual_value[k]}", f'校验内容: {k}')
        if isinstance(v, (str, int, float, bool, dict)):
            assert v == actual_value[k][0]

        if isinstance(v, list):
            if v[0] == '<':
                assert actual_value[k] < v[1]
            elif v[0] == '<=':
                assert actual_value[k] <= v[1]
            elif v[0] == '==':
                assert actual_value[k] == v[1]
            elif v[0] == '!=':
                assert actual_value[k] != v[1]
            elif v[0] == '>=':
                assert actual_value[k] >= v[1]
            elif v[0] == '>':
                assert actual_value[k] > v[1]
            elif v[0] == 'in':
                assert actual_value[k] in v[1]
            elif v[0] == 'not in':
                assert actual_value[k] not in v[1]
            elif v[0] == 'notin':
                assert actual_value[k] not in v[1]
            else:
                assert 1 == 0, '未匹配搭配比较符'
