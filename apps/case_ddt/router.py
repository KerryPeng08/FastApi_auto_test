#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/22-9:51
"""

from fastapi import APIRouter

case_ddt = APIRouter()


@case_ddt.get('/demo', name='开发中')
async def mode():
    pass
