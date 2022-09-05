#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: load_allure.py
@Time: 2022/9/3-22:55
"""

import os
from .global_log import logger
from fastapi.staticfiles import StaticFiles


def load_allure_report(app, allure_dir: str):
    files = os.listdir(os.path.join(allure_dir, 'allure_plus'))
    # from main import app
    for file in files:
        if file == 'history.json':
            continue
        allure_url = f"/allure/{file}"
        allure_path = f'{allure_dir}/allure_plus/{file}'
        app.mount(allure_url, StaticFiles(directory=allure_path, html=True))
        logger.info(f"加载allure静态报告, url:{allure_url}, path:{allure_path}")
