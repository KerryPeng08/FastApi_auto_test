#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/20-22:00
"""

import json
import time
from fastapi import APIRouter, UploadFile, HTTPException, status, Depends
from sqlalchemy.orm import Session
from apps.case_service import crud, schemas
from apps.template import crud as temp_crud
from .tool import insert, cover_insert
from tools import GenerateCase, OperationJson
from tools.check_case_json import CheckJson
from depends import get_db
from starlette.responses import FileResponse

case_service = APIRouter()


@case_service.get('/init/data', response_model=schemas.TestCaseDataOut, name='获取预处理后的测试数据')
async def test_case_data(temp_name: str, mode: schemas.ModeEnum, db: Session = Depends(get_db)):
    """
    自动处理部分接口数据上下级关联数据
    """
    if mode != schemas.ModeEnum.service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'该模式仅支持{mode}模式')

    template_data = await temp_crud.get_template_data(db=db, temp_name=temp_name)
    if template_data:
        test_data = await GenerateCase().read_template_to_api(temp_name=temp_name, mode=mode,
                                                              template_data=template_data)
        return test_data

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未查询到模板名称')


@case_service.get('/download/json', response_model=schemas.TestCaseDataOut, name='下载预处理后的测试数据-json')
async def download_case_data(temp_name: str, mode: schemas.ModeEnum, db: Session = Depends(get_db)):
    """
    自动处理部分接口上下级关联数据\n
    json格式化数据下载
    """
    if mode != schemas.ModeEnum.service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'该模式仅支持{mode}模式')

    template_data = await temp_crud.get_template_data(db=db, temp_name=temp_name)
    if template_data:
        test_data = await GenerateCase().read_template_to_api(temp_name=temp_name, mode=mode,
                                                              template_data=template_data)
        path = f'./files/json/{time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))}.json'
        await OperationJson.write(path=path, data=test_data)
        return FileResponse(
            path=path,
            filename=f'{temp_name}.json'
        )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未查询到模板名称')


@case_service.post('/upload/json', response_model=schemas.TestCaseOut, name='上传测试数据-json')
async def test_case_upload_json(temp_name: str, case_name: str, file: UploadFile, cover: bool = False,
                                db: Session = Depends(get_db)):
    """
    上传json文件，解析后储存测试数据
    """

    if file.content_type != 'application/json':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='文件类型错误，只支持json格式文件')

    db_temp = await temp_crud.get_temp_name(db=db, temp_name=temp_name)
    if not db_temp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='模板不存在')

    # 校验数据
    try:
        case_data = json.loads(file.file.read().decode('utf-8'))
    except json.decoder.JSONDecodeError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'json文件格式有错误: {str(e)}')
    msg_list = await CheckJson.check_to_service(case_data=case_data['data'])
    if msg_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg_list)

    if cover:  # 覆盖
        return await cover_insert(db=db, case_name=case_name, temp_id=db_temp.id, case_data=case_data)
    else:  # 不覆盖
        if await crud.get_case_name(db=db, case_name=case_name):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用例名称已存在')
        return await insert(db=db, case_name=case_name, temp_id=db_temp.id, case_data=case_data)
