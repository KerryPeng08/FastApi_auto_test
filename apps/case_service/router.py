#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/20-22:00
"""

import os
import json
import time
from typing import List
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from apps.case_service import crud, schemas
from apps.template import crud as temp_crud
from .tool import insert, cover_insert
from tools.check_case_json import CheckJson
from depends import get_db
from starlette.responses import FileResponse
from starlette.background import BackgroundTask
from tools import GenerateCase as case_
from tools import OperationJson as json_
from apps import response_code

case_service = APIRouter()


@case_service.get('/init/data/list', response_model=schemas.TestCaseDataOut, name='获取预处理后的模板数据')
async def test_case_data(temp_name: str, mode: schemas.ModeEnum, db: Session = Depends(get_db)):
    """
    自动处理部分接口数据上下级关联数据
    """
    if mode != schemas.ModeEnum.service:
        return await response_code.resp_400(message=f'该模式仅支持{mode}模式')

    template_data = await temp_crud.get_template_data(db=db, temp_name=temp_name)
    if template_data:
        test_data = await case_().read_template_to_api(temp_name=temp_name, mode=mode,
                                                       template_data=template_data)
        return test_data

    return await response_code.resp_404()


@case_service.get('/download/init/data/json', response_model=schemas.TestCaseDataOut, name='下载预处理后的模板数据-json')
async def download_case_data(temp_name: str, mode: schemas.ModeEnum, db: Session = Depends(get_db)):
    """
    自动处理部分接口上下级关联数据\n
    json格式化数据下载
    """
    if mode != schemas.ModeEnum.service:
        return await response_code.resp_400(message=f'该模式仅支持{mode}模式')

    template_data = await temp_crud.get_template_data(db=db, temp_name=temp_name)
    if template_data:
        test_data = await case_().read_template_to_api(temp_name=temp_name, mode=mode,
                                                       template_data=template_data)
        path = f'./files/json/{time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))}.json'
        await json_.write(path=path, data=test_data)
        return FileResponse(
            path=path,
            filename=f'{temp_name}.json',
            background=BackgroundTask(lambda: os.remove(path))
        )

    return await response_code.resp_404()


@case_service.post('/upload/json', response_model=schemas.TestCaseOut, name='上传测试数据-json')
async def test_case_upload_json(temp_name: str, file: UploadFile,
                                case_id: int = None, case_name: str = None, cover: bool = False,
                                db: Session = Depends(get_db)):
    """
    上传json文件，解析后储存测试数据
    """

    if file.content_type != 'application/json':
        return await response_code.resp_400(message='文件类型错误，只支持json格式文件')

    db_temp = await temp_crud.get_temp_name(db=db, temp_name=temp_name)
    if not db_temp:
        return await response_code.resp_404(message='temp_name不存在')

    # 校验数据
    try:
        case_data = json.loads(file.file.read().decode('utf-8'))
    except json.decoder.JSONDecodeError as e:
        return await response_code.resp_400(message=f'json文件格式有错误: {str(e)}')

    msg_list = await CheckJson.check_to_service(db=db, temp_name=temp_name, case_data=case_data['data'])
    if msg_list:
        return await response_code.resp_400(data=msg_list)

    if cover:  # 覆盖
        if not case_id:
            return await response_code.resp_400(message='未输入case_id')

        if not await crud.get_case_name(db=db, case_id=case_id):
            return await response_code.resp_404()

        return await cover_insert(db=db, case_id=case_id, case_data=case_data)
    else:  # 不覆盖
        if not case_name:
            return await response_code.resp_400(message='未输入case_name')
        return await insert(db=db, case_name=case_name, temp_id=db_temp[0].id, case_data=case_data)


@case_service.get('/data/{case_id}', response_model=List[schemas.TestCaseDataOut2], name='查看用例测试数据')
async def case_data(case_id: int, db: Session = Depends(get_db)):
    """
    查看测试数据
    """
    case_info = await crud.get_case_data(db=db, case_id=case_id)
    if case_info:
        return case_info

    return await response_code.resp_404()


@case_service.delete('/del/{case_id}', name='删除测试数据')
async def del_case(case_id: int, db: Session = Depends(get_db)):
    if not await crud.get_case_name(db=db, case_id=case_id):
        return await response_code.resp_404()
    await crud.del_case_data(db=db, case_id=case_id)
    return await response_code.resp_200(message=f'用例{case_id}删除成功')
