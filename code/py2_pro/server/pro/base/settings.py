#! -*- coding:utf-8 -*-
u"""

- 配置文件
@创建时间: 2018-09-08
@创建作者: scfan
@更新时间: 

"""

import os
import sys

from string import Template



class Config(object):
    u""" 配置文件 """

    """
        app
    """
    BASE_PATH = os.path.join(sys.path[0], '../')
    print BASE_PATH

    TMP_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../tmp") 
    IMG_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../statics/images") 
    TESTS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../tests") 


    """
        邮箱配置
    """
    # 邮箱发送方
    msg_from = os.environ['msg_from']
    # 邮箱接受方
    msg_to = os.environ['msg_to']
    # 邮箱发送方授权码
    msg_from_sqm = os.environ['msg_from_sqm']
    
    
    """
        12306抢票软件 
    """
    # 用户名
    train_username = os.environ['train_username']
    # 密码
    train_password = os.environ['train_password']

    """
        数据库地址
    """
    DB_CONFIG = {
        'DB_USER' : 'fdm',             # 数据库用户
        'DB_PASSWD' : 'qwe123',        # 数据库密码
        'DB_HOST' : '192.168.172.70',  # 数据库地址
        'DB_PORT' : '1521',            # 数据库端口
        'DB_INSTANCE' : 'fdm',         # 数据库实例名
    }

    SQLALCHEMY_DATABASE_URL = Template("oracle://$DB_USER:$DB_PASSWD@$DB_HOST:$DB_PORT/$DB_INSTANCE").safe_substitute(**DB_CONFIG)
    
    SQLITE_CONFIG = {
        'DB_NAME':'mypro'
    }

    # 功能模块参数
    """
        爬虫模块
    """
    scrapy_proxy_csvname = os.path.join(TESTS_PATH, 'scrapy_proxy_ipaddr.csv')
    scrapy_proxy_firstipaddr = ['183.129.207.84:41545']

    
    """
        火车票抢票
    """
    

    # 基础参数

