#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/4-15:30
"""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .tool import YApi
from depends import get_db
from setting import YAPI_INFO
from apps.api_pool import schemas
from apps.api_pool import crud as pool_crud

pool = APIRouter()


@pool.get('/download/project/data', response_model=List[schemas.YApiOut], name='从YApi全量下载接口数据')
async def download_project_data(really: bool = False, db: Session = Depends(get_db)):
    if really:
        yapi = YApi(YAPI_INFO['host'])
        await yapi.login(email=YAPI_INFO['email'], password=YAPI_INFO['password'])
        return await yapi.header_all_data(db=db)


@pool.get('/get_project/data', response_model=List[schemas.YApiOut], name='获取YApi项目数据')
async def get_project_data(
        group_name: str = None,
        project_name: str = None,
        project_id: int = None,
        db: Session = Depends(get_db)
):
    return await pool_crud.get_project_info(
        db=db,
        group_name=group_name,
        project_name=project_name,
        project_id=project_id
    )


@pool.get('/get_api/data', response_model=List[schemas.YApiDataOut], name='获取单项目中的接口数据')
async def get_api_data(project_name: str = None, project_id: int = None, db: Session = Depends(get_db)):
    if project_id:
        return await pool_crud.get_api_info(db=db, project_id=project_id)

    if project_name:
        return await pool_crud.get_api_info(db=db, project_name=project_name)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未获取到数据')


@pool.get('/get_api/{id}', response_model=schemas.YApiDataOut, name='获取单个接口的信息')
async def get_api(id: int, db: Session = Depends(get_db)):
    return await pool_crud.get_api(db=db, api_id=id)
