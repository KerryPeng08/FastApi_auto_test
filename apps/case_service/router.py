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
from typing import List, Any
from fastapi import APIRouter, UploadFile, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
from starlette.background import BackgroundTask
from depends import get_db
from apps import response_code
from tools.check_case_json import CheckJson
from tools import OperationJson, ExtractParamsPath, RepData
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
async def test_case_data(
        temp_name: str,
        mode: schemas.ModeEnum,
        fail_stop: bool,
        db: Session = Depends(get_db)
):
    """
    自动处理部分接口数据上下级关联数据
    """
    if mode != schemas.ModeEnum.service:
        return await response_code.resp_400(message=f'该模式仅支持{schemas.ModeEnum.service}模式')

    template_data = await temp_crud.get_template_data(db=db, temp_name=temp_name)
    if template_data:
        return await GenerateCase().read_template_to_api(
            temp_name=temp_name,
            mode=mode,
            fail_stop=fail_stop,
            template_data=template_data
        )

    return await response_code.resp_404()


@case_service.get(
    '/download/init/data/json',
    response_model=schemas.TestCaseDataOut,
    response_model_exclude_unset=True,
    name='下载预处理后的模板数据-json',
)
async def download_case_data(
        temp_name: str,
        mode: schemas.ModeEnum,
        fail_stop: bool,
        db: Session = Depends(get_db)
):
    """
    自动处理部分接口上下级关联数据\n
    json格式化数据下载
    """
    if mode != schemas.ModeEnum.service:
        return await response_code.resp_400(message=f'该模式仅支持{schemas.ModeEnum.service}模式')

    template_data = await temp_crud.get_template_data(db=db, temp_name=temp_name)
    if template_data:
        test_data = await GenerateCase().read_template_to_api(
            temp_name=temp_name,
            mode=mode,
            fail_stop=fail_stop,
            template_data=template_data
        )
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
async def test_case_upload_json(
        temp_id: int,
        file: UploadFile,
        case_id: int = None,
        case_name: str = None,
        cover: bool = False,
        db: Session = Depends(get_db)
):
    """
    上传json文件，解析后储存测试数据
    """

    if file.content_type != 'application/json':
        return await response_code.resp_400(message='文件类型错误，只支持json格式文件')

    db_temp = await temp_crud.get_temp_name(db=db, temp_id=temp_id)
    if not db_temp:
        return await response_code.resp_404(message='模板不存在')

    # 校验数据
    try:
        case_data = json.loads(file.file.read().decode('utf-8'))
    except json.decoder.JSONDecodeError as e:
        return await response_code.resp_400(message=f'json文件格式有错误: {str(e)}')

    msg_list = await CheckJson.check_to_service(db=db, temp_id=temp_id, case_data=case_data['data'])
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
    response_model_exclude_unset=True,
    name='查看测试用例列表'
)
async def case_data_list(outline: bool = True, db: Session = Depends(get_db)):
    """
    查看测试用例列表
    """
    test_case = await crud.get_case_info(db=db, all_=True)

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
            } if outline is False else {
                "name": f"{temp_info[0].project_name}-{temp_info[0].temp_name}-{case.case_name}",
                "case_id": case.id
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
    response_model_exclude_unset=True,
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
    response_model_exclude_unset=True,
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


@case_service.put(
    '/swap/one',
    name='编排用例数据的顺序-单次'
)
async def swap_one(
        case_id: int,
        old_number: int,
        new_number: int,
        db: Session = Depends(get_db)
):
    """
    单次替换用例中API的顺序-索引号
    """
    case_data = await crud.get_case_data(db=db, case_id=case_id)
    if not case_data:
        return await response_code.resp_404(message='没有获取到这个用例id')

    # 判断序号
    numbers = {x.number: x.id for x in case_data}
    null_num = [num for num in [old_number, new_number] if num not in [x for x in numbers]]
    if null_num:
        return await response_code.resp_400(message=f'序号{null_num} 不在该用例的序号中')

    # 替换number序号
    id_ = numbers[old_number]
    await crud.update_api_number(db=db, case_id=case_id, id_=id_, new_number=new_number)
    id_ = numbers[new_number]
    await crud.update_api_number(db=db, case_id=case_id, id_=id_, new_number=old_number)

    return await response_code.resp_200(
        data={
            'old_number': old_number,
            'new_number': new_number
        }
    )


@case_service.put(
    '/swap/many',
    name='编排用例数据的顺序-全部'
)
async def swap_many(
        case_id: int,
        new_numbers: List[int],
        db: Session = Depends(get_db)
):
    """
    依次替换用例中API的顺序-索引号
    """
    case_data = await crud.get_case_data(db=db, case_id=case_id)
    if not case_data:
        return await response_code.resp_404(message='没有获取到这个用例id')

    if len(set(new_numbers)) != len(case_data):
        return await response_code.resp_400(
            message=f'new_numbers长度：{len(set(new_numbers))}，'
                    f'与数据库中的numbers长度：{len(case_data)}，不一致'
        )

    # 判断序号
    numbers = {x.number: x.id for x in case_data}
    null_num = [num for num in new_numbers if num not in [x for x in numbers]]
    if null_num:
        return await response_code.resp_400(message=f'序号{null_num} 不在该模板的序号中')

    # 替换number序号
    num_info = False
    for x in range(len(new_numbers)):
        if x != new_numbers[x]:
            await crud.update_api_number(db=db, case_id=case_id, id_=numbers[x], new_number=new_numbers[x])
            num_info = True

    return await response_code.resp_200(
        data={
            'old_number': [x for x in numbers],
            'new_number': new_numbers
        },
        message='Success 请注意-需要同步修改用例文件中 JsonPath 表达式的序号引用'
    ) if num_info else await response_code.resp_200(
        message='数据无变化'
    )


@case_service.put(
    '/set/api/config',
    name='设置用例配置'
)
async def set_api_config(case_id: int, number: int, config: dict, db: Session = Depends(get_db)):
    """
    设置每个接口的配置信息
    """
    if not config:
        return await response_code.resp_400(message='无效配置内容')

    case_data = await crud.get_case_data(db=db, case_id=case_id, number=number)
    if not case_data:
        return await response_code.resp_404(message='没有获取到这个用例配置')

    for k in config.keys():
        if k not in schemas.TestCaseConfig.__fields__.keys():
            return await response_code.resp_400(message=f'无效的key: {k}')

    await crud.set_case_config(db=db, case_id=case_id, number=number, config=config)

    return await response_code.resp_200()


@case_service.get(
    '/response/jsonpath/list',
    name='从原始数据response中获取jsonpath表达式',
)
async def get_response_json_path(case_id: int, extract_contents: Any, db: Session = Depends(get_db)):
    """
    通过用例id从原始数据中获取jsonpath表达式
    """
    case_info = await crud.get_case_info(db=db, case_id=case_id)
    if not case_info:
        return await response_code.resp_404(message='没有获取到这个用例id')

    temp_data = await temp_crud.get_template_data(db=db, temp_id=case_info[0].temp_id)
    value_list = ExtractParamsPath.get_value_path(
        extract_contents=extract_contents,
        my_data=temp_data,
        type_='response'
    )
    return await response_code.resp_200(
        data=value_list
    ) if value_list.get('extract_contents') else await response_code.resp_404()


@case_service.get(
    '/casedata/jsonpath/list',
    name='从测试数据中获取会被替换的数据'
)
async def get_case_data_json_path(case_id: int, extract_contents: Any, new_str: str, db: Session = Depends(get_db)):
    """
    通过用例id从测试数据url、params、data中预览会被替换的数据
    """
    if "{{" not in new_str and "}}" not in new_str and "$" not in new_str:
        return await response_code.resp_400(message='表达式格式有误')

    case_info = await crud.get_case_info(db=db, case_id=case_id)
    if not case_info:
        return await response_code.resp_404(message='没有获取到这个用例id')

    case_data = await crud.get_case_data(db=db, case_id=case_id)

    # 预览查询================================#
    url_list = ExtractParamsPath.get_url_path(
        extract_contents=extract_contents,
        my_data=case_data,
    )
    params_list = ExtractParamsPath.get_value_path(
        extract_contents=extract_contents,
        my_data=case_data,
        type_='params'
    )
    data_list = ExtractParamsPath.get_value_path(
        extract_contents=extract_contents,
        my_data=case_data,
        type_='data'
    )
    # 预览查询================================#
    RepData.rep_url(url_list=url_list, new_str=new_str, extract_contents=extract_contents)
    # 对比数据================================#
    RepData.rep_json(json_data=params_list, case_data=case_data, new_str=new_str, type_='params')
    # 对比数据================================#
    RepData.rep_json(json_data=data_list, case_data=case_data, new_str=new_str, type_='data')
    return await response_code.resp_200(
        data={
            'url_list': url_list,
            'params_list': params_list,
            'data_list': data_list,
        }
    )
