#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: my_selenoid.py
@Time: 2023/6/25-20:02
"""

from setting import SELENOID
from selenium import webdriver


async def get_session_id(browser_name: str, browser_version: str):
    """
    获取远程浏览器的session_id
    :param browser_name: 浏览器名称
    :param browser_version: 浏览器版本
    :return:
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.set_capability("browserName", browser_name)
    chrome_options.set_capability("browserVersion", browser_version)
    chrome_options.set_capability("selenoid:options", {"enableVNC": True, "enableVideo": True})

    driver = webdriver.Remote(
        command_executor=f"http://{SELENOID['host']}/wd/hub",
        options=chrome_options
    )

    return driver.session_id
