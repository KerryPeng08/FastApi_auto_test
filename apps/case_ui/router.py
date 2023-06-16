#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2023/6/9-16:31
"""

from fastapi import APIRouter, Depends
from depends import get_db
from typing import List
from sqlalchemy.orm import Session
from apps.my_pagination import Page
from fastapi_pagination import add_pagination, paginate

from apps import response_code
from apps.case_ui import schemas, crud
from apps.case_ui.tool import case_data

case_ui = APIRouter()


@case_ui.put(
    '/add/playwright',
    name='新增UI用例'
)
async def put_playwright(pd: schemas.PlaywrightIn, db: Session = Depends(get_db)):
    """
    导入新的playwright脚本文件
    """
    if pd.id:
        temp_id = await crud.get_playwright(db=db, temp_id=pd.id)
        if not temp_id:
            return await response_code.resp_404()

        await crud.update_playwright(
            db=db,
            temp_id=pd.id,
            project_name=pd.project_name,
            temp_name=pd.temp_name,
            rows=pd.text.count('\n'),
            text=pd.text,
        )
        return await response_code.resp_200()

    temp_name = await crud.get_playwright(db=db, temp_name=pd.temp_name)
    if temp_name:
        return await response_code.resp_400(message='存在同名模板')

    await crud.create_playwright(db=db, data=pd, rows=pd.text.count('\n'))
    return await response_code.resp_200()


@case_ui.get(
    '/get/playwright/data',
    name='获取UT数据详情',
    response_model=schemas.PlaywrightOut,
    response_class=response_code.MyJSONResponse,
)
async def get_playwright_data(temp_id: int, db: Session = Depends(get_db)):
    """
    获取playwright详情
    """
    temp_info = await crud.get_playwright(db=db, temp_id=temp_id)
    return temp_info[0] or await response_code.resp_404()


@case_ui.get(
    '/get/playwright/list',
    name='获取UI数据列表',
    response_model=Page[schemas.PlaywrightOut],
    response_class=response_code.MyJSONResponse,
    response_model_exclude=['text']
)
async def get_playwright_list(db: Session = Depends(get_db)):
    """
    获取playwright列表
    """
    temp_info = await crud.get_playwright(db=db)
    return paginate(temp_info) or await response_code.resp_404()


@case_ui.get(
    '/get/playwright/case/{temp_id}',
    name='获取文本中对应的数据',
)
async def get_playwright_case(temp_id: int, db: Session = Depends(get_db)):
    """
    获取测试数据
    """
    temp_info = await crud.get_playwright(db=db, temp_id=temp_id)
    if temp_info:
        data = await case_data.get_row_data(temp_info=temp_info[0])
        if data:
            return await response_code.resp_200(data=data)
        else:
            return await response_code.resp_400(message='没有提取到内容')
    else:
        return await response_code.resp_404()


@case_ui.delete(
    '/del/playwright/data/{temp_id}',
    name='删除UI数据列表,'
)
async def del_playwright_data(temp_id: int, db: Session = Depends(get_db)):
    """
    删除UI数据列表
    """
    await crud.del_template_data(db=db, temp_id=temp_id)
    return await response_code.resp_200()


add_pagination(case_ui)
