#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: schemas.py
@Time: 2023/6/9-16:31
"""

from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Union


class PlaywrightIn(BaseModel):
    id: Optional[int]
    project_name: str
    temp_name: str
    text: str

    class Config:
        orm_mode = True


class PlaywrightOut(PlaywrightIn):
    id: int
    rows: int
    run_order: int
    created_at: datetime = None
    updated_at: datetime = None


class PlaywrightDataIn(BaseModel):
    temp_id: int
    case_name: str
    rows_data: Union[list, dict]

    class Config:
        orm_mode = True


class PlaywrightDataOut(PlaywrightDataIn):
    id: int
    created_at: datetime = None
    updated_at: datetime = None


class PaginationPlaywright(BaseModel):
    total: int
    page: int
    size: int
    items: List[PlaywrightOut]
