# -*- coding: utf-8 -*-
"""
@File    : logger.py
@Time    : 2022/3/21 17:43
@Author  : Leonardo Zhou
@Email   : 2974519865@qq.com
@Software: PyCharm
"""
import logging


class Logger:
    def __init__(self, path, cmd_level=logging.DEBUG, file_level=logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            '%Y-%m-%d %H:%M:%S')
        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(cmd_level)
        # 设置文件日志
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(file_level)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


if __name__ == '__main__':
    logger = Logger('测试.log', logging.ERROR, logging.DEBUG)
    logger.debug('一个debug信息')
    logger.info('一个info信息')
    logger.warn('一个warning信息')
    logger.error('一个error信息')
    logger.info('aaa')
