#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: setting.py
@Time: 2022/8/23-12:54
"""

# allure总目录
ALLURE_PATH = 'D:\\Works\\liweijia\\auto_report'

# host
HOST = 'http://172.16.100.95:8000/'

# YApi配置信息
YAPI_INFO = {
    'host': 'http://yapi.liweijia.com',
    'email': 'yangjie@liweijia.com',
    'password': 'liweijia666'
}

# TIPS
TIPS = {
    '1': '编写用例时，只需关注params/data/check',
    '2': 'headers接受键值对输入，有内容则在执行时添加/替换请求头内容',
    '3': 'is_login标记登录接口，标记后自动获取cookie进行替换',
    '4': {
        '请求参数提取': [
            '1.默认会按key-value完全匹配提取上级接口响应数据',
            "2.参数提取表达式'{{number.$.jsonPath表达式}}'",
            "3.假数据使用表达式'{function.int}'"
        ],
        '响应数据校验': [
            '1.key为要校验的字段，value为校验的值',
            '2.若value数据类型为: string/integer/float/bool/dict, 按 == 直接进行校验',
            '3.若value数据类型为: list, 索引0应填写比较符: <,<=,==,!=,>=,>,in,not in; 索引1填写比较的值'
        ]
    },
    '5': 'description: 单接口用例描述信息',
    '6': 'mode: 运行模式, 支持: service/ddt/perf',
    '7': 'config: 单接口的配置信息',
    '8': {'假数据工具-function': {
        'name': '名称',
        'ssn': '身份证',
        'phone_number': '电话',
        'credit_card_number': '银行卡',
        'city': '城市',
        'address': '地址',
        'random_int': {
            ':param 1': '长度为1的随机数字',
            ':param 5': '长度为5的随机数字'
        },
        'time_int': {
            ':param 0': '当前时间',
            ':param -1': '当前时间前一天',
            ':param 1': '当前时间后一天',
            ':param -2': '前一天00:00:00',
            ':param 2': '后一天23:59:59',
        },
        'time_str': '时间字符串, 同上',
    }}
}
