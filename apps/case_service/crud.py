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


async def get_case_info(db: Session, case_name: str = None, case_id: int = None, all_: bool = False):
    """
    按用例名称查询数据
    :param db:
    :param case_name:
    :param case_id:
    :param all_:
    :return:
    """
    if case_id:
        return db.query(models.TestCase).filter(models.TestCase.id == case_id).order_by(models.TestCase.id.desc()).all()

    if case_name:
        return db.query(models.TestCase).filter(models.TestCase.case_name == case_name).order_by(
            models.TestCase.id.desc()
        ).all()
    if all_:
        return db.query(models.TestCase).order_by(models.TestCase.id.desc()).all()


async def get_case_data(db: Session, case_id: int, number: int = None):
    """
    查询测试用例数据
    :param db:
    :param case_id:
    :param number:
    :return:
    """

    if number:
        return db.query(models.TestCaseData).filter(
            models.TestCaseData.case_id == case_id,
            models.TestCaseData.number == number
        ).order_by(
            models.TestCaseData.number
        ).all()
    else:
        return db.query(models.TestCaseData).filter(models.TestCaseData.case_id == case_id).order_by(
            models.TestCaseData.number
        ).all()


async def set_case_config(db: Session, case_id: int, number: int, config: dict):
    """
    设置用例的配置项
    :param db:
    :param case_id:
    :param number:
    :param config:
    :return:
    """
    db_temp = db.query(models.TestCaseData).filter(
        models.TestCaseData.case_id == case_id,
        models.TestCaseData.number == number,
    ).first()

    if db_temp:
        new_config = {}
        for k, v in db_temp.config.items():
            if k in config.keys():
                new_config[k] = config.get(k)
            else:
                new_config[k] = v

        db_temp.config = new_config
        db.commit()
        db.refresh(db_temp)
        return db_temp


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


async def get_case_ids(db: Session, temp_id: int):
    """
    按模板查用例id
    :param db:
    :param temp_id:
    :return:
    """
    return db.query(models.TestCase.id).filter(models.TestCase.temp_id == temp_id).order_by(models.TestCase.id).all()


async def get_urls(db: Session, url: str):
    """
    模糊查询url
    :param db:
    :param url:
    :return:
    """
    return db.query(models.TestCaseData).filter(models.TestCaseData.path.like(f"{url}%")).order_by(
        models.TestCaseData.number
    ).all()


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

    db_info = db.query(models.TestCaseData).filter(models.TestCaseData.path.like(f"{old_url}%")).order_by(
        models.TestCaseData.number
    ).all()

    url_info = []
    for info in db_info:
        info.path = new_url
        db.commit()
        db.refresh(info)
        url_info.append(info)
    return url_info


async def get_api_info(db: Session, case_id: int, number: int):
    """
    查询用例api信息
    :param db:
    :param case_id:
    :param number:
    :return:
    """
    return db.query(models.TestCaseData).filter(
        models.TestCaseData.case_id == case_id,
        models.TestCaseData.number == number
    ).first()


async def update_api_info(db: Session, api_info: schemas.TestCaseDataOut1):
    """
    修改用例api信息
    :param db:
    :param api_info:
    :return:
    """
    if not await get_api_info(db=db, case_id=api_info.case_id, number=api_info.number):
        return False

    db.query(models.TestCaseData).filter(
        models.TestCaseData.case_id == api_info.case_id,
        models.TestCaseData.number == api_info.number
    ).update(api_info.dict())
    db.commit()
    return True


async def update_api_number(db: Session, case_id: int, id_: int, new_number: int):
    """
    更新用例的number
    :param db:
    :param case_id:
    :param id_:
    :param new_number:
    :return:
    """
    db_temp = db.query(models.TestCaseData).filter(
        models.TestCaseData.id == id_,
        models.TestCaseData.case_id == case_id,
    ).first()

    if db_temp:
        db_temp.number = new_number
        db.commit()
        db.refresh(db_temp)
        return db_temp
