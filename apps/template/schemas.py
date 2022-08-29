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
from enum import Enum


class TempEnum(str, Enum):
    sales = 'sales'
    oms = 'oms'
    site = 'site'
    tms = 'tms'
    wxapp = 'wxapp'


# 模板名称的请求/响应数据模型
class TemplateIn(BaseModel):
    temp_name: str
    project_name: TempEnum


class TemplateOut(TemplateIn):
    id: int
    api_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TestCase(BaseModel):
    id: int
    mode: str
    name: str
    run_num: int


class TempTestCase(TemplateOut):
    case_count: int
    case_info: List[TestCase]


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
