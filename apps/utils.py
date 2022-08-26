#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: utils.py
@Time: 2022/8/26-11:27
"""

from fastapi import status
from fastapi.responses import JSONResponse, Response  # , ORJSONResponse,UJSONResponse
from typing import Union
from pydantic import BaseModel


async def resp_200(*, data: Union[list, dict, str, BaseModel]) -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 0,
            'message': "Success",
            'data': data,
        }
    )


async def resp_400(*, data: str = None, message: str = "BAD REQUEST") -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'code': 1,
            'message': message,
            'data': data,
        }
    )


async def resp_404(*, data: str = None, message: str = "未获取到内容") -> Response:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            'code': 1,
            'message': message,
            'data': data,
        }
    )
