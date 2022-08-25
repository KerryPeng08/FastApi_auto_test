#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: test_service.py
@Time: 2022/8/23-21:29
"""

import json
import asyncio
import aiohttp
# import time
import allure
import pytest
from tools import OperationJson

loop = asyncio.get_event_loop()
run_data = loop.run_until_complete(OperationJson.read(path=f'./files/run_case/{123}.json'))

data_list = [
    [
        x,
        run_data['data'][x]['host'],
        run_data['data'][x]['path'],
        run_data['data'][x]['code'],
        run_data['data'][x]['method'],
        run_data['data'][x]['params'],
        run_data['data'][x]['json_body'],
        run_data['data'][x]['data'],
        run_data['data'][x]['headers'],
        run_data['data'][x]['description'],
        run_data['data'][x]['config'],
        run_data['data'][x]['check']

    ] for x in range(len(run_data['data']))
]


# COOKIE = []


class TestService:
    cookie = None

    @pytest.mark.asyncio
    @allure.feature(run_data['name'])
    @pytest.mark.parametrize(
        'num,host,path,code,method,params,json_body,data,headers,description,config,check', data_list
    )
    async def test_service(self, num, host, path, code, method, params, json_body, data, headers, description, config,
                           check):
        allure.dynamic.title(f"${str(num).rjust(3, '0')}{path}-{description}")
        allow = False if config['is_login'] else True
