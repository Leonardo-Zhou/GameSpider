# -*- coding: utf-8 -*-
"""
@File    : 测试不同ip.py
@Time    : 2022/3/22 19:59
@Author  : Leonardo Zhou
@Email   : 2974519865@qq.com
@Software: PyCharm
"""
import requests
from RequiredFiles.USER_AGENT import get_ua
from lxml import etree

url = 'https://www.ipaddress.com/'
proxies = {
    'http':'http://180.111.138.238:4212',
    'https': 'http://180.111.138.238:4212'
}
headers = get_ua()
response = requests.get(url, headers=headers,proxies=proxies,timeout=5)
selector = etree.HTML(response.content.decode())

print(selector.xpath('//*[@id="ipv4"]/a[1]/text()')[0])