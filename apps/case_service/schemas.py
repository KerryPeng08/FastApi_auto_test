#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: schemas.py
@Time: 2022/8/20-22:00
"""

from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Union
from enum import Enum


class ModeEnum(str, Enum):
    service = 'service'
    ddt = 'ddt'
    perf = 'perf'


# 用例名称的请求/响应数据模型
class TestCaseIn(BaseModel):
    case_name: str
    mode: ModeEnum

    class Config:
        orm_mode = True


class TestCaseOut(TestCaseIn):
    id: int
    case_count: int
    run_order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 测试用例的数据模型
class TestCaseConfig(BaseModel):
    is_login: bool = None
    sleep: float = 0.3
    stop: bool = None
    code: int = None
    extract: list = None


class TestCaseDataIn(BaseModel):
    number: Union[str, int]
    path: str
    headers: Optional[dict] = {}
    params: Optional[dict] = {}
    data: Optional[dict] = {}
    file: bool
    check: Optional[dict] = {}
    description: str
    config: TestCaseConfig

    class Config:
        orm_mode = True


class TestCaseData(BaseModel):
    number: Union[int, str]
    path: str
    headers: Optional[dict] = {}
    params: Optional[dict] = {}
    data: Optional[dict] = {}
    file: bool
    check: Optional[dict] = {}
    description: str
    config: TestCaseConfig

    class Config:
        orm_mode = True


class TestCaseDataOut(BaseModel):
    tips: dict
    temp_name: str = None
    case_name: str = None
    mode: ModeEnum
    data: List[TestCaseData]

    class Config:
        orm_mode = True


class TestCaseDataOut1(BaseModel):
    number: int
    case_id: int
    path: str
    headers: Optional[dict] = {}
    params: Optional[dict] = {}
    data: Optional[dict] = {}
    file: bool
    check: Optional[dict] = {}
    description: str
    config: TestCaseConfig

    class Config:
        orm_mode = True


class TestCaseDataOut2(BaseModel):
    number: int
    case_id: int
    path: str
    headers: Optional[dict] = {}
    params: Optional[dict] = {}
    data: Optional[dict] = {}
    file: bool
    check: Optional[dict] = {}
    description: str
    config: TestCaseConfig
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TestCaseInfoOut(BaseModel):
    name: str
    case_id: int
    api_count: int = None
    run_order: int = None
    mode: str = None
    created_at: datetime = None
