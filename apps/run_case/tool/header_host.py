#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: header_host.py
@Time: 2023/4/21-12:27
"""

import re
from typing import List
from apps.template import schemas as temp_schemas
from apps.run_case import schemas


async def whole_host(temp_data: List[temp_schemas.TemplateDataOut], temp_hosts: List[schemas.TempHosts]):
    """
    处理模板中的host，替换掉全局配置中选择的host
    :param temp_data:
    :param temp_hosts:
    :return:
    """
    if not temp_hosts:
        return

    for temp in temp_data:
        for host in temp_hosts:
            if host.change and temp.host == host.temp_host:
                temp.host = host.whole_host

                for k, v in temp.headers.items():
                    if k == 'Host' or k == 'host':
                        if 'http://' in host.whole_host:
                            host_ = re.findall(r"http://(.*?)/", host.whole_host + '/')
                        else:
                            host_ = re.findall(r"https://(.*?)/", host.whole_host + '/')
                        temp.headers[k] = host_[0]

                    if host.temp_host in v:
                        temp.headers[k] = temp.headers[k].replace(host.temp_host, host.whole_host)

                break

    return temp_data
