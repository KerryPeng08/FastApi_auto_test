#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/4-15:30
"""

import time
from typing import List, Optional
from fastapi import APIRouter, UploadFile, HTTPException, status, Depends
from sqlalchemy.orm import Session
from apps.template import crud, schemas
from tools.database import Base, engine
from .tool import ParseData
from depends import get_db
from tools import CreateExcel
from starlette.responses import FileResponse

template = APIRouter()

Base.metadata.create_all(bind=engine)


@template.post('/upload/har', response_model=schemas.TemplateOut, response_model_exclude_unset=True,
               name='上传Charles的har文件')
async def upload_file_har(temp_name: str, project_name: schemas.TempEnum, file: UploadFile,
                          db: Session = Depends(get_db)):
    """
    1、上传文件后，解析数据，形成模板数据\n
    2、自动过滤掉'js','css','image'\n
    3、记录原始数据，拆解params、body、json数据
    """
    if file.content_type != 'application/har+json':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='文件类型错误，只支持har格式文件')

    if await crud.get_temp_name(db=db, temp_name=temp_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='模板名称已存在')

    return await ParseData.pares_data(db=db, temp_name=temp_name, project_name=project_name, har_data=file.file.read())


@template.get('/name', response_model=List[schemas.TempTestCase], response_model_exclude_unset=True, name='查询模板数据')
async def get_templates(temp_name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    1、查询已存在的测试模板/场景\n
    2、场景包含的测试用例
    3、默认返回所有模板
    """
    if not temp_name:
        templates = await crud.get_temp_name(db=db)
    else:
        templates = await crud.get_temp_name(db=db, temp_name=temp_name)

    out_info = []
    for temp in templates:
        case_info = await crud.get_temp_case_info(db=db, temp_id=temp.id)
        temp_info = {
            'temp_name': temp.temp_name,
            'project_name': temp.project_name,
            'id': temp.id,
            'api_count': temp.api_count,
            'created_at': temp.created_at,
            'updated_at': temp.updated_at,
        }
        temp_info.update(case_info)
        out_info.append(temp_info)

    if out_info:
        return out_info
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未查询到模板信息')


@template.put('/name', response_model=schemas.TemplateOut, name='修改模板名称')
async def update_name(old_name: str, new_name: str, db: Session = Depends(get_db)):
    """
    修改模板名称
    """
    temp_name = await crud.put_temp_name(db=db, old_name=old_name, new_name=new_name)
    if temp_name:
        return temp_name
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未查询到模板名称')


@template.delete('/name', name='删除模板数据')
async def delete_name(temp_name: str, db: Session = Depends(get_db)):
    """
    删除模板数据
    """
    template_data = await crud.del_template_data(db=db, temp_name=temp_name)
    if template_data:
        return {'message': '删除成功'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未查询到模板名称')


@template.get('/data', response_model=List[schemas.TemplateDataOut], response_model_exclude_unset=True,
              response_model_exclude=['headers'], name='查询模板接口数据')
async def get_template_data(temp_name: str, db: Session = Depends(get_db)):
    """
    按模板名称查询接口原始数据
    """
    template_data = await crud.get_template_data(db=db, temp_name=temp_name)
    if template_data:
        return template_data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未查询到模板名称')


@template.get('/download/excel', name='下载模板数据-excel', deprecated=True)
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
            filename=f'{temp_name}.xlsx'
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未查询到模板名称')
