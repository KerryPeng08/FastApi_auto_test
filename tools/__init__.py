#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: __init__.py.py
@Time: 2022/8/11-16:40
"""

import pathlib
from .excel import CreateExcel, ReadExcel
from .operation_json import OperationJson
from .global_log import logger
from .aiohttp_get_cookie import get_cookie
from .my_sql import AsyncMySql
from .get_value_path import ExtractParamsPath, RepData
from .rep_case_data_value import rep_value, rep_url


def mkdir():
    """
    按项目创建多级目录
    :return:
    """
    # pathlib.Path(f"{ALLURE_PATH}/allure_plus/1/1").mkdir(parents=True, exist_ok=True)
    pathlib.Path(f'./files/excel').mkdir(parents=True, exist_ok=True)
    pathlib.Path(f'./files/json').mkdir(parents=True, exist_ok=True)
    pathlib.Path(f'./files/code').mkdir(parents=True, exist_ok=True)


mkdir()
