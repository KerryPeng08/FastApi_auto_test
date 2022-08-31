#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: aiohttp_get_cookie.py
@Time: 2022/8/29-12:55
"""

import re


async def get_cookie(response) -> str:
    """
    获取cookie数据
    :param response:
    :return:
    """
    cookie = ''
    for k, v in response.cookies.items():
        cookie += f"{k}={re.compile(r'=(.*?); ', re.S).findall(str(v))[0]}; "
    return cookie
