#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/20-22:00
"""

import time
from fastapi import APIRouter, UploadFile, HTTPException, status, Depends
from sqlalchemy.orm import Session
from apps.case_data import crud, schemas
from apps.template import crud as temp_crud
from tool.database import Base, engine
from .tool import GenerateCase
from depends import get_db
from tool import OperationJson
from starlette.responses import FileResponse

case = APIRouter()

Base.metadata.create_all(bind=engine)


@case.get('/init/data', response_model=schemas.ReadTemplate, name='获取预处理后的测试数据')
async def test_case_data(temp_name: str, db: Session = Depends(get_db)):
    """
    自动处理部分接口数据上下级关联数据
    """
    template_data = await temp_crud.get_template_data(db=db, temp_name=temp_name)
    if template_data:
        test_data = await GenerateCase().read_template(temp_name=temp_name, template_data=template_data)
        return test_data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未查询到模板名称')


@case.get('/download/json', name='下载初步处理后的测试数据-json')
async def download_case_data(temp_name: str, db: Session = Depends(get_db)):
    """
    自动处理部分接口上下级关联数据\n
    json格式化数据下载
    """
    template_data = await temp_crud.get_template_data(db=db, temp_name=temp_name)
    if template_data:
        test_data = await GenerateCase().read_template(temp_name=temp_name, template_data=template_data)
        path = f'./files/json/{time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))}.json'
        await OperationJson.write(path=path, data=test_data)
        return FileResponse(
            path=path,
            filename=f'{temp_name}.json'
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未查询到模板名称')


@case.post('/upload/json', name='上传测试数据-json')
async def test_case_upload_json(temp_name: str, case_name, file: UploadFile, db: Session = Depends(get_db)):
    """
    上传json文件，解析后储存测试数据
    """
    if file.content_type != 'application/json':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='文件类型错误，只支持json格式文件')

    if not await temp_crud.get_temp_name(db=db, temp_name=temp_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='模板不存在')

    if await crud.get_case_name(db=db, case_name=case_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用例名称已存在')
