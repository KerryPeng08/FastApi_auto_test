#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: run_case.py
@Time: 2022/9/28-17:15
"""

# from aiohttp.client import ServerDisconnectedError, ServerConnectionError
from requests.exceptions import ConnectionError
from fastapi import Request
from sqlalchemy.orm import Session
from apps.case_service import crud as case_crud
from apps.template import crud as temp_crud
from apps.run_case.tool import RunApi, run
from tools.load_allure import load_allure_report
from apps import response_code
from setting import ALLURE_PATH, HOST


async def run_service_case(db: Session, request: Request, case_ids: list):
    report = []
    for case_id in case_ids:
        case_info = await case_crud.get_case_name(db=db, case_id=case_id)
        if case_info:
            # 拿到测试数据
            case_data = await case_crud.get_case_data(db=db, case_id=case_info[0].id)
            # 拿到模板数据
            temp_data = await temp_crud.get_template_data(db=db, temp_id=case_info[0].temp_id)
            # 拿到项目名称、模板名称
            temp_info = await temp_crud.get_temp_name(db=db, temp_id=case_info[0].temp_id)
            # 处理数据，执行用例
            try:
                case, run_order = await RunApi().fo_service(
                    db=db,
                    case_id=case_id,
                    temp_data=temp_data,
                    case_data=case_data,
                    temp_pro=temp_info[0].project_name,
                    temp_name=temp_info[0].temp_name
                )
            # except (ServerDisconnectedError, ServerConnectionError) as e:
            except (ConnectionError,) as e:
                return await response_code.resp_400(message=f'网络访问失败: {str(e)}')

            except IndexError as e:
                return await response_code.resp_400(message=f': {str(e)}')

            # 校验结果，生成报告
            allure_dir = ALLURE_PATH
            await run(
                test_path='./apps/run_case/test_case/test_service.py',
                allure_dir=allure_dir,
                report_url=HOST,
                case_name=case,
                case_id=case_id
            )
            load_allure_report(allure_dir=allure_dir, case_id=case_id, run_order=run_order)

            report.append(f'{HOST}allure/{case_id}/{run_order}')
        else:
            report.append(f'用例{case_id}不存在')

    return await response_code.resp_200(data={'allure_report': report})
