#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: schemas.py
@Time: 2022/8/23-13:56
"""

from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class TempHosts(BaseModel):
    temp_host: HttpUrl
    whole_host: HttpUrl
    change: bool


class RunCase(BaseModel):
    case_ids: List[int]
    temp_hosts: List[TempHosts]


class RunCaseGather(BaseModel):
    case_id: int
    suite: List[int]
    async_: Optional[bool] = False
