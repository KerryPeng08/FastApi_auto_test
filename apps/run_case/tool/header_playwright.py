#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: header_playwright.py
@Time: 2023/6/25-20:18
"""

from setting import SELENOID
from tools import get_session_id
from urllib3 import exceptions

BROWSER_TEMP: str = f"""
    browser = playwright.chromium.connect_over_cdp(
        endpoint_url='ws://{SELENOID['host']}/ws/devtools/driver.session_id'
    )
"""


async def replace_playwright(
        playwright_text: str,
        temp_name: str,
        remote: bool,
        remote_id: int
):
    """
    替换文本内容
    :param playwright_text:
    :param temp_name:
    :param remote: 是否使用远程浏览器
    :param remote_id:
    :return:
    """

    new_text = playwright_text.replace(
        '{{case_name}}', temp_name
    ).replace(
        '{{', ''
    ).replace(
        '}}', ''
    )
    if remote and remote_id:
        se = SELENOID['browsers'][remote_id - 1]
        try:
            session_id = await get_session_id(browser_name=se['browser_name'], browser_version=se['browser_name'])
        except exceptions.MaxRetryError:
            return ''
        browser_temp = BROWSER_TEMP.replace('driver.session_id', str(session_id))
        new_text = playwright_text.replace(
            'browser = playwright.chromium.launch(headless=False)',
            browser_temp
        )

    return new_text
