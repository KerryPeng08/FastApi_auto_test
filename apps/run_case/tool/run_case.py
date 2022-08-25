#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: run_case.py
@Time: 2022/8/23-15:20
"""

import re
import asyncio
import aiohttp
import jsonpath
from typing import List
from apps.template import schemas as temp
from apps.case_service import schemas as service
from tools import OperationJson


class RunCase:
    def __init__(self):
        self.sees = aiohttp.client.ClientSession()
        self.cookies = None

    async def fo_service(
            self,
            case_name: str,
            temp_data: List[temp.TemplateDataOut],
            case_data: List[service.TestCaseData]
    ):
        """
        集合模板用例和测试数据

        1.识别url，data中的表达式
        2.拿表达式从response里面提取出来值
        2.url拿到值，直接替换

        :param case_name:
        :param temp_data:
        :param case_data:
        :return:
        """
        # 返回结果收集
        response = []

        for num in range(len(temp_data)):
            # 识别url表达式
            url = await self._replace_rul(old_str=f"{temp_data[num].host}{case_data[num].path}", response=response)
            # 识别params表达式
            params = await self._replace_params_data(data=case_data[num].params, response=response)
            print(params)
            # 识别data表达式
            data = await self._replace_params_data(data=case_data[num].data, response=response)
            print(data)
            # 替换headers中的内容
            headers = await self._replace_headers(tmp_header=temp_data[num].headers, case_header=case_data[num].headers)

            request_info = {
                'method': temp_data[num].method,
                'url': url,
                'headers': headers,
                'params': params,
                f"{'data' if temp_data[num].json_body == 'body' else 'json'}": data,
            }

            config = case_data[num].config
            check = case_data[num].check

            if self.cookies:
                request_info['headers']['Cookie'] = self.cookies

            # print(request_info)

            async with self.sees.request(**request_info, allow_redirects=False) as res:
                if config['is_login']:
                    self.cookies = await self._get_cookie(res)
                # print(res.status)

                res_json = await res.json() if res.status == 200 and 'application/json' in res.content_type else {}
                response.append(res_json)
                print(res_json)
                print("=" * 50)

                # 收集结果

            await asyncio.sleep(config['sleep'])

        await self.sees.close()
        # path = f'./files/run_case/{123}.json'
        # await OperationJson.write(path=path, data={'name': case_name, 'data': run_case_data[:5]})

    @staticmethod
    async def _get_cookie(response) -> str:
        """
        获取cookie数据
        :param response:
        :return:
        """
        cookie = ''
        for k, v in response.cookies.items():
            cookie += f"{k}={re.compile(r'=(.*?); ', re.S).findall(str(v))[0]}; "
        return cookie

    @staticmethod
    async def _replace_rul(old_str: str, response: list) -> str:
        """
        替换url的值
        :param old_str:
        :param response:
        :return:
        """
        replace_values: List[str] = re.compile(r'{{(.*?)}}', re.S).findall(old_str)
        for replace in replace_values:
            num, json_path = replace.split('.', 1)
            value = jsonpath.jsonpath(response[int(num)], json_path)
            if value:
                old_str = re.sub("{{" + f"{num}." + '\\' + f"{json_path}" + "}}", str(value[0]), old_str)

        return old_str

    async def _replace_params_data(self, data: dict, response: list) -> dict:
        """
        替换params和data的值
        :param data:
        :param response:
        :return:
        """

        async def handle_value(data_json):
            target = {}
            for key in data_json.keys():
                if isinstance(data_json[key], dict):
                    target[key] = await handle_value(data_json[key])
                    continue

                if isinstance(data_json[key], list):
                    none_list = []
                    for i in data_json[key]:
                        none_list.append(await handle_value(i))
                    target[key] = none_list
                    continue

                if isinstance(data_json[key], str):
                    if "{{" in data_json[key] and "$" in data_json[key] and "}}" in data_json[key]:
                        replace_value = re.compile(r'{{(.*?)}}', re.S).findall(data_json[key])[0]
                        num, json_path = replace_value.split('.', 1)
                        target[key] = jsonpath.jsonpath(response[int(num)], json_path)[0]
                    else:
                        target[key] = data_json[key]
                else:
                    target[key] = data_json[key]

            return target

        return await handle_value(data)

    @staticmethod
    async def _replace_headers(tmp_header: dict, case_header: dict) -> dict:
        """
        替换headers中的内容
        :param tmp_header:
        :param case_header:
        :return:
        """
        for k, v in case_header.items():
            tmp_header[k] = v
        return tmp_header
