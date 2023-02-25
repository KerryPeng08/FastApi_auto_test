#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: crud.py
@Time: 2023/2/25-21:08
"""

from sqlalchemy.orm import Session
from apps.template import models, schemas
from apps.case_service import models as case_models
from apps.case_service import schemas as case_schemas


async def get_all_url_method(db: Session, method: str, path: str):
    """
    通过url查询全部的接口数据
    :param db:
    :param method:
    :param path:
    :return:
    """
    db_temp = db.query(
        models.Template.id,
        models.Template.temp_name,
        models.TemplateData.number,
        models.TemplateData.path,
        models.TemplateData.params,
        models.TemplateData.data,
    ).filter(
        models.TemplateData.method == method,
        models.TemplateData.path.like(f'{path}%'),
    ).filter(
        models.TemplateData.temp_id == models.Template.id
    ).order_by(
        models.TemplateData.temp_id
    ).limit(50).all()
    return db_temp


async def get_temp_fo_case_info(db: Session, temp_id: int, number: int):
    """
    通过模板id获取case的信息
    :param db:
    :param temp_id:
    :param number:
    :return:
    """
    db_temp = db.query(
        case_models.TestCaseData.case_id,
        case_models.TestCaseData.number,
        case_models.TestCaseData.path,
        case_models.TestCaseData.params,
        case_models.TestCaseData.data,
    ).filter(
        models.TemplateData.temp_id == temp_id,
        models.TemplateData.number == number
    ).filter(
        models.TemplateData.temp_id == case_models.TestCase.temp_id,
        case_models.TestCase.id == case_models.TestCaseData.case_id,
        models.TemplateData.number == case_models.TestCaseData.number
    ).all()
    return db_temp


"""
template相关操作
"""


async def temp_rep_url_edit(db: Session, temp_id: int, number: int, old_url: str, new_url: str):
    """
    替换url
    :param db:
    :param temp_id:
    :param number:
    :param old_url:
    :param new_url:
    :return:
    """
    db_info = db.query(models.TemplateData).filter(
        models.TemplateData.temp_id == temp_id,
        models.TemplateData.number == number,
        models.TemplateData.path == old_url
    ).first()

    if db_info:
        db_info.path = new_url
        db.commit()
        db.refresh(db_info)
        return db_info


"""
test_case相关操作
"""


async def case_rep_url_edit(db: Session, case_id: int, number: int, old_url: str, new_url: str):
    """

    :param db:
    :param case_id:
    :param number:
    :param old_url:
    :param new_url:
    :return:
    """
    db_info = db.query(case_models.TestCaseData).filter(
        case_models.TestCaseData.case_id == case_id,
        case_models.TestCaseData.number == number,
        case_models.TestCaseData.path == old_url
    ).first()

    if db_info:
        db_info.path = new_url
        db.commit()
        db.refresh(db_info)
        return db_info
