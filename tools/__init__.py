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
from .global_log import logger
from .aiohttp_get_cookie import get_cookie
import os
import pathlib
from setting import ALLURE_PATH
from fastapi.staticfiles import StaticFiles
from tools.database import Base, engine

Base.metadata.create_all(bind=engine)


def load_allure_report():
    files = os.listdir(os.path.join(ALLURE_PATH, 'allure_plus'))
    from main import app
    for file in files:
        if file == 'history.json':
            continue
        app.mount(f"/allure/{file}", StaticFiles(directory=f'{ALLURE_PATH}/allure_plus/{file}', html=True))


def mkdir():
    """
    按项目创建多级目录
    :return:
    """
    pathlib.Path(f"{ALLURE_PATH}/allure_plus/1").mkdir(parents=True, exist_ok=True)
    pathlib.Path(f'./files/excel').mkdir(parents=True, exist_ok=True)
    pathlib.Path(f'./files/json').mkdir(parents=True, exist_ok=True)


mkdir()
