#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: schemas.py
@Time: 2022/8/9-16:07
"""

from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional


class YApiInfo(BaseModel):
    """
    YApi登录信息
    """
    url: HttpUrl = Field(..., description='YApi登录接口')
    email: EmailStr = Field(..., description='登录邮箱')
    password: str = Field(..., max_length=50, description='登录密码')


class SwaggerInfo(BaseModel):
    url: HttpUrl
    username: str
    password: str


class YApiInfoTask(BaseModel):
    yapi_info: YApiInfo
    message: str
    id: Optional[int] = None
