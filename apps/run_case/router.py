#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/23-13:45
"""

import asyncio
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from depends import get_db
from apps import response_code
from apps.case_service import crud as case_crud
from .tool.run_case import run_service_case

run_case = APIRouter()


@run_case.post(
    '/case',
    response_class=response_code.MyJSONResponse,
    name='按用例Id执行'
)
async def run_case_name(case_ids: List[int], db: Session = Depends(get_db)):
    if not case_ids:
        return await response_code.resp_400()

    report = await run_service_case(db=db, case_ids=case_ids)
    return await response_code.resp_200(data={'allure_report': report})


@run_case.post(
    '/temp',
    response_class=response_code.MyJSONResponse,
    name='按模板Id执行'
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
