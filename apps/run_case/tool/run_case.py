#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: run_case.py
@Time: 2022/8/23-15:20
"""

import re
import time
import copy
import json
import asyncio
# import aiohttp
import jsonpath
# import ujson
import requests
from requests import exceptions
from typing import List
from apps.template import schemas as temp
from apps.case_service import schemas as service
from tools import logger, get_cookie
from apps.run_case import crud
from sqlalchemy.orm import Session


class RunCase:
    def __init__(self):
        # self.sees = aiohttp.client.ClientSession(json_serialize=ujson.dumps)
        self.cookies = None

    async def fo_service(
            self,
            db: Session,
            case_name: str,
            temp_data: List[temp.TemplateDataOut],
            case_data: List[service.TestCaseData],
            temp_pro: str,
            temp_name: str
    ):
        """
        集合模板用例和测试数据

        1.识别url，data中的表达式
        2.拿表达式从response里面提取出来值
        2.url拿到值，直接替换
        """
        # 返回结果收集
        response = []

        result = []
        for num in range(len(temp_data)):
            logger.info(f"{'=' * 30}开始请求{num}{'=' * 30}")
            # 识别url表达式
            url = await self._replace_rul(old_str=f"{temp_data[num].host}{case_data[num].path}", response=response)
            # 识别params表达式
            params = await self._replace_params_data(data=case_data[num].params, response=response)
            # 识别data表达式
            data = await self._replace_params_data(data=case_data[num].data, response=response)
            # 替换headers中的内容
            headers = await self._replace_headers(tmp_header=temp_data[num].headers, case_header=case_data[num].headers)

            request_info = {
                'url': url,
                'method': temp_data[num].method,
                'headers': headers,
                'params': params,
                f"{'json' if temp_data[num].json_body == 'json' else 'data'}": data,
            }

            config = case_data[num].config

            if self.cookies:
                request_info['headers']['Cookie'] = self.cookies

            logger.info(f"请求信息: {json.dumps(request_info, indent=2, ensure_ascii=False)}")

            # async with self.sees.request(**request_info, allow_redirects=False) as res:
            res = requests.request(**request_info, allow_redirects=False)
            if config['is_login']:
                self.cookies = await get_cookie(rep_type='requests', response=res)
            logger.info(f"状态码: {res.status_code}")

            # 收集结果
            request_info['expect'] = case_data[num].check
            request_info['description'] = case_data[num].description
            request_info['config'] = case_data[num].config
            # res_json = await res.json() if 'application/json' in res.content_type else {}
            try:
                res_json = res.json()
            except exceptions.RequestException:
                res_json = {}
            request_info['response'] = res_json
            response.append(res_json)

            if res.status_code != case_data[num].check['status_code']:
                request_info['actual'] = {'status_code': [res.status_code]}

                logger.info(f"响应信息: {json.dumps(res_json, indent=2, ensure_ascii=False)}")
                result.append(request_info)
                await asyncio.sleep(config['sleep'])
                logger.info(f"{'=' * 30}结束请求{num}{'=' * 30}")
                continue
            else:
                new_check = copy.deepcopy(case_data[num].check)
                del new_check['status_code']
                request_info['actual'] = {
                    **{'status_code': [res.status_code]},
                    **{k: jsonpath.jsonpath(res_json, f'$..{k}') for k in new_check}
                }
                logger.info(f"响应信息: {json.dumps(res_json, indent=2, ensure_ascii=False)}")
                result.append(request_info)
                await asyncio.sleep(config['sleep'])
                logger.info(f"{'=' * 30}结束请求{num}{'=' * 30}")
                continue

        # await self.sees.close()

        await crud.update_test_case_order(db=db, case_name=case_name)

        await crud.queue_add(db=db, data={
            'start_time': int(time.time() * 1000),
            'case_name': f'{temp_pro}-{temp_name}-{case_name}',
            'case_data': result
        })
        logger.info(f"用例: {temp_pro}-{temp_name}-{case_name} 执行完成, 进行结果校验")
        return f"{temp_pro}-{temp_name}-{case_name}"

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

    @staticmethod
    async def _replace_params_data(data: dict, response: list) -> dict:
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
                        if isinstance(i, dict):
                            none_list.append(await handle_value(i))
                        else:
                            none_list.append(i)
                    target[key] = none_list
                    continue

                if isinstance(data_json[key], str):
                    if "{{" in data_json[key] and "$" in data_json[key] and "}}" in data_json[key]:
                        replace_value = re.compile(r'{{(.*?)}}', re.S).findall(data_json[key])[0]
                        num, json_path = replace_value.split('.', 1)
                        value = jsonpath.jsonpath(response[int(num)], json_path)
                        if value:
                            target[key] = value[0]
                        else:
                            target[key] = value
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
