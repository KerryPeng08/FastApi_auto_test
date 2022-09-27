#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: router.py
@Time: 2022/8/3-16:40
"""

import uvicorn
from fastapi import FastAPI, Request
from setting import ALLURE_PATH
from apps.template.router import template
from apps.case_service.router import case_service
from apps.case_ddt.router import case_ddt
from apps.case_perf.router import case_perf
from apps.api_pool.router import pool
from apps.run_case.router import run_case
from tools.database import Base, engine
from tools.load_allure import load_allure_reports
from apps import response_code

Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url='/',
    include_in_=True,
    title='一个基于FastApi实现的纯后端 接口测试平台'
)


@app.get('/helpInfo', name='操作说明概要', tags=['Help'])
async def help_info():
    return await response_code.resp_200(data={
        'order': {
            '/template/upload/har': '上传Charles的Har文件-先解析-再写入',
            '/caseService/init/data/json': '下载预处理后的模板数据-Json',
            '/template/data/list': '查询模板接口原始数据',
            '/caseService/upload/json': '上传测试数据-Json',
            '/runCase/': '按用例执行',
        },
        'description': '将模板数据Json下载下来后，通常需要对照原始数据进行jsonPath表达式进行编辑，编辑完成即可上传Json'
    })


app.include_router(template, prefix='/template', tags=['测试场景'])
app.include_router(case_service, prefix='/caseService', tags=['业务接口测试用例'])
app.include_router(case_ddt, prefix='/caseDdt', tags=['数据驱动测试用例'])
app.include_router(case_perf, prefix='/casePerf', tags=['性能测试用例'])
app.include_router(run_case, prefix='/runCase', tags=['执行测试'])
app.include_router(pool, prefix='/YApi', tags=['YApi接口池'])


# 测试报告路径
@app.get('/allure', name='allure测试报告地址', tags=['测试报告'])
async def allure(request: Request):
    return await response_code.resp_200(data={'allure_report': f"{request.url}" + "/{case_id}/{run_order}"})


load_allure_reports(app=app, allure_dir=ALLURE_PATH)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
