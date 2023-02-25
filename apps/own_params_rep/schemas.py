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
