#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: schemas.py
@Time: 2022/8/20-22:00
"""

from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


# 用例名称的请求/响应数据模型
class TestCaseIn(BaseModel):
    case_name: str


class TestCaseOut(TestCaseIn):
    id: int
    case_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 测试用例的数据模型
class TestCaseDataIn(BaseModel):
    headers: Optional[dict] = {}
    params: Optional[dict] = {}
    data: Optional[dict] = {}
    check: Optional[dict] = {}


class TestCaseDataOut(BaseModel):
    number: str
    path: str
    is_login: bool = None
    headers: Optional[dict] = {}
    params: Optional[dict] = {}
    data: Optional[dict] = {}
    check: Optional[dict] = {}

    class Config:
        orm_mode = True


class ReadTemplate(BaseModel):
    description: list
    temp_name: str
    data: List[TestCaseDataOut]
