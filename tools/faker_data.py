#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: Kobayasi
@File: faker_data.py
@Time: 2022/9/5-17:32
"""

import time
import random
from faker import Faker


class FakerData:

    def __init__(self, *_):
        self._faker = Faker(locale='zh_CN')

    def _name(self, *_) -> str:
        return self._faker.name_female()

    def _ssn(self, *_) -> int:
        return self._faker.ssn(min_age=18, max_age=50)

    def _phone_number(self, *_) -> int:
        return self._faker.phone_number()

    def _credit_card_number(self, *_) -> int:
        return self._faker.credit_card_number()

    def _city(self, *_) -> str:
        return self._faker.city()

    def _address(self, *_) -> str:
        return self._faker.address()[:-7]

    @staticmethod
    def _random_int(*args) -> int:
        length = args[0] if args[0] <= 20 else 20
        i = [str(x) for x in range(9)]
        return int(''.join(random.sample(i, length)))

    @staticmethod
    def _time_int(*args) -> int:
        now_time = int(time.time())
        day = args[0]
        if day == 0:
            return now_time * 1000

        if day == -1:
            return (now_time - 86400) * 1000

        if day == 1:
            return (now_time + 86400) * 1000

        if day == -2:
            return int(time.mktime(
                time.strptime(time.strftime('%Y-%m-%d', time.localtime(now_time - 86400)), '%Y-%m-%d'))) * 1000

        if day == 2:
            return int(time.mktime(
                time.strptime(time.strftime('%Y-%m-%d', time.localtime(now_time + 86400)), '%Y-%m-%d')) + 86399) * 1000

        return now_time * 1000

    def _time_str(self, *args) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self._time_int(args) // 1000))

    def faker_data(self, func: str, param: int) -> (str, int, None):
        """
        :param func:
        :param param:
        :return:
        """
        func_dict = {
            'name': self._name,
            'ssn': self._ssn,
            'phone_number': self._phone_number,
            'credit_card_number': self._credit_card_number,
            'city': self._city,
            'address': self._address,
            'random_int': self._random_int,
            'time_int': self._time_int,
            'time_str': self._time_str,
        }
        if func_dict.get(func):
            return func_dict[func](param)
