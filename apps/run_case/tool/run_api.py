#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: run_api.py
@Time: 2022/8/23-15:20
"""

import re
import time
import copy
import json
import base64
import asyncio
# import aiohttp
import jsonpath
# import ujson
import requests
from requests.exceptions import RequestException
from typing import List
from requests import exceptions
from sqlalchemy.orm import Session
from tools import logger, get_cookie
from tools.faker_data import FakerData
from apps.template import schemas as temp
from apps.case_service import schemas as service
from apps.run_case import crud


class RunApi:
    def __init__(self):
        # self.sees = aiohttp.client.ClientSession(json_serialize=ujson.dumps)
        self.cookies = {}
        self.fk = FakerData()

    async def fo_service(
            self,
            db: Session,
            case_id: int,
            temp_data: List[temp.TemplateDataOut],
            case_data: List[service.TestCaseData],
            temp_pro: str,
            temp_name: str
    ):
        """
        集合模板用例和测试数据
        1.识别url，data中的表达式
        2.拿表达式从response里面提取出来值
        2.拿到值，直接替换
        """
        # 返回结果收集
        response = []

        result = []
        for num in range(len(temp_data)):
            logger.info(f"{'=' * 30}开始请求{num}{'=' * 30}")
            try:
                # 识别url表达式
                url = await self._replace_url(
                    old_str=f"{temp_data[num].host}{case_data[num].path}", response=response, faker=self.fk
                )
                # 识别params表达式
                params = await self._replace_params_data(data=case_data[num].params, response=response, faker=self.fk)
                # 识别data表达式
                data = await self._replace_params_data(data=case_data[num].data, response=response, faker=self.fk)
            except IndexError:
                raise IndexError(f'参数提取错误, 请检查用例编号: {num} 的提取表达式')
            # 替换headers中的内容
            headers = await self._replace_headers(tmp_header=temp_data[num].headers, case_header=case_data[num].headers)

            request_info = {
                'url': url,
                'method': temp_data[num].method,
                'headers': headers,
                'params': params,
                f"{'json' if temp_data[num].json_body == 'json' else 'data'}": data,
            }
            # 上传附件
            files = {
                f"{temp_data[num].file_data[0]['name']}": (
                    temp_data[num].file_data[0]['fileName'],
                    base64.b64decode(temp_data[num].file_data[0]['value'].encode('utf-8')),
                    temp_data[num].file_data[0]['contentType']
                )
            } if temp_data[num].file else None

            config = copy.deepcopy(case_data[num].config)

            if self.cookies.get(temp_data[num].host):
                request_info['headers']['Cookie'] = self.cookies[temp_data[num].host]

            # 有附件时，要删除Content-Type
            if files:
                del request_info['headers']['Content-Type']

            logger.info(f"请求信息: {json.dumps(request_info, indent=2, ensure_ascii=False)}")

            # 轮询执行接口
            res = await self.polling(
                sleep=config['sleep'],
                check=case_data[num].check,
                request_info=request_info,
                files=files
            )

            if config['is_login']:
                self.cookies[temp_data[num].host] = await get_cookie(rep_type='requests', response=res)
            logger.info(f"状态码: {res.status_code}")

            # 收集结果
            request_info['file'] = True if temp_data[num].file else False
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

            # 判断响应结果，调整校验内容收集
            if res.status_code != case_data[num].check['status_code']:
                request_info['actual'] = {'status_code': [res.status_code]}
            else:
                new_check = copy.deepcopy(case_data[num].check)
                del new_check['status_code']
                request_info['actual'] = {
                    **{'status_code': [res.status_code]},
                    **{k: jsonpath.jsonpath(res_json, f'$..{k}') for k in new_check}
                }

            config['sleep'] = 0.3
            await asyncio.sleep(config['sleep'])
            result.append(request_info)
            logger.info(f"响应信息: {json.dumps(res_json, indent=2, ensure_ascii=False)}")
            logger.info(f"{'=' * 30}结束请求{num}{'=' * 30}")

        # await self.sees.close()

        case_info = await crud.update_test_case_order(db=db, case_id=case_id)

        await crud.queue_add(db=db, data={
            'start_time': int(time.time() * 1000),
            'case_name': f'{temp_pro}-{temp_name}-{case_info.case_name}',
            'case_data': result
        })
        logger.info(f"用例: {temp_pro}-{temp_name}-{case_info.case_name} 执行完成, 进行结果校验, 序号: {case_info.run_order}")
        return f"{temp_pro}-{temp_name}-{case_info.case_name}", case_info.run_order

    @staticmethod
    async def polling(sleep: int, check: dict, request_info: dict, files):
        """
        轮询执行接口
        :param sleep:
        :param check:
        :param request_info:
        :param files:
        :return:
        """

        check = copy.deepcopy(check)
        del check['status_code']

        num = 1
        while True:
            # async with self.sees.request(**request_info, allow_redirects=False) as res:
            res = requests.request(**request_info, files=files, allow_redirects=False, timeout=60)
            if sleep < 5:
                break

            logger.info(f"循环{num + 1}次: {request_info['url']}")
            if res.status_code != 200:
                logger.error(f"状态码: {res.status_code}")
                break
            try:
                res_json = res.json()
            except RequestException as e:
                logger.error(f"错误信息: {str(e)}")
                break

            result = []
            for k, v in check.items():
                # 获取需要的值
                value = jsonpath.jsonpath(res_json, f'$..{k}')

                if value:
                    value = value[0]
                else:
                    break

                if isinstance(v, (str, int, float, bool, dict)):
                    if v == value:
                        result.append({k: value})
                    continue

                if isinstance(v, list):
                    if v[0] == '<':
                        if value < v[1]:
                            result.append({k: value})
                    elif v[0] == '<=':
                        if value <= v[1]:
                            result.append({k: value})
                    elif v[0] == '==':
                        if value == v[1]:
                            result.append({k: value})
                    elif v[0] == '!=':
                        if value != v[1]:
                            result.append({k: value})
                    elif v[0] == '>=':
                        if value >= v[1]:
                            result.append({k: value})
                    elif v[0] == '>':
                        if value > v[1]:
                            result.append({k: value})
                    elif v[0] == 'in':
                        if value in v[1]:
                            result.append({k: value})
                    elif v[0] == 'not in':
                        if value not in v[1]:
                            result.append({k: value})
                    elif v[0] == 'notin':
                        if value not in v[1]:
                            result.append({k: value})
            logger.info(f"匹配结果: {result}")
            if len(result) == len(check):
                break

            await asyncio.sleep(5)
            sleep -= 5
            num += 1

        return res

    @staticmethod
    async def _replace_url(old_str: str, response: list, faker: FakerData) -> str:
        """
        替换url的值
        :param old_str:
        :param response:
        :return:
        """
        return await header_srt(x=old_str, response=response, faker=faker, value_type='url')

    @staticmethod
    async def _replace_params_data(data: dict, response: list, faker: FakerData) -> dict:
        """
        替换params和data的值
        :param data:
        :param response:
        :return:
        """

        async def handle_value(data_json):
            target = {}
            for key in data_json.keys():
                if isinstance(data_json[key], str):
                    target[key] = await header_srt(x=data_json[key], response=response, faker=faker)
                    continue

                if isinstance(data_json[key], dict):
                    target[key] = await handle_value(data_json[key])
                    continue

                if isinstance(data_json[key], list):
                    new_list = []
                    for x in data_json[key]:
                        if isinstance(x, (list, dict)):
                            new_list.append(await handle_value(x))
                        elif isinstance(x, str):
                            new_list.append(await header_srt(x=x, response=response, faker=faker))
                        else:
                            new_list.append(x)

                    target[key] = new_list
                    continue

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


async def header_srt(x: str, response: list, faker: FakerData, value_type: str = None):
    """
    处理数据
    :param x:
    :param response:
    :param faker:
    :param value_type:
    :return:
    """
    if "{{" in x and "$" in x and "}}" in x:
        replace_values: List[str] = re.compile(r'{{(.*?)}}', re.S).findall(x)
        for replace in replace_values:
            new_value = await _header_str_param(x=replace, response=response)

            if value_type == 'url':
                x = re.sub("{{(.*?)}}", str(new_value), x, count=1)
                continue

            if isinstance(new_value, str):
                x = re.sub("{{(.*?)}}", new_value, x, count=1)
            else:
                x = new_value

        return x

    if "{" in x and "}" in x:
        replace_values: List[str] = re.compile(r'{(.*?)}', re.S).findall(x)
        for replace in replace_values:
            new_value = await _header_str_func(x=replace, faker=faker)

            if value_type == 'url':
                x = re.sub("{(.*?)}", str(new_value), x, count=1)
                continue

            if isinstance(new_value, str):
                x = re.sub("{(.*?)}", new_value, x, count=1)
            else:
                x = new_value
        return x

    return x


async def _header_str_param(x: str, response: list) -> str:
    """
    提取参数：字符串内容
    :param x:
    :param response:
    :return:
    """
    num, json_path = x.split('.', 1)

    # 字符串截取
    start_index, end_index = None, None
    if "|" in json_path:
        json_path, str_index = json_path.split('|', 1)
        start_index, end_index = str_index.split(':', 1)

    value = jsonpath.jsonpath(response[int(num)], json_path)
    if value:
        if start_index is None and end_index is None:
            return value[0]
        else:
            if isinstance(value[0], str):
                try:
                    return value[0][
                           int(start_index):int(
                               end_index) if end_index != '' else None
                           ]
                except ValueError:
                    return value[0]
            else:
                return value[0]
    else:
        return value


async def _header_str_func(x: str, faker: FakerData):
    """
    处理随机方法生成的数据
    :param x:
    :param faker:
    :return:
    """
    try:
        if '.' in x:
            func, param = x.split('.', 1)
        else:
            func, param = x, 1

        try:
            param = int(param)
        except TypeError:
            param = 1

        value = faker.faker_data(func=func, param=param)

        return value if value else x

    except ValueError:
        return x