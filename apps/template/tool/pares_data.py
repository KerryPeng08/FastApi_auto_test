#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: pares_data.py
@Time: 2022/8/8-15:03
"""

import base64
import json
from sqlalchemy.orm import Session
from apps.template import schemas, crud

filter_url = ['application/javascript', 'text/css', 'image/png']


class ParseData:
    """
    解析Har数据
    """

    @classmethod
    async def pares_data(cls, db: Session, temp_name: str, project_name: str, har_data: bytes):
        data_json = json.loads(har_data.decode('utf-8'))

        db_template = await crud.create_template(db=db, temp_name=temp_name, project_name=project_name)

        api_count = 0
        for data in data_json['log']['entries']:

            # 过滤文件接口
            if data['response']['content'].get('mimeType') in filter_url:
                continue

            host = [x['value'] for x in data['request']['headers'] if x['name'] == 'Host'][0]
            http, path = data['request']['url'].split(host, 1)

            # 处理请求中的params数据
            if data['request'].get('queryString'):
                query = {query['name']: query['value'] for query in data['request']['queryString']}
            else:
                query = {}

            # 处理请求中 body和json数据
            if data['request'].get('postData'):
                body_json = await cls.post_data(data['request']['postData'])
            else:
                body_json = ['body', {}]

            if 'application/json' in str(data['response']['content'].get('mimeType')):
                res_data = json.loads(base64.b64decode(data['response']['content']['text'].encode('utf-8')))
            else:
                res_data = {}

            new_data = {
                'host': http + host,
                'path': path.split('?', 1)[0],
                'code': data['response']['status'],
                'method': data['request']['method'],
                'params': query,
                'json_body': body_json[0],
                'data': body_json[1],
                'headers': {header['name']: header['value'] for header in data['request']['headers']},
                'response': res_data,
            }
            await crud.create_template_data(db=db, data=schemas.TemplateDataIn(**new_data), temp_id=db_template.id)
            api_count += 1

        return await crud.update_template(db=db, temp_name=db_template.temp_name, api_count=api_count)

    @classmethod
    async def post_data(cls, post_data: dict):
        """
        处理请求数据类型
        :param post_data:
        :return:
        """
        if 'application/x-www-form-urlencoded' in post_data['mimeType']:
            return ['body', {params['name']: params['value'] for params in post_data['params']}]

        if 'application/json' in post_data['mimeType']:
            return ['json', json.loads(post_data['text'])]

        # if 'multipart/form-data' in post_data['mimeType']:
        #     return ['files', post_data['text']]

        return ['other', {}]
