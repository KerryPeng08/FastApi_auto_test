#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: my_pagination.py
@Time: 2023/3/31-13:56
"""

from __future__ import annotations
import math
from typing import TypeVar, Generic, Sequence

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from pydantic import BaseModel

T = TypeVar("T")


class Params(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(15, gt=0, le=100, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * (self.page - 1),
        )


class Page(AbstractPage[T], Generic[T]):
    items: Sequence[T]
    total: int
    page: int
    size: int
    next: str
    previous: str
    total_pages: int

    __params_type__ = Params  # Set params related to Page

    @classmethod
    def create(
            cls,
            items: items,
            total: int,
            params: Params,
    ) -> Page[T]:
        page = params.page
        size = params.size
        total_pages = math.ceil(total / params.size)
        next_ = f"?page={page + 1}&size={size}" if (page + 1) <= total_pages else ""
        previous = f"?page={page - 1}&size={size}" if (page - 1) >= 1 else ""

        return cls(items=items, total=total, page=params.page,
                   size=params.size,
                   next=next_,
                   previous=previous,
                   total_pages=total_pages)
