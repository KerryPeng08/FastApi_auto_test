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
    conf_info = await crud.get_info(db=db)
    if conf_info:
        return conf_info
    else:
        return {
            'host': [
                {'key': '本地', 'value': 'http://127.0.0.1'}
            ],
            'project': [
                {'key': '', 'value': ''}
            ],
            'unify_res': [
                {'key': 'code', 'value': 0, 'type': 'string'}
            ],
            'db_conf': {
                'host': '',
                'user': '',
                'password': '',
                'database': '',
                'port': 3306,
                'charset': 'utf8',
            }
        }


@conf.put(
    '/set/setting',
    name='更新全局配置信息',
    response_model=schemas.WholeConfOut
)
async def setting_conf(conf_info: schemas.WholeConfIn, db: Session = Depends(get_db)):
    for host in conf_info.host:
        if host.value[-1] == '/':
            host.value = host.value[:-1]
    return await crud.set_info(db=db, conf_info=conf_info)
