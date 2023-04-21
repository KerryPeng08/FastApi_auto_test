#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: run_case.py
@Time: 2022/9/28-17:15
"""

import copy
from aiohttp.client_exceptions import ServerTimeoutError, ServerConnectionError, ServerDisconnectedError, \
    ClientConnectorError
from sqlalchemy.orm import Session
from typing import List
from apps.case_service import crud as case_crud
from apps.template import crud as temp_crud
from apps.run_case.tool import RunApi, run
from apps.run_case import schemas
from tools.load_allure import load_allure_report
from apps import response_code
from setting import ALLURE_PATH, HOST
from apps.run_case.tool.header_host import whole_host


async def run_service_case(db: Session, case_ids: list, temp_hosts: List[schemas.TempHosts] = None):
    """
    执行业务流程用例
    :param db:
    :param case_ids:
    :temp_hosts:
    :return:
    """
    report = {}
    for case_id in case_ids:
        case_info = await case_crud.get_case_info(db=db, case_id=case_id)
        if case_info:
            # 拿到测试数据
            case_data = await case_crud.get_case_data(db=db, case_id=case_info[0].id)
            # 拿到模板数据
            temp_data = await temp_crud.get_template_data(db=db, temp_id=case_info[0].temp_id)
            temp_data = await whole_host(temp_data=copy.deepcopy(temp_data), temp_hosts=temp_hosts)
            # 拿到项目名称、模板名称
            temp_info = await temp_crud.get_temp_name(db=db, temp_id=case_info[0].temp_id)
            # 处理数据，执行用例
            try:
                case, run_order, is_fail = await RunApi().fo_service(
                    db=db,
                    case_id=case_id,
                    temp_data=temp_data,
                    case_data=case_data,
                    temp_pro=temp_info[0].project_name,
                    temp_name=temp_info[0].temp_name
                )
            except (ServerTimeoutError, ServerConnectionError, ServerDisconnectedError, ClientConnectorError) as e:
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
            await load_allure_report(allure_dir=allure_dir, case_id=case_id, run_order=run_order)

            # report[case_id] = f'{HOST}allure/{case_id}/{run_order}'
            report[case_id] = {
                'report': f'/allure/{case_id}/{run_order}',
                'is_fail': is_fail,
                'run_order': run_order
            }
        else:
            report[case_id] = {
                'report': f'用例{case_id}不存在',
                'is_fail': True,
                'run_order': 0
            }

    return report


async def run_ddt_case(db: Session, case_id: int, case_info: list):
    """
    执行数据驱动用例
    :param db:
    :param case_id:
    :param case_info:
    :return:
    """
    report = {}
    for case_data in case_info:
        case_info = await case_crud.get_case_info(db=db, case_id=case_id)
        # 拿到模板数据
        temp_data = await temp_crud.get_template_data(db=db, temp_id=case_info[0].temp_id)
        # 拿到项目名称、模板名称
        temp_info = await temp_crud.get_temp_name(db=db, temp_id=case_info[0].temp_id)
        # 处理数据，执行用例
        try:
            case, run_order, is_fail = await RunApi().fo_service(
                db=db,
                case_id=case_id,
                temp_data=temp_data,
                case_data=case_data,
                temp_pro=temp_info[0].project_name,
                temp_name=temp_info[0].temp_name
            )
        except (ServerTimeoutError, ServerConnectionError, ServerDisconnectedError, ClientConnectorError) as e:
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
        await load_allure_report(allure_dir=allure_dir, case_id=case_id, run_order=run_order)

        # report[case_id] = f'{HOST}allure/{case_id}/{run_order}'
        report[case_id] = {
            'report': f'/allure/{case_id}/{run_order}',
            'is_fail': is_fail,
            'run_order': run_order
        }

    return report
