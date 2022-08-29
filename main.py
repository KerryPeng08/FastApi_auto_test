#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/3-16:40
"""

import os
import uvicorn
from fastapi import FastAPI, Request
from apps.template import template
from apps.case_service import case_service
from apps.case_ddt import case_ddt
from apps.case_perf import case_perf
from apps.run_case import run_case
from tools.database import Base, engine
from tools import load_allure_report

Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url='/',
    include_in_=True,
    title='一个基于FastApi实现的纯后端 接口测试平台'
)

app.include_router(template, prefix='/template', tags=['测试场景'])
app.include_router(case_service, prefix='/caseService', tags=['业务接口测试用例'])
app.include_router(case_ddt, prefix='/caseDdt', tags=['数据驱动测试用例'])
app.include_router(case_perf, prefix='/casePerf', tags=['性能测试用例'])
app.include_router(run_case, prefix='/runCase', tags=['执行测试用例'])


# 测试报告路径
@app.get('/allure', name='allure测试报告地址', tags=['测试报告'])
async def allure(request: Request):
    return {'allure_report': f"{request.url}/allure/*"}


load_allure_report()

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, debug=True)
