#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: schemas.py
@Time: 2022/8/23-13:56
"""

from typing import List, Optional
from pydantic import BaseModel


class RunCaseGather(BaseModel):
    case_id: int
    suite: List[int]
    async_: Optional[bool] = False
