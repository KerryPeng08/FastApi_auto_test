#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: crud.py
@Time: 2023/6/9-16:30
"""

from sqlalchemy.orm import Session
from apps.case_ui import models, schemas


async def create_playwright(db: Session, data: schemas.PlaywrightIn, rows: int):
    """
    创建模板信息
    :param db:
    :param data:
    :param rows:
    :return:
    """
    db_temp = models.PlaywrightTemp(**data.dict(), rows=rows)
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


async def get_playwright(db: Session, temp_id: int = None, temp_name: str = None):
    """
    查询内容
    :param db:
    :param temp_id:
    :param temp_name:
    :return:
    """
    if temp_id:
        return db.query(models.PlaywrightTemp).filter(
            models.PlaywrightTemp.id == temp_id
        ).all()

    if temp_name:
        return db.query(models.PlaywrightTemp).filter(
            models.PlaywrightTemp.temp_name == temp_name
        ).all()

    return db.query(models.PlaywrightTemp).order_by(models.PlaywrightTemp.id.desc()).all()


async def update_playwright(db: Session, temp_id: int, project_name: str, temp_name: str, rows: int, text: str):
    """
    更新模板信息
    """
    db_temp = db.query(models.PlaywrightTemp).filter(models.PlaywrightTemp.id == temp_id).first()
    if db_temp:
        db_temp.project_name = project_name
        db_temp.temp_name = temp_name
        db_temp.rows = rows
        db_temp.text = text
        db.commit()
        db.refresh(db_temp)
        return db_temp


async def del_template_data(db: Session, temp_id: int):
    """
    删除部分数据
    :param db:
    :param temp_id:
    :return:
    """
    db.query(models.PlaywrightTemp).filter(
        models.PlaywrightTemp.id == temp_id,
    ).delete()
    db.commit()


async def create_play_case_data(db: Session, data: schemas.PlaywrightDataIn):
    """
    获取测试数据
    :param db:
    :param data:
    :return:
    """
    db_temp = models.PlaywrightCaseDate(**data.dict())
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


async def get_play_case_data(db: Session, case_id: int = None, temp_id: int = None):
    """
    获取测试用例的数据
    :param db:
    :param case_id:
    :param temp_id:
    :return:
    """
    if case_id:
        return db.query(models.PlaywrightCaseDate).filter(
            models.PlaywrightCaseDate.id == case_id
        ).all()

    if temp_id:
        return db.query(models.PlaywrightCaseDate).filter(
            models.PlaywrightCaseDate.temp_id == temp_id
        ).all()

    return ()


async def del_play_case_data(db: Session, case_id: int = None, temp_id: int = None):
    """
    删除测试呼叫
    :param db:
    :param case_id:
    :param temp_id:
    :return:
    """
    if case_id:
        db.query(models.PlaywrightCaseDate).filter(
            models.PlaywrightCaseDate.id == case_id,
        ).delete()
        db.commit()
        return

    if temp_id:
        db.query(models.PlaywrightCaseDate).filter(
            models.PlaywrightCaseDate.temp_id == temp_id,
        ).delete()
        db.commit()
        return


async def update_ui_temp_order(db: Session, temp_id: int):
    """
    更新用例次数
    :param db:
    :param temp_id:
    :return:
    """
    db_case = db.query(models.PlaywrightTemp).filter(models.PlaywrightTemp.id == temp_id).first()
    db_case.run_order = db_case.run_order + 1
    db.commit()
    db.refresh(db_case)
    return db_case
