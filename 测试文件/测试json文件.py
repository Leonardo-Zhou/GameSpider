# -*- coding: utf-8 -*-
"""
@File    : 测试json文件.py
@Time    : 2022/3/22 12:30
@Author  : Leonardo Zhou
@Email   : 2974519865@qq.com
@Software: PyCharm
"""
import json
with open('a.json','r') as file:
    b = json.load(file)

print(b)
if b:
    print(1)
else:
    print(2)