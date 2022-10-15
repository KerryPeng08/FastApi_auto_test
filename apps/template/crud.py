#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: crud.py
@Time: 2022/8/8-10:19
"""

from sqlalchemy.orm import Session
from apps.template import models, schemas
from apps.case_service import models as case_models


async def create_template(db: Session, temp_name: str, project_name: str):
    """
    创建模板信息
    :param db:
    :param temp_name:
    :param project_name:
    :return:
    """
    db_temp = models.Template(temp_name=temp_name, project_name=project_name)
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


async def update_template(db: Session, temp_name: str, api_count: int = None):
    """
    更新模板信息
    :param db:
    :param temp_name:
    :param api_count:
    :return:
    """
    db_temp = db.query(models.Template).filter(models.Template.temp_name == temp_name).first()
    if db_temp:
        db_temp.api_count = api_count
        db.commit()
        db.refresh(db_temp)
        return db_temp


async def create_template_data(db: Session, data: schemas.TemplateDataIn, temp_id: int):
    """
    创建模板数据集
    :param db:
    :param data:
    :param temp_id:
    :return:
    """
    db_data = models.TemplateData(**data.dict(), temp_id=temp_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


async def get_temp_name(db: Session, temp_name: str = None, temp_id: int = None, like: bool = False):
    """
    按模板名称查询数据
    :param db:
    :param temp_name:
    :param temp_id:
    :param like:
    :return:
    """
    if temp_id:
        return db.query(models.Template).filter(models.Template.id == temp_id).all()

    if temp_name:
        if like:
            return db.query(models.Template).filter(models.Template.temp_name.like(f"%{temp_name}%")).all()
        else:
            return db.query(models.Template).filter(models.Template.temp_name == temp_name).all()

    return db.query(models.Template).all()


async def get_temp_case_info(db: Session, temp_id: int, outline: bool):
    """
    查询模板下有多少条用例
    :param db:
    :param temp_id:
    :param outline:
    :return:
    """
    db_case = db.query(case_models.TestCase).filter(case_models.TestCase.temp_id == temp_id).all()
    case_info = []
    for case in db_case:
        if outline is False:
            case_info.append({'id': case.id, 'mode': case.mode, 'name': case.case_name, 'run_num': case.run_order})
        else:
            case_info.append({'id': case.id, 'name': case.case_name})

    return {'case_count': len(db_case), 'case_info': case_info} if outline is False else {'case_info': case_info}


async def get_template_data(db: Session, temp_name: str = None, temp_id: int = None):
    """
    查询模板数据
    :param db:
    :param temp_name:
    :param temp_id:
    :return:
    """
    if temp_name:
        db_temp = db.query(models.Template).filter(models.Template.temp_name == temp_name).first()
        if db_temp:
            return db.query(models.TemplateData).filter(models.TemplateData.temp_id == db_temp.id).all()

    if temp_id:
        return db.query(models.TemplateData).filter(models.TemplateData.temp_id == temp_id).all()


async def put_temp_name(db: Session, new_name: str, temp_id: int = None, old_name: str = None):
    """
    更新模板名称
    :param db:
    :param temp_id:
    :param old_name:
    :param new_name:
    :return:
    """
    db_temp = None

    if temp_id:
        db_temp = db.query(models.Template).filter(models.Template.id == temp_id).first()

    if old_name:
        db_temp = db.query(models.Template).filter(models.Template.temp_name == old_name).first()

    if db_temp:
        db_temp.temp_name = new_name
        db.commit()
        db.refresh(db_temp)
        return db_temp


async def del_template_data(db: Session, temp_name: str = None, temp_id: int = None):
    """
    删除模板数据
    :param db:
    :param temp_name:
    :param temp_id:
    :return:
    """
    db_temp = None
    if temp_name:
        db_temp = db.query(models.Template).filter(models.Template.temp_name == temp_name).first()

    if temp_id:
        db_temp = db.query(models.Template).filter(models.Template.id == temp_id).first()

    if db_temp:
        db.query(models.TemplateData).filter(models.TemplateData.temp_id == db_temp.id).delete()
        db.query(models.Template).filter(models.Template.id == db_temp.id).delete()
        db.commit()
        return db_temp
