#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: case_data_gather.py
@Time: 2023/3/6-14:46
"""

import openpyxl
from openpyxl.styles import Alignment


class CaseDataGather:

    def data_gather(self, case_data, path: str):
        """
        处理测试数据集的内容
        :param case_data:
        :param path:
        :return:
        """
        # 处理需要做数据集的参数
        case_gather = []
        for data in case_data:
            # params的参数数据
            params = self._header_data(data.params)
            # data的参数数据
            data_ = self._header_data(data.data)
            # check的数据
            check = self._header_data(data.check)
            if params or data_:
                case_gather.append({
                    'url': f"{data.number}#{data.path}",
                    'params': params,
                    'data': data_,
                    'check': check

                })
        # 输出表格
        self._excel(path=path, case_gather=case_gather)

    @staticmethod
    def _excel(path: str, case_gather: list):
        """
        输出excel
        :param case_gather:
        :return:
        """
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        align = Alignment(horizontal='center', vertical='center')
        start_column = 2
        end_column = 0
        for data in case_gather:
            params_len = len(data['params'])
            data_len = len(data['data'])
            check_len = len(data['check'])
            url_len = params_len + data_len + check_len

            end_column += url_len
            # 合并url的行
            sheet.merge_cells(
                start_row=1,
                end_row=1,
                start_column=start_column,
                end_column=end_column + 1
            )
            sheet.cell(1, start_column).value = data['url']
            sheet.cell(1, start_column).alignment = align
            sheet.cell(1, 1).value = 'URL'
            sheet.cell(1, 1).alignment = align
            # 合并params、data、check的行
            if data['params']:
                sheet.merge_cells(
                    start_row=2,
                    end_row=2,
                    start_column=start_column,
                    end_column=end_column + 1 - (data_len + check_len)
                )
                sheet.cell(2, start_column).value = 'params'
                sheet.cell(2, start_column).alignment = align
                sheet.cell(2, 1).value = '分类'
                sheet.cell(2, 1).alignment = align
                for x in range(len(data['params'])):
                    sheet.cell(3, start_column + x).value = list(data['params'].keys())[x]
                    sheet.cell(3, start_column + x).alignment = align
                    sheet.cell(4, start_column + x).value = list(data['params'].values())[x]
                    sheet.cell(4, start_column + x).alignment = align
            if data['data']:
                sheet.merge_cells(
                    start_row=2,
                    end_row=2,
                    start_column=start_column + params_len,
                    end_column=end_column + 1 - check_len
                )
                sheet.cell(2, start_column + params_len).value = 'data'
                sheet.cell(2, start_column + params_len).alignment = align
                for x in range(len(data['data'])):
                    sheet.cell(3, start_column + params_len + x).value = list(data['data'].keys())[x]
                    sheet.cell(3, start_column + params_len + x).alignment = align
                    sheet.cell(4, start_column + params_len + x).value = list(data['data'].values())[x]
                    sheet.cell(4, start_column + params_len + x).alignment = align

            if data['check']:
                sheet.merge_cells(
                    start_row=2,
                    end_row=2,
                    start_column=start_column + params_len + data_len,
                    end_column=end_column + 1
                )
                sheet.cell(2, start_column + params_len + data_len).value = 'check'
                sheet.cell(2, start_column + params_len + data_len).alignment = align
                sheet.cell(3, 1).value = '参数'
                sheet.cell(3, 1).alignment = align
                sheet.cell(4, 1).value = '原始数据'
                sheet.cell(4, 1).alignment = align
                for x in range(len(data['check'])):
                    sheet.cell(3, start_column + params_len + data_len + x).value = list(data['check'].keys())[x]
                    sheet.cell(3, start_column + params_len + data_len + x).alignment = align
                    sheet.cell(4, start_column + params_len + data_len + x).value = list(data['check'].values())[x]
                    sheet.cell(4, start_column + params_len + data_len + x).alignment = align

            start_column += url_len

        workbook.save(path)

    @staticmethod
    def _header_data(data_json: dict):
        """
        处理数据
        :param data_json:
        :return:
        """
        target = {}

        def inter_of(data):
            for k, v in data.items():
                if not isinstance(v, (list, dict)):
                    if '{' not in str(v) and '}' not in str(v):
                        target[k] = v
                    continue
                if isinstance(v, dict):
                    target[k] = inter_of(v)
                    continue
                if isinstance(v, list):
                    # new_list = []
                    for x in v:
                        inter_of(x)
                    # target[k] = new_list
                    continue
            return target

        return inter_of(data_json)
