#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: crud.py
@Time: 2022/8/20-21:59
"""
from sqlalchemy.orm import Session
from apps.case_data import models, schemas


async def create_test_case(db: Session, case_name: str, temp_id: int):
    """
    创建测试数据
    :param db:
    :param case_name:
    :param temp_id:
    :return:
    """
    db_case = models.TestCase(case_name=case_name, temp_id=temp_id)
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case


async def update_test_case(db: Session, case_name: str, case_count: int = None):
    """
    更新测试信息
    :param db:
    :param case_name:
    :param case_count:
    :return:
    """
    db_temp = db.query(models.TestCase).filter(models.TestCase.case_name == case_name).first()
    if db_temp:
        db_temp.case_count = case_count
        db.commit()
        db.refresh(db_temp)
        return db_temp


async def create_test_case_data(db: Session, data: schemas.TestCaseDataIn, case_id: int):
    """
    创建测试数据集
    :param db:
    :param data:
    :param case_id:
    :return:
    """
    db_data = models.TestCaseData(**data.dict(), case_id=case_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


async def get_case_name(db: Session, case_name: str = None):
    """
    按用例名称查询数据
    :param db:
    :param case_name:
    :return:
    """
    if case_name:
        return db.query(models.TestCase).filter(models.TestCase.case_name == case_name).first()
    return db.query(models.TestCase).all()
