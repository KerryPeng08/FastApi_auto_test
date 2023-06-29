#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/23-13:45
"""

import re
import os
import time
import asyncio
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from depends import get_db
from starlette.background import BackgroundTask
from apps import response_code
from apps.template import crud
from apps.case_service import crud as case_crud
from apps.case_ddt import crud as gather_crud
from apps.case_ui import crud as ui_crud
from apps.run_case import schemas, CASE_STATUS
from .tool import run_service_case, run_ddt_case, run_ui_case, header, replace_playwright
from setting import SELENOID

run_case = APIRouter()


@run_case.post(
    '/case',
    response_class=response_code.MyJSONResponse,
    name='按用例Id执行',
    description='按用例ID的顺序执行'
)
async def run_case_name(ids: schemas.RunCase, db: Session = Depends(get_db)):
    if not ids.case_ids:
        return await response_code.resp_400()

    report = await run_service_case(db=db, case_ids=ids.case_ids, temp_hosts=ids.temp_hosts)
    return await response_code.resp_200(data={'allure_report': report})


@run_case.post(
    '/temp',
    response_class=response_code.MyJSONResponse,
    name='按模板Id执行',
    description='按模板ID查询出关联的用例，再异步执行所有用例，收集结果集'
)
async def run_case_name(temp_ids: List[int], db: Session = Depends(get_db)):
    case_list = [await case_crud.get_case_ids(db=db, temp_id=x) for x in temp_ids]

    all_case_list = []
    temp_info = {}
    for x in range(len(case_list)):
        temp_info[temp_ids[x]] = [i[0] for i in case_list[x]]
        for y in case_list[x]:
            all_case_list.append(y[0])

    if not all_case_list:
        return await response_code.resp_404()

    # 按模板并发
    tasks = [asyncio.create_task(run_service_case(db=db, case_ids=[case_id])) for case_id in all_case_list]
    result = await asyncio.gather(*tasks)

    new_result = {}
    for x in result:
        new_result.update(x)
    return await response_code.resp_200(data={'allure_report': new_result, "temp_info": temp_info})


@run_case.post(
    '/gather',
    name='选择数据集执行用例',
    response_class=response_code.MyJSONResponse,
)
async def run_case_gather(rcs: schemas.RunCaseGather, db: Session = Depends(get_db)):
    """
    按数据集执行用例
    """
    gather_data = await gather_crud.get_gather(db=db, case_id=rcs.case_id, suite=rcs.suite)
    if not gather_data:
        return await response_code.resp_404()

    # 获取用例数据,按数据集分套替换数据
    case_data = await case_crud.get_case_data(db=db, case_id=rcs.case_id)
    new_case_data = await header(case_data=case_data, gather_data=gather_data)

    # 运行用例
    if rcs.async_:
        tasks = [
            asyncio.create_task(
                run_ddt_case(
                    db=db,
                    case_id=rcs.case_id,
                    case_info=[data],
                    temp_hosts=rcs.temp_hosts
                )
            ) for data in new_case_data
        ]
        result = await asyncio.gather(*tasks)

        new_result = {}
        for x in result:
            new_result.update(x)
        return await response_code.resp_200(data={'allure_report': new_result})
    else:
        report = await run_ddt_case(
            db=db,
            case_id=rcs.case_id,
            case_info=new_case_data,
            temp_hosts=rcs.temp_hosts
        )
        return await response_code.resp_200(data={'allure_report': report})


@run_case.post(
    '/ui/temp',
    name='执行ui脚本用例',
)
async def ui_temp(rut: schemas.RunUiTemp, db: Session = Depends(get_db)):
    """
    执行ui脚本用例
    """
    ui_temp_info = await ui_crud.get_playwright(db=db, temp_id=rut.temp_id)
    if ui_temp_info:
        file_name = f"temp_id_{ui_temp_info[0].id}_{time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))}"

        if rut.gather_id:
            case_info = await ui_crud.get_play_case_data(db=db, case_id=rut.gather_id, temp_id=rut.temp_id)

            # 替换测试数据
            temp_text = ui_temp_info[0].text.split('\n')
            for x in case_info[0].rows_data:
                temp_text[x['row'] - 1] = re.sub(r'{{(.*?)}}', x['data'], temp_text[x['row'] - 1], 1)

            playwright = await replace_playwright(
                playwright_text='\n'.join(temp_text),
                temp_name=ui_temp_info[0].temp_name,
                remote=rut.remote,
                remote_id=rut.remote_id,
                headless=rut.headless,
                file_name=file_name
            )
        else:
            playwright = await replace_playwright(
                playwright_text=ui_temp_info[0].text,
                temp_name=ui_temp_info[0].temp_name,
                remote=rut.remote,
                remote_id=rut.remote_id,
                headless=rut.headless,
                file_name=file_name
            )

        if not playwright:
            return await response_code.resp_400(message='由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败')

        report = await run_ui_case(db=db, playwright_text=playwright, temp_id=rut.temp_id)
        report['video'] = f"http://{SELENOID['selenoid_ui_host']}/video/{file_name}.mp4"
        return await response_code.resp_200(
            data=report,
            background=BackgroundTask(lambda: os.remove(report['tmp_file']))
        )
    else:
        return await response_code.resp_404()


@run_case.get(
    '/case/status',
    name='获取用例运行的状态',
    response_class=response_code.MyJSONResponse,
)
async def case_status(key_id: str = None):
    if key_id:
        if CASE_STATUS.get(key_id):
            CASE_STATUS[key_id]['stop'] = True
            return await response_code.resp_200(message='停止成功')
        else:
            return await response_code.resp_200(message='没有运行这个用例')
    return CASE_STATUS


@run_case.get(
    '/temp/host',
    name='通过case_id查询temp的host数据'
)
async def get_temp_host_list(case_id: int, db: Session = Depends(get_db)):
    """
    查询模板的host列表
    """
    case_info = await case_crud.get_case_info(db=db, case_id=case_id)

    hosts = await crud.get_temp_host(db=db, temp_id=case_info[0].temp_id)
    if hosts:
        return hosts
    else:
        return await response_code.resp_404()
