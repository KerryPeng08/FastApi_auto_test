#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: crud.py
@Time: 2022/8/23-13:56
"""

from sqlalchemy.orm import Session
from apps.template import models
from apps.run_case import models as queue


async def get_pro_name(db: Session, temp_id: int):
    """
    查询模板名称
    :param db:
    :param temp_id:
    :return:
    """
    temp_info = db.query(models.Template).filter(models.Template.id == temp_id).first()
    return temp_info.project_name


async def queue_add(db: Session, data: dict):
    """
    添加消息列队
    :param db:
    :param data:
    :return:
    """
    db_data = queue.RunCaseQueue(**data)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


async def queue_query(db: Session):
    """
    查询
    :param db:
    :return:
    """
    return db.query(queue.RunCaseQueue).all()


async def queue_del(db: Session, queue_id: int):
    """
    删除输出
    :param db:
    :param queue_id:
    :return:
    """
    db.query(queue.RunCaseQueue).filter(queue.RunCaseQueue.id == queue_id).delete()
    db.commit()
