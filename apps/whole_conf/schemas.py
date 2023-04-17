#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: schemas.py
@Time: 2023/4/16-14:42
"""

from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import Union, List


class HostConf(BaseModel):
    key: str
    value: HttpUrl


class WholeConfIn(BaseModel):
    host: Union[List[HostConf]] = []
    project: Union[List[str]] = []
    unify_res: Union[dict] = {}
    db_conf: Union[dict] = {}

    class Config:
        orm_mode = True


class WholeConfOut(WholeConfIn):
    created_at: datetime = None
    updated_at: datetime = None
