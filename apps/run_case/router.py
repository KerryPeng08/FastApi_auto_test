#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/23-13:45
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from depends import get_db
from .tool.run_case import run_case as run
from apps import response_code
from apps.case_service import crud as case_crud

run_case = APIRouter()


@run_case.post(
    '/case',
    response_class=response_code.MyJSONResponse,
    name='按用例Id执行'
)
async def run_case_name(request: Request, case_ids: List[int], db: Session = Depends(get_db)):
    if not case_ids:
        return await response_code.resp_400()

    return await run(db=db, request=request, case_ids=case_ids)


@run_case.post(
    '/temp',
    response_class=response_code.MyJSONResponse,
    name='按模板Id执行'
)
async def run_case_name(request: Request, temp_id: int, db: Session = Depends(get_db)):
    case_ids = await case_crud.get_case_ids(db=db, temp_id=temp_id)
    return await run(db=db, request=request, case_ids=[x[0] for x in case_ids])
