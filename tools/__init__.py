#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: __init__.py.py
@Time: 2022/8/11-16:40
"""

from .excel import CreateExcel
from .operation_json import OperationJson
from .generate_case import GenerateCase
# from .check_case_json import CheckJson

from typing import List
import pathlib
from setting import PROJECT_NAME, ALLURE_PATH


def mkdir(pro_names: List[str]):
    """
    按项目创建多级目录
    :param pro_names:
    :return:
    """
    for name in pro_names:
        pathlib.Path(f'{ALLURE_PATH}{name.lower()}/report').mkdir(parents=True, exist_ok=True)
        pathlib.Path(f'{ALLURE_PATH}{name.lower()}/allure').mkdir(parents=True, exist_ok=True)

    pathlib.Path(f'./files/excel').mkdir(parents=True, exist_ok=True)
    pathlib.Path(f'./files/json').mkdir(parents=True, exist_ok=True)
    pathlib.Path(f'./files/run_case').mkdir(parents=True, exist_ok=True)


mkdir(PROJECT_NAME)
