#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: crud.py
@Time: 2022/8/23-13:56
"""

from sqlalchemy.orm import Session
from apps.template import models


async def get_pro_name(db: Session, temp_id: int):
    temp_info = db.query(models.Template).filter(models.Template.id == temp_id).first()
    return temp_info.project_name
