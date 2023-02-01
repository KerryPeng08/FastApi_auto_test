#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/4-15:30
"""

import os
import time
from typing import List
from fastapi import APIRouter, UploadFile, Depends, Form, File, Query
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
from starlette.background import BackgroundTask
from apps import response_code
from depends import get_db

from apps.template import crud, schemas
from apps.case_service import schemas as case_schemas
from apps.case_service import crud as case_crud
from apps.template.tool import ParseData, check_num, GenerateCase
from tools import CreateExcel, OperationJson
from .tool import InsertTempData, DelTempData

template = APIRouter()


@template.post(
    '/upload/har',
    response_model=schemas.TemplateOut,
    response_class=response_code.MyJSONResponse,
    response_model_exclude_unset=True,
    name='上传Charles的har文件-先解析-再写入'
)
async def upload_file_har(
        temp_name: str,
        project_name: schemas.TempEnum,
        file: UploadFile,
        db: Session = Depends(get_db)
):
    """
    1、上传文件后，解析数据，形成模板数据\n
    2、自动过滤掉'js','css','image'\n
    3、记录原始数据，拆解params、body、json数据
    """
    if file.content_type != 'application/har+json':
        return await response_code.resp_400(message=f'文件类型错误，只支持har格式文件')

    if await crud.get_temp_name(db=db, temp_name=temp_name):
        return await response_code.resp_400(message=f'模板名称已存在')

    # 解析数据，拿到解析结果
    temp_info = await ParseData.pares_data(
        har_data=file.file.read()
    )

    # 创建主表数据
    db_template = await crud.create_template(db=db, temp_name=temp_name, project_name=project_name)
    # 批量写入数据
    for temp in temp_info:
        await crud.create_template_data(db=db, data=schemas.TemplateDataIn(**temp), temp_id=db_template.id)
    return await crud.update_template(db=db, temp_id=db_template.id, api_count=len(temp_info))


@template.post(
    '/analysis/har',
    response_model=List[schemas.TemplateDataIn],
    response_class=response_code.MyJSONResponse,
    response_model_exclude_unset=True,
    name='上传Charles的har文件-仅解析-不写入',
    response_model_exclude=['headers', 'file_data']
)
async def analysis_file_har(file: UploadFile):
    """
    仅解析Charles数据，不返回['headers', 'file_data', 'response']\n
    用于同一接口多次使用时，查看请求数据的不同处
    """
    if file.content_type != 'application/har+json':
        return await response_code.resp_400(message=f'文件类型错误，只支持har格式文件')

    return await ParseData.pares_data(har_data=file.file.read())


@template.put(
    '/insert/har',
    response_model=case_schemas.TestCaseDataOut,
    # response_class=response_code.MyJSONResponse,
    response_model_exclude_unset=True,
    name='插入原始数据到模板中，并提供插入数据的预处理数据下载',
    # response_model_exclude=['headers', 'file_data']
)
async def insert_har(
        temp_id: int = Query(description='模板id'),
        numbers: str = Form(description='索引-整数列表,使用英文逗号隔开', min_length=1),
        file: UploadFile = File(description='上传Har文件'),
        db: Session = Depends(get_db)
):
    """
    按num序号，按顺序插入原始数据到模板中
    """
    if file.content_type != 'application/har+json':
        return await response_code.resp_400(message=f'文件类型错误，只支持har格式文件')

    har_data = await ParseData.pares_data(har_data=file.file.read())
    template_data = await crud.get_template_data(db=db, temp_id=temp_id)
    if not template_data:
        return await response_code.resp_404(message='没有获取到这个模板id')

    try:
        num_list = await check_num(nums=numbers, har_data=har_data, template_data=template_data)
    except ValueError as e:
        return await response_code.resp_400(
            message=f'序号校验错误, 错误:{e}',
            data={
                'numbers': numbers,
                'har_length': len(har_data),
            }
        )
    else:
        if len(num_list) == 1:
            new_numbers = await InsertTempData.one_data(
                db=db,
                temp_id=temp_id,
                num_list=num_list,
                har_data=har_data,
                template_data=template_data
            )
        else:
            new_numbers = await InsertTempData.many_data(
                db=db,
                temp_id=temp_id,
                num_list=num_list,
                har_data=har_data,
                template_data=template_data
            )

    test_data = await GenerateCase().read_template_to_api(
        temp_name=str(temp_id),
        mode=case_schemas.ModeEnum.service,
        fail_stop=True,
        template_data=await crud.get_template_data(db=db, temp_id=temp_id, numbers=new_numbers)
    )

    path = f'./files/json/{time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))}.json'
    await OperationJson.write(path=path, data=test_data)
    return FileResponse(
        path=path,
        filename=f'模板{temp_id}_新增数据.json',
        background=BackgroundTask(lambda: os.remove(path))
    )


@template.delete(
    '/del/part',
    response_model=List[schemas.TemplateDataIn],
    response_class=response_code.MyJSONResponse,
    response_model_exclude_unset=True,
    name='删除部分模板数据',
    response_model_exclude=['headers', 'file_data']
)
async def del_har(
        temp_id: int = Query(description='模板id'),
        numbers: str = Form(description='索引-整数列表,使用英文逗号隔开', min_length=1),
        db: Session = Depends(get_db)
):
    template_data = await crud.get_template_data(db=db, temp_id=temp_id)
    if not template_data:
        return await response_code.resp_404(message='没有获取到这个模板id')

    try:
        num_list = await check_num(nums=numbers, template_data=template_data)
    except ValueError as e:
        return await response_code.resp_400(
            message=f'序号校验错误, 错误:{e}',
            data={
                'numbers': numbers,
            }
        )
    else:
        await DelTempData.del_data(
            db=db,
            temp_id=temp_id,
            num_list=num_list,
            template_data=template_data
        )
        return await response_code.resp_200(
            data={
                'numbers': numbers,
            }
        )


@template.delete(
    '/del/all',
    name='删除全部模板数据'
)
async def delete_name(temp_id: int, db: Session = Depends(get_db)):
    """
    删除模板数据
    """

    temp_info = await crud.get_temp_name(db=db, temp_id=temp_id)

    if temp_info:
        case_info = await case_crud.get_case(db=db, temp_id=temp_info[0].id)
        if case_info:
            return await response_code.resp_400(message='模板下还存在用例')
        else:
            template_data = await crud.del_template_data_all(db=db, temp_id=temp_info[0].id)
            if template_data:
                return await response_code.resp_200(message='删除成功')
            else:
                return await response_code.resp_400()
    else:
        return await response_code.resp_404()


@template.get(
    '/name/list',
    response_model=List[schemas.TempTestCase],
    response_class=response_code.MyJSONResponse,
    response_model_exclude_unset=True,
    name='查询模板数据'
)
async def get_templates(
        temp_name: str = None,
        temp_id: int = None,
        outline: bool = True,
        db: Session = Depends(get_db)
):
    """
    1、查询已存在的测试模板/场景\n
    2、场景包含的测试用例\n
    3、默认返回所有模板
    """
    if temp_id:
        templates = await crud.get_temp_name(db=db, temp_id=temp_id)
    elif temp_name:
        templates = await crud.get_temp_name(db=db, temp_name=temp_name, like=True)
    else:
        templates = await crud.get_temp_name(db=db)

    out_info = []
    for temp in templates:
        case_info = await crud.get_temp_case_info(db=db, temp_id=temp.id, outline=outline)
        temp_info = {
            'temp_name': temp.temp_name,
            'project_name': temp.project_name,
            'id': temp.id,
            'api_count': temp.api_count,
            'created_at': temp.created_at,
            'updated_at': temp.updated_at,
        } if outline is False else {
            'temp_name': temp.temp_name,
            'id': temp.id,
        }
        temp_info.update(case_info)
        out_info.append(temp_info)

    return out_info or await response_code.resp_404()


@template.put(
    '/name/edit',
    response_model=schemas.TemplateOut,
    response_class=response_code.MyJSONResponse,
    name='修改模板名称'
)
async def update_name(new_name: str, old_name: str = None, temp_id: int = None, db: Session = Depends(get_db)):
    """
    修改模板名称
    """
    return await crud.put_temp_name(
        db=db,
        temp_id=temp_id, old_name=old_name,
        new_name=new_name
    ) or await response_code.resp_404()


@template.get(
    '/data/list',
    response_model=List[schemas.TemplateDataOut],
    response_class=response_code.MyJSONResponse,
    response_model_exclude_unset=True,
    response_model_exclude=['headers', 'file_data'],
    name='查询模板接口原始数据'
)
async def get_template_data(temp_name: str = None, temp_id: int = None, db: Session = Depends(get_db)):
    """
    按模板名称查询接口原始数据，不返回['headers', 'file_data']
    """
    if temp_name:
        return await crud.get_template_data(db=db, temp_name=temp_name) or await response_code.resp_404()

    if temp_id:
        return await crud.get_template_data(db=db, temp_id=temp_id) or await response_code.resp_404()

    return await response_code.resp_400()


@template.get(
    '/download/excel',
    name='下载模板数据-excel',
    deprecated=True,
    include_in_schema=False
)
async def download_temp_excel(temp_name: str, db: Session = Depends(get_db)):
    """
    将Charles录制的测试场景原始数据下载到excel
    """
    template_data = await crud.get_template_data(db=db, temp_name=temp_name)
    if template_data:
        sheet_name = [temp_name]
        sheet_title = ['域名', '接口地址', '响应状态码', '请求参数', 'JSON或BODY数据', '响应数据']
        sheet_data = [
            [
                [x.host, x.path, x.code, x.params, x.data, x.response] for x in template_data
            ]
        ]
        path = f'./files/excel/{time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))}.xlsx'
        excel = CreateExcel(path=path)
        excel.insert(sheet_name=sheet_name, sheet_title=sheet_title, sheet_data=sheet_data)

        return FileResponse(
            path=path,
            filename=f'{temp_name}.xlsx',
            background=BackgroundTask(lambda: os.remove(path))
        )
    return await response_code.resp_404()

# @template.get(
#     '/diff',
#     name='对比测试模板数据-开发中'
# )
# async def diff_template(name: str, db: Session = Depends(get_db)):
#     pass
