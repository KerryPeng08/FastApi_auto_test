#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: models.py
@Time: 2022/8/20-21:59
"""

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, JSON, Boolean
from tool.database import Base


class TestCase(Base):
    """
    用例名称表
    """
    __tablename__ = 'test_case'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    temp_id = Column(Integer, ForeignKey('case_template.id'))
    case_name = Column(String, unique=True, nullable=True, index=True, comment='用例名称')
    case_count = Column(Integer, default=0, nullable=True, comment='用例数量')

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    __mapper_args__ = {'order_by': id.desc()}


class TestCaseData(Base):
    """
    用例数据表
    """
    __tablename__ = 'test_case_data'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey('test_case.id'))
    is_login = Column(Boolean, default=None, comment='登录接口')
    headers = Column(JSON, comment='请求头测试数据')
    params = Column(JSON, comment='请求参数测试数据')
    data = Column(JSON, comment='json/表单 测试数据')
    check = Column(JSON, comment='测试数据校验字段')

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    __mapper_args__ = {'order_by': id}
