#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: crud.py
@Time: 2023/4/16-14:42
"""

from sqlalchemy.orm import Session
from apps.whole_conf import models, schemas


async def get_info(db: Session):
    """
    获取信息
    :param db:
    :return:
    """
    return db.query(models.WholeConfInfo).filter(models.WholeConfInfo.id == 1).first()


async def set_info(db: Session, conf_info: schemas.WholeConfIn):
    """
    创建/更新信息
    :param db:
    :param conf_info:
    :return:
    """
    db_info = db.query(models.WholeConfInfo).filter(models.WholeConfInfo.id == 1).first()
    if db_info:
        db.query(models.WholeConfInfo).filter(models.WholeConfInfo.id == 1).delete()
        db_info = models.WholeConfInfo(**conf_info.dict())
        db.add(db_info)
        db.commit()
        db.refresh(db_info)
        return db_info
    else:
        db_info = models.WholeConfInfo(**conf_info.dict())
        db.add(db_info)
        db.commit()
        db.refresh(db_info)
        return db_info
