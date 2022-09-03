#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: response_code.py
@Time: 2022/8/26-11:27
"""

from fastapi import status
from fastapi.responses import JSONResponse, Response  # , ORJSONResponse,UJSONResponse
from typing import Union


async def resp_200(*, data: Union[list, dict, str, int, float] = '', message: str = 'Success') -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 0,
            'message': message,
            'data': data,
        }
    )


async def resp_400(*, data: str = '', message: str = "操作失败") -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'code': 1,
            'message': message,
            'data': data,
        }
    )


async def resp_404(*, data: str = '', message: str = "未获取到内容") -> Response:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            'code': 1,
            'message': message,
            'data': data,
        }
    )
