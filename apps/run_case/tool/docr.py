#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: docr.py
@Time: 2022/10/27-15:38
"""

import ddddocr
import requests

from tools.global_log import logger


async def ocr_code(url: str, data: dict = None):
    """
    使用第三方库识别验证码
    :param url:
    :param data:
    :return:
    """
    try:
        res = requests.get(url=url, params=data)
    except Exception as e:
        logger.error(f'验证码获取错误: {e}')
    else:
        ocr = ddddocr.DdddOcr(show_ad=False)
        code = ocr.classification(res.content)
        logger.info(f'验证码获取成功: {code}')
        return code
