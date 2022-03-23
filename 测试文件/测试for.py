# -*- coding: utf-8 -*-
"""
@File    : 测试for.py
@Time    : 2022/3/21 16:08
@Author  : Leonardo Zhou
@Email   : 2974519865@qq.com
@Software: PyCharm
"""
from pymongo import MongoClient
import time
collections = MongoClient()['test']['test']
# a = [{}]
# for i in range(10):
#     a[i]['aa'] = 'ab'
# print(a)


def a(n):
    for i in range(n):
        try:
            # if i == 6:
                # time.sleep(10000)

            yield {'{}'.format(i):i}
        except TypeError:
            pass


# collections.insert_one({})
b = a(10)

while 1:
    collections.insert_one(b.__next__())