#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: run_case.py
@Time: 2022/8/23-22:14
"""

import os


async def run(test_path: str, report_path: str, allure_path: str):
    """
    执行测试用例
    :param test_path: test_*.py测试文件路径
    :param report_path: json文件路径
    :param allure_path: allure文件路径
    :return:
    """
    os.system(f"pytest -s --tb=short --durations=0 --alluredir={report_path} {test_path}")
    os.system(f"allure generate {report_path} -o {allure_path} --clean")
