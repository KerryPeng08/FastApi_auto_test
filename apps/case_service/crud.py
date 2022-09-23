#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: crud.py
@Time: 2022/8/20-21:59
"""
from sqlalchemy.orm import Session
from apps.case_service import models, schemas


async def create_test_case(db: Session, case_name: str, mode: str, temp_id: int):
    """
    创建测试数据
    :param db:
    :param case_name:
    :param mode:
    :param temp_id:
    :return:
    """
    db_case = models.TestCase(case_name=case_name, mode=mode, temp_id=temp_id)
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case


async def update_test_case(db: Session, case_id: int, case_count: int = None):
    """
    更新测试信息
    :param db:
    :param case_id:
    :param case_count:
    :return:
    """
    db_temp = db.query(models.TestCase).filter(models.TestCase.id == case_id).first()
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


async def del_test_case_data(db: Session, case_id: int):
    """
    删除测试数据，不删除用例
    :param db:
    :param case_id:
    :return:
    """
    db.query(models.TestCaseData).filter(models.TestCaseData.case_id == case_id).delete()
    db.commit()


async def get_case_name(db: Session, case_name: str = None, case_id: int = None):
    """
    按用例名称查询数据
    :param db:
    :param case_name:
    :param case_id:
    :return:
    """
    if case_id:
        return db.query(models.TestCase).filter(models.TestCase.id == case_id).all()

    if case_name:
        return db.query(models.TestCase).filter(models.TestCase.case_name == case_name).all()
    # return db.query(models.TestCase).all()


async def get_case_data(db: Session, case_id: int):
    """
    查询测试用例数据
    :param db:
    :param case_id:
    :return:
    """
    return db.query(models.TestCaseData).filter(models.TestCaseData.case_id == case_id).all()


async def del_case_data(db: Session, case_id: int):
    """
    删除测试数据
    :param db:
    :param case_id:
    :return:
    """
    db.query(models.TestCase).filter(models.TestCase.id == case_id).delete()
    db.query(models.TestCaseData).filter(models.TestCaseData.case_id == case_id).delete()
    db.commit()


async def get_case(db: Session, temp_id: int):
    """
    按模板查用例
    :param db:
    :param temp_id:
    :return:
    """
    return db.query(models.TestCase).filter(models.TestCase.temp_id == temp_id).first()


async def get_urls(db: Session, url: str):
    """
    模糊查询url
    :param db:
    :param url:
    :return:
    """
    return db.query(models.TestCaseData).filter(models.TestCaseData.path.like(f"{url}%")).all()


async def update_urls(db: Session, old_url: str, new_url: str):
    """
    按url查询数据
    :param db:
    :param old_url:
    :param new_url:
    :return:
    """
    if not await get_urls(db=db, url=old_url):
        return None

    db_info = db.query(models.TestCaseData).filter(models.TestCaseData.path.like(f"{old_url}%")).all()

    url_info = []
    for info in db_info:
        info.path = new_url
        db.commit()
        db.refresh(info)
        url_info.append(info)
    return url_info
