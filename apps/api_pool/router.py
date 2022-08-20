#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/4-15:30
"""

import json
import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
from fastapi import APIRouter, HTTPException, status, Query, Path, BackgroundTasks
from typing import Optional
from .schemas import YApiInfo, YApiInfoTask
from pathlib import Path as path

api_pool = APIRouter()


@api_pool.post('/login_yapi_info/', response_model=YApiInfo, name='记录YApi登录信息')
async def post_login_yapi_info(login_info: YApiInfo):
    p = path('./files/yapi.json')
    p.write_text(data=json.dumps(login_info.dict()))
    return login_info.dict()


@api_pool.get('/login_yapi_ifno/', name='获取YApi登录信息')
async def get_login_yapi_info():
    p = path('./files/yapi.json')
    try:
        data = json.loads(p.read_text())
    except FileNotFoundError:
        return {'message': '未记录信息'}
    return data


@api_pool.delete('/login_yapi_info/', name='删除YApi登录信息')
async def del_login_yapi_info():
    p = path('./files/yapi.json')
    try:
        p.unlink()
    except FileNotFoundError:
        return {'message': '未记录信息'}
    return {'message': '删除成功'}


async def test_task(msg: str):
    for _ in range(10):
        print(msg)


@api_pool.put('/project/{id}', response_model=YApiInfoTask, name='从YApi更新接口池数据')
async def project_yapi(back_ground_tasks: BackgroundTasks, id: int = Path(description='项目id')):
    p = path('./files/yapi.json')
    try:
        login_info = json.loads(p.read_text())
    except FileNotFoundError:
        return {'message': '未记录登录信息', 'yapi_info': YApiInfoTask}
    if id:
        sess = aiohttp.ClientSession()
        url = login_info['url']
        del login_info['url']

        try:
            async with sess.post(url + '/api/user/login', json=login_info) as res:
                if res.status != 200:
                    return {'message': f'登录信息不可用，{res.status}'}

        except ClientConnectorError as e:
            return {'message': f'连接失败：{str(e)}', 'yapi_info': YApiInfoTask}

        else:
            back_ground_tasks.add_task(test_task, msg='测试')

        return {'message': '更新单个项目的所有接口数据'}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未传递项目id，不能直接更新api')


@api_pool.get('/project/{id}', name='按项目查询接口池数据')
async def get_project(id: Optional[int] = Query(None, description='项目id')):
    if id:
        return {'message': '查询单个项目的所有接口列表'}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未传递项目id，不能直接查询api')
