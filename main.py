#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/3-16:40
"""

import uvicorn
from fastapi import FastAPI

# from apps.api_pool import api_pool
from apps.template import template
from apps.case_service import case_service
from apps.case_ddt import case_ddt
from apps.case_perf import case_perf
from tool.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url='/',
    include_in_=True,
    title='一个基于FastApi实现的纯后端 接口测试平台'
)

# app.include_router(api_pool, prefix='/pool', tags=['获取接口数据[接口池]'])
app.include_router(template, prefix='/template', tags=['测试场景'])
app.include_router(case_service, prefix='/caseService', tags=['业务接口测试用例'])
app.include_router(case_ddt, prefix='/caseDdt', tags=['数据驱动测试用例'])
app.include_router(case_perf, prefix='/casePerf', tags=['性能测试用例'])
# app.include_router(diff_api_data, prefix='/diff', tags=['接口数据对比'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, debug=True)
    # uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, debug=True)
