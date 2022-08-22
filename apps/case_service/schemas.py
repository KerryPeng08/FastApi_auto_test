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
from enum import Enum


class ModeEnum(str, Enum):
    service = 'service'
    ddt = 'ddt'
    perf = 'perf'


# 用例名称的请求/响应数据模型
class TestCaseIn(BaseModel):
    case_name: str
    mode: ModeEnum


class TestCaseOut(TestCaseIn):
    id: int
    case_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 测试用例的数据模型
class TestCaseConfig(BaseModel):
    is_login: bool = None
    sleep: float = 0.3


class TestCaseDataIn(BaseModel):
    headers: Optional[dict] = {}
    params: Optional[dict] = {}
    data: Optional[dict] = {}
    check: Optional[dict] = {}
    description: str
    config: TestCaseConfig

    class Config:
        orm_mode = True


class TestCaseData(BaseModel):
    number: str
    path: str
    headers: Optional[dict] = {}
    params: Optional[dict] = {}
    data: Optional[dict] = {}
    check: Optional[dict] = {}
    description: str
    config: TestCaseConfig

    class Config:
        orm_mode = True


class TestCaseDataOut(BaseModel):
    tips: list
    temp_name: str
    mode: ModeEnum
    data: List[TestCaseData]

    class Config:
        orm_mode = True
