# -*- coding: utf-8 -*-
"""
@File    : parse_page.py
@Time    : 2022/3/20 19:43
@Author  : Leonardo Zhou
@Email   : 2974519865@qq.com
@Software: PyCharm
"""

from RequiredFiles.USER_AGENT import get_ua
import requests
import json
from lxml import etree
import random
import time
from RequiredFiles.logger import Logger
from RequiredFiles.Russian2Chinese import rus2chiDict


class Spider:
    def __init__(self, year=2021):
        self.init_url = 'https://byrut.org/games-{}-years/page/{}/'
        self.headers = get_ua()
        self.year = year
        self.session = requests.Session()
        self.session.headers = self.headers
        self.url_list = []
        self.logger = Logger(r'RequiredFiles\game_downloader.log')
        # self.logger = Logger(r'测试.log')
        self.n = 0

    def parse_init_page(self):
        """
        用于分析首页游戏，获得详细游戏内容url
        写入json文件中，方便后期续爬
        :return: None
        """
        response = self.session.get(self.init_url.format(self.year, 1))
        selector = etree.HTML(response.content.decode())
        all_page_num = int(selector.xpath(
            '//span[@class="page-navi"]/a/text()')[-1])
        i = 1
        while i < all_page_num + 1:
        # while i < 2:
            try:
                time.sleep(random.randint(1, 2))
                response = self.session.get(self.init_url.format(self.year, i))
                selector = etree.HTML(response.content.decode())
                game_list = selector.xpath('//div[@id="dle-content"]/div')
                for game_detail in game_list:
                    url = game_detail.xpath('./div[2]/a/@href')[0]
                    self.url_list.append(url)
                self.logger.info(
                    '{}年游戏第{}页下载完成，共获得{}条游戏url，'.format(
                        self.year, i, len(game_list)))
            except requests.exceptions.ConnectionError as e:
                self.logger.warn(
                    '访问{}被拒绝，等待1s后尝试继续访问，报错为{}'.format(
                        self.init_url.format(
                            self.year, i), e))
                i -= 1
            finally:
                i += 1
        self.logger.info('{}游戏初始界面下载完成'.format(self.year))
        with open(r'RequiredFiles\year_{}_game_urls.json'.format(self.year), 'w') as file:
            json.dump({j: self.url_list[j] for j in range(
                len(self.url_list))}, file, indent=4)

    def parse_detail_page(self, url, num=0):
        """
        用于分析详细界面，获得各种信息
        :param url: 网页url
        :param num: 游戏的编号，唯一，用于方便断点续爬
        :return: 详细信息
        """
        infor = {}
        # with open(r'RequiredFiles\proxies.txt','r') as file:
        #     temp = file.readlines()
        # proxies_list = [i.replace('\n','') for i in temp]
        # proxies_list.append(None)
        # proxy = random.choice(proxies_list)
        # proxies = {
        #     'http':'http://{}'.format(proxy),
        #     'https':'http://{}'.format(proxy)
        # }

        try:
            # self.session.proxies = proxies
            response = self.session.get(url)
            selector = etree.HTML(response.content.decode())
            # 最重要的两个，名字和下载地址
            try:
                name = selector.xpath('//div[@class="hname"]/h1/text()')[0]
                infor['游戏名称'] = name
                try:
                    download_url = selector.xpath(
                        '//a[@class="itemdown_games"]/@href')[0]
                    infor['下载地址'] = download_url
                except IndexError:
                    self.logger.error('{}未找到下载地址，手动访问进行下载'.format(name))
                infor['详细网页'] = url

                # 获得版本信息
                try:
                    version = selector.xpath(
                        '//div[@class="hname"]/div/text()')[0].split('[')[0]
                    infor['版本'] = version
                except Exception as e:
                    self.logger.error('未找到{}中的版本信息,错误为{}'.format(name, e))

                # 详细信息的基础xpath
                details = selector.xpath('//ul[@class="ul-details"]')[0]
                # 获得出版商信息
                try:
                    publisher = details.xpath('./li[2]/text()')[0]
                    infor['出版商'] = publisher
                except Exception as e:
                    self.logger.error('未找到{}中的出版商信息,错误为{}'.format(name, e))
                # 获得类型
                try:
                    types = [rus2chiDict[i]
                             for i in details.xpath('./li[3]/a/text()')]
                    infor['类型'] = types
                except Exception as e:
                    self.logger.error('未找到{}中的类型信息，错误为{}'.format(name, e))

                # 获得文件大小
                try:
                    size = selector.xpath('//div[@class="persize"]/span/text()')[0]
                    temp = size.split()
                    size = temp[0] + rus2chiDict[temp[1]]
                    infor['大小'] = size
                except Exception as e:
                    self.logger.error('未找到{}中的大小信息，错误为{}'.format(name, e))

                self.logger.info('{}下载完毕，剩余{},编号为{}'.format(name, self.n-num-1, num))

                try:
                    other_urls = []
                    other_urls_xpath = selector.xpath('//div[@class="torrent_list"]/div')
                    for xpath in other_urls_xpath:
                        temp = {}
                        if xpath.xpath('./@class')[0] != "tempcast":
                            temp['版本'] = xpath.xpath('./div[2]/text()')[0].split(':')[-1]
                            size = xpath.xpath('.//div[@class="packagedownld"]/span/text()')[0]
                            size_temp = size.split()
                            size = size_temp[0] + rus2chiDict[size_temp[1]]
                            temp['大小'] = size
                            temp['下载地址'] = xpath.xpath('.//a[@class="downld"]/@href')[0]
                            other_urls.append(temp)
                    infor['其他下载版本'] = other_urls
                except Exception as e:
                    print(e)
            except:
                self.logger.error('游戏{}网页出错，重新进行分析'.format(url))
                self.parse_detail_page(url)

            infor['发售年份'] = self.year
            return infor

        except requests.exceptions.ConnectionError as e:
            self.logger.error('访问网页{}失败，准备进行下次访问，错误为{}'.format(url, e))
            # if proxy is not None:
            #     proxies_list.remove(proxy)
            # proxies_list.remove(None)
            # with open(r'RequiredFiles\proxies.txt','w') as file:
            #     for pro in proxies:
            #         file.write(pro + '\n')
            time.sleep(random.randint(1, 2))
            self.parse_detail_page(url)

    def start(self):
        print('开始下载')
        try:
            with open(r'RequiredFiles\year_{}_game_urls.json'.format(self.year), 'r') as file:
                self.url_list = json.load(file)
                if not self.url_list:
                    raise FileNotFoundError
            self.logger.info('找到原本的json信息，开始续爬')
        except FileNotFoundError:
            self.logger.info('未检测到初始化界面下载信息，开始下载初始化界面')
            self.parse_init_page()

        try:
            with open(r'RequiredFiles\game_downloader.log','r') as file:
                temp = file.readlines()[-2].replace('\n','')
                num = int(temp.split(',编号为')[-1])
                self.logger.info('找到断点，序号为{}'.format(num))
        except Exception as e:
            print(e)
            num = -1
        finally:
            self.n = len(self.url_list)
            for i in range(num+1,len(self.url_list)):
                time.sleep(random.randint(2,3))
                yield self.parse_detail_page(self.url_list['{}'.format(i)],i)


if __name__ == '__main__':
    spider = Spider()
    spider.parse_detail_page('https://byrut.org/23452-xombee.html')

