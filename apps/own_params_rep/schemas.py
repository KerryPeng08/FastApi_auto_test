#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: schemas.py
@Time: 2023/2/25-21:07
"""

from pydantic import BaseModel
from typing import Optional, List, Union
from enum import Enum


class UrlEdit(BaseModel):
    temp_id: Optional[int] = None
    case_id: Optional[int] = None
    number: int
    rep_url: bool
    old_url: str
    new_url: str


class ParamsAdd(BaseModel):
    temp_id: Optional[int] = None
    case_id: Optional[int] = None
    number: int
    rep_params_add: bool
    key: str
    value: Optional[str] = None


class ParamsEdit(BaseModel):
    temp_id: Optional[int] = None
    case_id: Optional[int] = None
    number: int
    rep_params_edit: bool
    old_key: str
    new_key: str
    value: Optional[str] = None


class ParamsDel(BaseModel):
    temp_id: Optional[int] = None
    case_id: Optional[int] = None
    number: int
    rep_params_del: bool
    key: str


class DataAdd(BaseModel):
    temp_id: Optional[int] = None
    case_id: Optional[int] = None
    number: int
    rep_data_add: bool
    key: str
    value: Optional[str] = None


class DataEdit(BaseModel):
    temp_id: Optional[int] = None
    case_id: Optional[int] = None
    number: int
    rep_data_edit: bool
    old_key: str
    new_key: str
    value: Optional[str] = None


class DataDel(BaseModel):
    temp_id: Optional[int] = None
    case_id: Optional[int] = None
    number: int
    rep_data_del: bool
    key: str
