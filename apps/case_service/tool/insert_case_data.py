#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: insert_case_data.py
@Time: 2022/8/21-21:54
"""

import base64
import json
from sqlalchemy.orm import Session
from apps.case_service import schemas, crud


async def cover_insert(db: Session, case_name: str, temp_id: int, case_data: dict):
    """
    覆盖数据写入
    :param db:
    :param case_name,:
    :param temp_id:
    :param case_data:
    :return:
    """
    # 删除数据，不删除用例名称
    case_id = await crud.del_test_case_data(db=db, case_name=case_name)
    if not case_id:
        db_case = await crud.create_test_case(db=db, case_name=case_name, mode=case_data['mode'], temp_id=temp_id)
        case_id = db_case.id

    case_count = 0
    for data in case_data['data']:
        del data['number']
        await crud.create_test_case_data(db=db, data=schemas.TestCaseDataIn(**data), case_id=case_id)
        case_count += 1

    return await crud.update_test_case(db=db, case_name=case_name, case_count=case_count)


async def insert(db: Session, case_name: str, temp_id: int, case_data: dict):
    """
    不覆盖数据写入
    :param db:
    :param case_name:
    :param case_data:
    :return:
    """
    db_case = await crud.create_test_case(db=db, case_name=case_name, mode=case_data['mode'], temp_id=temp_id)
    case_count = 0
    for data in case_data['data']:
        del data['number']
        await crud.create_test_case_data(db=db, data=schemas.TestCaseDataIn(**data), case_id=db_case.id)
        case_count += 1

    return await crud.update_test_case(db=db, case_name=case_name, case_count=case_count)
