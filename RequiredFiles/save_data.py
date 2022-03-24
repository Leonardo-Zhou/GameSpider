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

    # 去重处理。获得所有已经下载过的url，判断是否有可能重复
    url_downloaded_list = []
    this_year_games = collections.find({"发售年份": year})
    for game in this_year_games:
        try:
            url_downloaded_list.append({'url':game['详细网页'],'下载地址':'下载地址' in game})
        except KeyError:
            pass

    spider = Spider(year)
    logger = spider.logger
    data = spider.start(url_downloaded_list)
    while True:
        try:

            # 获得start函数中yield的值
            temp = data.__next__()

            collections.insert_one(temp)

        except StopIteration:
            logger.info('{}年所有游戏下载完成'.format(year))
            break


def unit_conversion():
    client = MongoClient()
    db = client['games']
    collections = db['byrut.org']

    game_list = collections.find({"发售年份":2022})
    for game in game_list:
        try:
            size_temp = game['大小']
            if type(size_temp) == str:
                size_temp = size_temp.replace(',', '.')
                size = float(size_temp[:-2])
                unit = size_temp[-2:]
                if unit == 'MB':
                    size/=1024
                size = round(size,2)
                collections.update_one(game,{"$set": {"大小": size}})
        except KeyError:
            pass


if __name__ == '__main__':
    # main()
    unit_conversion()