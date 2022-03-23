# -*- coding: utf-8 -*-
"""
@File    : 测试yield.py
@Time    : 2022/3/20 23:10
@Author  : Leonardo Zhou
@Email   : 2974519865@qq.com
@Software: PyCharm
"""



def ceshi(c):
    print(1)
    b = [1]
    yield b
    if c < 5:
        b.append(ceshi(c+1))
    else:
        pass


if __name__ == '__main__':
    a = ceshi(10)