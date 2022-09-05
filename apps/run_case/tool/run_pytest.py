#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: run_pytest.py
@Time: 2022/8/23-22:14
"""

import os
import json
import time
import pathlib


async def run(test_path: str, allure_dir: str, report_url, case_name: str, case_id: int):
    """
    执行测试用例
    :param test_path: test_*.py测试文件路径
    :param allure_dir: allure 报告路径
    :param report_url: 报告路由
    :param case_name: 用例名称
    :param case_id: 用例id
    :return:
    """
    allure_plus_dir = os.path.join(allure_dir, str(case_id), 'allure_plus')
    pathlib.Path(allure_plus_dir).mkdir(parents=True, exist_ok=True)
    allure_path = os.path.join(allure_dir, str(case_id), 'allure', str(int(time.time())))
    command = f'pytest {test_path} -s  --alluredir={allure_path}'
    os.system(command)
    # 先调用get_dirname()，获取到这次需要构建的次数
    build_order, old_data = get_dirname(allure_plus_dir)
    # 再执行命令行
    command = f"allure generate {allure_path} -o {os.path.join(allure_plus_dir, str(build_order))} --clean"
    os.system(command)
    # 执行完毕后再调用update_trend_data()
    update_trend_data(allure_plus_dir, build_order, old_data, report_url, case_name, case_id)


def get_dirname(allure_plus_dir):
    hostory_file = os.path.join(allure_plus_dir, "history.json")
    if os.path.exists(hostory_file):
        with open(hostory_file) as f:
            li = eval(f.read())
        # 根据构建次数进行排序，从大到小
        li.sort(key=lambda x: x['buildOrder'], reverse=True)
        # 返回下一次的构建次数，所以要在排序后的历史数据中的buildOrder+1
        return li[0]["buildOrder"] + 1, li
    else:
        # 首次进行生成报告，肯定会进到这一步，先创建history.json,然后返回构建次数1（代表首次）
        with open(hostory_file, "w") as f:
            f.write(json.dumps({}))
        return 1, None


def update_trend_data(allure_plus_dir: str, dirname: int, old_data: list, report_url: str, case_name: str,
                      case_id: int):
    """
    dirname：构建次数
    old_data：备份的数据
    update_trend_data(get_dirname())
    """
    widgets_dir = os.path.join(allure_plus_dir, f"{str(dirname)}/widgets")
    # 读取最新生成的history-trend.json数据
    with open(os.path.join(widgets_dir, "history-trend.json")) as f:
        data = f.read()

    new_data = eval(data)
    if old_data is not None:
        new_data[0]["buildOrder"] = old_data[0]["buildOrder"] + 1
    else:
        old_data = []
        new_data[0]["buildOrder"] = 1
    # 给最新生成的数据添加reportUrl key，reportUrl要根据自己的实际情况更改
    new_data[0]["reportUrl"] = f"{report_url}allure/{case_id}/{dirname}/index.html"
    new_data[0]["reportName"] = f"{case_name}"
    # 把最新的数据，插入到备份数据列表首位
    old_data.insert(0, new_data[0])
    # 把所有生成的报告中的history-trend.json都更新成新备份的数据old_data，这样的话，点击历史趋势图就可以实现新老报告切换
    for i in range(1, dirname + 1):
        with open(os.path.join(allure_plus_dir, f"{str(i)}/widgets/history-trend.json"), "w+") as f:
            f.write(json.dumps(old_data))
    # 把数据备份到history.json
    hostory_file = os.path.join(allure_plus_dir, "history.json")
    with open(hostory_file, "w+") as f:
        f.write(json.dumps(old_data))
    return old_data, new_data[0]["reportUrl"]
