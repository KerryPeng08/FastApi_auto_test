#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/4-15:30
"""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, BackgroundTasks
from typing import List
from .tool import YApi
from depends import get_db
from setting import YAPI_INFO
from apps.api_pool import schemas
from apps.api_pool import crud as pool_crud
from apps import response_code

pool = APIRouter()


async def download_api(db: Session, yapi: YApi):
    """
    后台全量下载接口数据
    :return:
    """
    return await yapi.header_all_data(db=db)


# response_model=List[schemas.YApiOut],
@pool.put('/download/projects/data', name='从YApi全量下载更新接口数据')
async def download_projects_data(
        background_tasks: BackgroundTasks,
        really: bool = False,
        db: Session = Depends(get_db)
):
    if really:
        # 登录
        yapi = YApi(YAPI_INFO['host'])
        if not await yapi.login(email=YAPI_INFO['email'], password=YAPI_INFO['password']):
            return await response_code.resp_400(message='YApi登录失败')
        # 删除数据
        await pool_crud.del_api_all(db=db)
        await pool_crud.del_project_all(db=db)
        # 后台任务下载
        background_tasks.add_task(download_api, db, yapi)
        return await response_code.resp_200(message='后台任务创建成功')


#
@pool.put('/download/project/{project_id}', response_model=List[schemas.YApiDataOut], name='按项目ID覆盖更新接口池')
async def download_project_name(project_id: int, db: Session = Depends(get_db)):
    # 查询项目数据
    pro_info = await pool_crud.get_project_info(db=db, project_id=project_id)
    if pro_info:
        # 登录YApi
        yapi = YApi(YAPI_INFO['host'])
        if not await yapi.login(email=YAPI_INFO['email'], password=YAPI_INFO['password']):
            return await response_code.resp_400(message='YApi登录失败')
        await pool_crud.del_project_api_info(db=db, project_id=project_id)

        # 下载数据
        return await yapi.header_project_data(db=db, project_id=project_id)
    else:
        return await response_code.resp_404()


@pool.put('/download/{api_id}', response_model=schemas.YApiDataOut, name='按接口ID覆盖更新接口')
async def download_api_title(api_id: int, db: Session = Depends(get_db)):
    # 查询项目数据
    api_info = await pool_crud.get_api(db=db, api_id=api_id)
    if api_info:
        # 登录YApi
        yapi = YApi(YAPI_INFO['host'])
        if not await yapi.login(email=YAPI_INFO['email'], password=YAPI_INFO['password']):
            return await response_code.resp_400(message='YApi登录失败')
        await pool_crud.del_api_info(db=db, api_id=api_id)

        # 下载数据
        return await yapi.header_api_data(db=db, api_id=api_id, project_id=api_info.project_id)
    else:
        return await response_code.resp_404()


@pool.get('/project/data', response_model=List[schemas.YApiOut], name='获取YApi项目数据')
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


@pool.get('/api/data', response_model=List[schemas.YApiDataOut], name='获取单项目中的接口数据')
async def get_api_data(project_name: str = None, project_id: int = None, db: Session = Depends(get_db)):
    if project_id:
        api_info = await pool_crud.get_api_info(db=db, project_id=project_id)
        if api_info:
            return api_info

    if project_name:
        api_info = await pool_crud.get_api_info(db=db, project_name=project_name)
        if api_info:
            return api_info

    return await response_code.resp_404()


@pool.get('/getApi/', response_model=schemas.YApiDataOut, name='获取单个接口的信息')
async def get_api_id(api_id: int = None, title: str = None, db: Session = Depends(get_db)):
    if api_id:
        api_info = await pool_crud.get_api(db=db, api_id=api_id)
        if api_info:
            return api_info

    if title:
        api_info = await pool_crud.get_api(db=db, title=title)
        if api_info:
            return api_info

    return await response_code.resp_404()
