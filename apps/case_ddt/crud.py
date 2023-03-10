#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: crud.py
@Time: 2022/8/22-9:50
"""

from sqlalchemy.orm import Session
from apps.case_ddt import models, schemas


async def create_test_gather(db: Session, data: schemas.TestGrater):
    """
    创建模板数据集
    :param db:
    :param data:
    :return:
    """
    db_data = models.TestGather(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


async def del_test_gather(db: Session, case_id: int):
    """
    删除测试数据集
    :param db:
    :param case_id:
    :return:
    """
    db.query(models.TestGather).filter(models.TestGather.case_id == case_id).delete()
    db.commit()


async def get_gather(db: Session, case_id: int, number: int = None, suite: int = None):
    """
    模糊查询url
    :param db:
    :param case_id:
    :param number:
    :param suite:
    :return:
    """

    return db.query(models.TestGather).filter(models.TestGather.case_id == case_id).order_by(
        models.TestGather.suite
    ).order_by(
        models.TestGather.number
    ).all()
