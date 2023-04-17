#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: models.py
@Time: 2023/4/16-14:42
"""

from sqlalchemy import Column, Integer, JSON, DateTime, func
from tools.database import Base


class WholeConfInfo(Base):
    """
    全局配置
    """
    __tablename__ = 'whole_conf_info'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    host = Column(JSON, comment='域名')
    project = Column(JSON, comment='项目名称')
    unify_res = Column(JSON, comment='统一响应')
    db_conf = Column(JSON, comment='数据库配置')

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
