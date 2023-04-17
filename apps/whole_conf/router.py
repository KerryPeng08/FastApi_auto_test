#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2023/4/16-14:42
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from depends import get_db
from apps.whole_conf import crud, schemas

conf = APIRouter()


@conf.get(
    '/get/setting',
    name='获取全局配置信息',
    response_model=schemas.WholeConfOut
)
async def get_setting(db: Session = Depends(get_db)):
    return await crud.get_info(db=db)


@conf.put(
    '/set/setting',
    name='更新全局配置信息',
    response_model=schemas.WholeConfOut
)
async def setting_conf(conf_info: schemas.WholeConfIn, db: Session = Depends(get_db)):
    return await crud.set_info(db=db, conf_info=conf_info)