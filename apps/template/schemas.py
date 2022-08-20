#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: schemas.py
@Time: 2022/8/9-16:03
"""

from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import Optional, List


# 模板名称的请求/响应数据模型
class TemplateIn(BaseModel):
    temp_name: str


class TemplateOut(TemplateIn):
    id: int
    api_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 测试模板数据的请求/响应数据模型
class TemplateDataIn(BaseModel):
    host: HttpUrl
    path: str
    code: int
    method: str
    params: Optional[dict] = {}
    json_body: str
    data: Optional[dict] = {}
    headers: Optional[dict] = {}
    response: Optional[dict] = {}


class TemplateDataOut(TemplateDataIn):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True



