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

    def __init__(self):
        self._faker = Faker(locale='zh_CN')

    def name(self) -> str:
        return self._faker.name_female()

    def ssn(self, min_age: int = 18, max_age: int = 50) -> int:
        return self._faker.ssn(min_age=min_age, max_age=max_age)

    def phone_number(self) -> int:
        return self._faker.phone_number()

    def credit_card_number(self) -> int:
        return self._faker.credit_card_number()

    def city(self) -> str:
        return self._faker.city()

    def address(self) -> str:
        return self._faker.address()[:-7]

    @staticmethod
    def random_int(length: int) -> int:
        i = [str(x) for x in range(9)]
        return int(''.join(random.sample(i, length)))

    @staticmethod
    def time_int(day: int) -> int:
        now_time = int(time.time())
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

    def time_str(self, day: int) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.time_int(day=int(day)) // 1000))


if __name__ == '__main__':
    f = FakerData()
    print(f.name())
    print(f.ssn())
    print(f.phone_number())
    print(f.credit_card_number())
    print(f.city())
    print(f.address())
    print(f.time_int(1))
    print(f.time_str(1))
    print(f.random_int(4))
