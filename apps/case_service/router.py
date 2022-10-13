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
import shutil
from typing import List
from fastapi import APIRouter, UploadFile, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
from starlette.background import BackgroundTask
from depends import get_db
from apps import response_code
from tools.check_case_json import CheckJson
from tools import OperationJson
from setting import ALLURE_PATH
from .tool.get_case_data_info import GetCaseDataInfo

from apps.template import crud as temp_crud
from apps.case_service import crud, schemas
from apps.case_service.tool import insert, cover_insert
from apps.template.tool import GenerateCase

case_service = APIRouter()


@case_service.get(
    '/init/data/list',
    response_model=schemas.TestCaseDataOut,
    response_class=response_code.MyJSONResponse,
    response_model_exclude_unset=True,
    name='获取预处理后的模板数据'
)
async def test_case_data(temp_name: str, mode: schemas.ModeEnum, db: Session = Depends(get_db)):
    """
    自动处理部分接口数据上下级关联数据
    """
    if mode != schemas.ModeEnum.service:
        return await response_code.resp_400(message=f'该模式仅支持{schemas.ModeEnum.service}模式')

    template_data = await temp_crud.get_template_data(db=db, temp_name=temp_name)
    if template_data:
        return await GenerateCase().read_template_to_api(temp_name=temp_name, mode=mode, template_data=template_data)

    return await response_code.resp_404()


@case_service.get(
    '/download/init/data/json',
    response_model=schemas.TestCaseDataOut,
    response_model_exclude_unset=True,
    name='下载预处理后的模板数据-json',
)
async def download_case_data(temp_name: str, mode: schemas.ModeEnum, db: Session = Depends(get_db)):
    """
    自动处理部分接口上下级关联数据\n
    json格式化数据下载
    """
    if mode != schemas.ModeEnum.service:
        return await response_code.resp_400(message=f'该模式仅支持{schemas.ModeEnum.service}模式')

    template_data = await temp_crud.get_template_data(db=db, temp_name=temp_name)
    if template_data:
        test_data = await GenerateCase().read_template_to_api(temp_name=temp_name, mode=mode,
                                                              template_data=template_data)
        path = f'./files/json/{time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))}.json'
        await OperationJson.write(path=path, data=test_data)
        return FileResponse(
            path=path,
            filename=f'{temp_name}.json',
            background=BackgroundTask(lambda: os.remove(path))
        )

    return await response_code.resp_404()


@case_service.post(
    '/upload/json',
    response_model=schemas.TestCaseOut,
    response_class=response_code.MyJSONResponse,
    name='上传测试数据-json'
)
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

        if not await crud.get_case_info(db=db, case_id=case_id):
            return await response_code.resp_404()

        return await cover_insert(db=db, case_id=case_id, case_data=case_data)
    else:  # 不覆盖
        if not case_name:
            return await response_code.resp_400(message='未输入case_name')
        return await insert(db=db, case_name=case_name, temp_id=db_temp[0].id, case_data=case_data)


@case_service.get(
    '/data/{case_id}',
    response_model=schemas.TestCaseDataOut,
    response_class=response_code.MyJSONResponse,
    response_model_exclude_unset=True,
    name='查看用例测试数据'
)
async def case_data_info(case_id: int, db: Session = Depends(get_db)):
    """
    查看测试数据
    """
    case_info = await crud.get_case_info(db=db, case_id=case_id)
    if not case_info:
        return await response_code.resp_404()

    return await GetCaseDataInfo().service(
        case_info=case_info,
        case_data_info=await crud.get_case_data(db=db, case_id=case_id)
    )


@case_service.get(
    '/download/data/{case_id}',
    response_model=schemas.TestCaseDataOut,
    response_class=response_code.MyJSONResponse,
    response_model_exclude_unset=True,
    name='下载测试数据-Json'
)
async def download_case_data_info(case_id: int, db: Session = Depends(get_db)):
    """
    下载测试数据
    """
    case_info = await crud.get_case_info(db=db, case_id=case_id)
    if not case_info:
        return await response_code.resp_404()

    case_data = await GetCaseDataInfo().service(
        case_info=case_info,
        case_data_info=await crud.get_case_data(db=db, case_id=case_id)
    )

    path = f'./files/json/{time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))}.json'
    await OperationJson.write(path=path, data=case_data)
    return FileResponse(
        path=path,
        filename=f'{case_info[0].case_name}.json',
        background=BackgroundTask(lambda: os.remove(path))
    )


@case_service.get(
    '/data/case/list',
    response_model=List[schemas.TestCaseInfoOut],
    response_class=response_code.MyJSONResponse,
    name='查看测试用例列表'
)
async def case_data_list(db: Session = Depends(get_db)):
    """
    查看测试用例列表
    """
    test_case = await crud.get_case_info(db=db, all=True)

    case_info = []
    for case in test_case:
        temp_info = await temp_crud.get_temp_name(db=db, temp_id=case.temp_id)
        case_info.append(
            {
                "name": f"{temp_info[0].project_name}-{temp_info[0].temp_name}-{case.case_name}",
                "case_id": case.id,
                "api_count": case.case_count,
                "run_order": case.run_order,
                "mode": case.mode,
                "created_at": case.created_at
            }
        )

    return case_info or await response_code.resp_404()


@case_service.delete(
    '/del/{case_id}',
    name='删除测试数据'
)
async def del_case(case_id: int, db: Session = Depends(get_db)):
    if not await crud.get_case_info(db=db, case_id=case_id):
        return await response_code.resp_404()
    await crud.del_case_data(db=db, case_id=case_id)
    shutil.rmtree(f"{ALLURE_PATH}/{case_id}", ignore_errors=True)
    return await response_code.resp_200(message=f'用例{case_id}删除成功')


@case_service.get(
    '/query/urls',
    response_model=List[schemas.TestCaseDataOut2],
    response_class=response_code.MyJSONResponse,
    name='查询url数据'
)
async def query_urls(url: str = Query(..., min_length=5), db: Session = Depends(get_db)):
    return await crud.get_urls(db=db, url=url) or await response_code.resp_404()


@case_service.put(
    '/update/urls',
    response_model=List[schemas.TestCaseDataOut2],
    response_class=response_code.MyJSONResponse,
    name='批量修改url'
)
async def update_urls(
        old_url: str = Query(..., min_length=5),
        new_url: str = Query(..., min_length=5),
        db: Session = Depends(get_db)
):
    return await crud.update_urls(db=db, old_url=old_url, new_url=new_url) or await response_code.resp_404()


@case_service.get(
    '/query/api/info',
    response_model=schemas.TestCaseDataOut1,
    response_class=response_code.MyJSONResponse,
    name='按用例/序号查看API数据'
)
async def get_api_info(case_id: int, number: int, db: Session = Depends(get_db)):
    return await crud.get_api_info(db=db, case_id=case_id, number=number) or await response_code.resp_404()


@case_service.put(
    '/update/api/info',
    name='按用例/序号修改API数据'
)
async def put_api_info(api_info: schemas.TestCaseDataOut1, db: Session = Depends(get_db)):
    if await crud.update_api_info(db=db, api_info=api_info):
        return await response_code.resp_200()
    else:
        return await response_code.resp_404(message='修改失败，未获取到内容')
