#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2023/2/25-21:07
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps import response_code
from depends import get_db

from apps.template import crud as t_crud
from apps.template import schemas as t_schemas
from apps.case_service import crud as c_crud

from apps.own_params_rep import schemas, crud

own_rep = APIRouter()


@own_rep.get(
    '/url/for/data',
    name='通过url+method查找相同接口数据',
    response_model=List[t_schemas.TempChangeParams]
    # response_model_exclude=['headers', 'file_data', 'response'],
)
async def url_for_data(method: str, path: str, db: Session = Depends(get_db)):
    """
    通过url+method，查询出模板的信息，以及关联的用例信息
    """
    temp_info = await crud.get_all_url_method(db=db, method=method.upper(), path=path.strip())
    return [{
        'temp_id': x[0],
        'temp_name': x[1],
        'number': x[2],
        'path': x[3],
        'params': x[4],
        'data': x[5],
    } for x in temp_info] if temp_info else await response_code.resp_404()


@own_rep.get(
    '/temp/for/casedata',
    name='通过模板id和number获取用例id和number和其他信息'
)
async def temp_for_case_data(temp_id: int, number: int, db: Session = Depends(get_db)):
    """
    通过模板id和number获取用例信息
    """
    db_info = await crud.get_temp_fo_case_info(db=db, temp_id=temp_id, number=number)
    return [{
        'case_id': x[0],
        'number': x[1],
        'path': x[2],
        'params': x[3],
        'data': x[4],
    } for x in db_info] if db_info else await response_code.resp_400()


@own_rep.put(
    '/url/edit',
    name='修改url',

)
async def url_edit(ue: schemas.UrlEdit, db: Session = Depends(get_db)):
    if ue.temp_id and ue.case_id:
        return await response_code.resp_400(message='temp_id和case_id不能同时存在')

    if ue.temp_id:
        template_data = await t_crud.get_template_data(db=db, temp_id=ue.temp_id)
        if not template_data:
            return await response_code.resp_404(message='没有获取到这个模板id')

        if ue.rep_url:
            await crud.temp_rep_url_edit(
                db=db,
                temp_id=ue.temp_id,
                number=ue.number,
                old_url=ue.old_url.strip(),
                new_url=ue.new_url.strip()
            )
        else:
            await crud.temp_rep_url_edit(
                db=db,
                temp_id=ue.temp_id,
                number=ue.number,
                old_url=ue.new_url.strip(),
                new_url=ue.old_url.strip()
            )

        return await response_code.resp_200()

    if ue.case_id:
        case_info = await c_crud.get_case_info(db=db, case_id=ue.case_id)
        if not case_info:
            return await response_code.resp_404(message='没有获取到这个用例id')

        if ue.rep_url:
            await crud.case_rep_url_edit(
                db=db,
                case_id=ue.case_id,
                number=ue.number,
                old_url=ue.old_url.strip(),
                new_url=ue.new_url.strip()
            )
        else:
            await crud.case_rep_url_edit(
                db=db,
                case_id=ue.case_id,
                number=ue.number,
                old_url=ue.new_url.strip(),
                new_url=ue.old_url.strip()
            )

        return await response_code.resp_200()
