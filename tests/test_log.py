# -*- coding:utf-8 -*-
# logging模块学习
import logging
import os
import threading

# http://www.cnblogs.com/i-honey/p/8052579.html
FORMAT = '%(asctime)s %(thread)d %(message)s'
DATEFMT = '[%Y-%m-%d %H:%M:%S]'
logging.basicConfig(level=logging.DEBUG, filename='test.log', format=FORMAT, datefmt=DATEFMT)
logging.debug('debug message')
logging.info('info message')
logging.warning('warn message')
logging.error('error message')
logging.critical('critical message')


def add(x, y):
    print(os.getpid())
    logging.warning('{} {}'.format(threading.enumerate(), x + y))


t = threading.Timer(1.0, add, args=[4, 5])
t.start()

# logging是一个模块，logger是logging模块的一个类
# 单独使用logging时，其实python也是直接创建了一个logger实例
