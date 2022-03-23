# -*- coding: utf-8 -*-
"""
@File    : 加入year.py
@Time    : 2022/3/22 15:28
@Author  : Leonardo Zhou
@Email   : 2974519865@qq.com
@Software: PyCharm
"""

from pymongo import MongoClient

collections = MongoClient()['games']['byrut.org']

for record in collections.find()[1:]:
    temp = record
    collections.update_one(record,{'$set':{'发售年份':2021}})

