#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: schemas.py
@Time: 2022/8/9-16:03
"""

from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Union
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
    project_name: TempEnum = None

    class Config:
        orm_mode = True


class TemplateOut(TemplateIn):
    id: int = None
    api_count: int = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class TestCase(BaseModel):
    id: int
    mode: str = None
    name: str
    run_num: int = None

    class Config:
        orm_mode = True


class TempTestCase(TemplateOut):
    case_count: int = None
    case_info: List[TestCase]

    class Config:
        orm_mode = True


# 测试模板数据的请求/响应数据模型
class TemplateDataIn(BaseModel):
    number: Union[str, int]
    host: HttpUrl
    path: str
    code: int
    method: str
    params: Optional[dict] = {}
    json_body: str
    data: Optional[dict] = {}
    file: bool
    file_data: Optional[list] = []
    headers: Optional[dict] = {}
    response: Union[dict, list, str] = None

    class Config:
        orm_mode = True


class TemplateDataInTwo(BaseModel):
    temp_id: int
    number: Union[int, str]
    host: HttpUrl
    path: str
    code: int
    method: str
    params: Optional[dict] = {}
    json_body: str
    data: Optional[dict] = {}
    file: bool
    file_data: Optional[list] = []
    headers: Optional[dict] = {}
    response: Union[dict, list, str] = None


class TemplateDataOut(TemplateDataIn):
    id: int
    temp_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TempChangeParams(BaseModel):
    temp_id: int
    temp_name: str
    number: int
    path: str
    params: dict
    data: dict


class SwapDataOne(BaseModel):
    temp_id: int
    old_number: int
    new_number: int


class SwapDataMany(BaseModel):
    temp_id: int
    new_numbers: List[int]


class UpdateName(BaseModel):
    new_name: str
    temp_id: int = None
