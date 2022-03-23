# -*- coding: utf-8 -*-
"""
@File    : save_data.py
@Time    : 2022/3/21 22:36
@Author  : Leonardo Zhou
@Email   : 2974519865@qq.com
@Software: PyCharm
"""

from pymongo import MongoClient
from RequiredFiles.parse_page import Spider


def main(year=2021):
    client = MongoClient()
    db = client['games']
    collections = db['byrut.org']

    spider = Spider(year)
    logger = spider.logger
    data = spider.start()
    while True:
        try:
            temp = data.__next__()
            collections.insert_one(temp)
        except StopIteration:
            logger.info('{}年所有游戏下载完成'.format(year))
            break


if __name__ == '__main__':
    main()