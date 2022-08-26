#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/23-13:45
"""

from aiohttp.client import ServerDisconnectedError, ServerConnectionError
from fastapi import APIRouter, Depends, HTTPException, status, Request
from apps.case_service import crud as case_crud
from apps.template import crud as temp_crud
from apps.run_case import crud as run_crud
from sqlalchemy.orm import Session
from depends import get_db
from .tool import RunCase, run
from setting import ALLURE_PATH

run_case = APIRouter()


@run_case.post('/case_name', name='按用例执行')
async def run_case_name(request: Request, case_name: str, db: Session = Depends(get_db)):
    case_info = await case_crud.get_case_name(db=db, case_name=case_name)
    if case_info:
        # 拿到测试数据
        case_data = await case_crud.get_case_data(db=db, case_id=case_info[0].id)
        # 拿到模板数据
        temp_data = await temp_crud.get_template_data(db=db, temp_id=case_info[0].temp_id)
        # 处理数据，执行用例
        try:
            await RunCase().fo_service(case_name=case_name, temp_data=temp_data, case_data=case_data)
        except (ServerDisconnectedError, ServerConnectionError) as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': f'访问失败: {str(e)}'})
        # 拿到项目名称
        pro_name = await run_crud.get_pro_name(db=db, temp_id=case_info[0].temp_id)
        # 校验结果，生成报告
        await run(
            test_path='./apps/run_case/test_case/test_service.py',
            report_path=f'{ALLURE_PATH}{pro_name}/report',
            allure_path=f'{ALLURE_PATH}{pro_name}/allure'
        )
        return {
            'message': '执行完成',
            'allure_report': f'{request.base_url}allure/{pro_name}'
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未查询到用例')


@run_case.post('/case_ids', name='按用例ID执行')
async def run_case_ids(ids: list, db: Session = Depends(get_db)):
    pass


@run_case.post('/temp_name', name='按模块执行')
async def run_temp_name(temp_name: str, db: Session = Depends(get_db)):
    pass
