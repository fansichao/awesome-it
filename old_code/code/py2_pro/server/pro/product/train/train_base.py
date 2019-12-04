#! /usr/bin/python2
# -*- coding:utf-8 -*-
u"""
抢票软件12306
    - 登录网址: https://kyfw.12306.cn/otn/login/init

参考链接:
    - 下单步骤说明: https://blog.csdn.net/nonoroya_zoro/article/details/80108722
    - 链接请求说明: https://blog.csdn.net/u012593871/article/details/79241174
    - 本文参考内容: https://blog.csdn.net/qqtMJK/article/details/79375324

关键链接说明:
    1、检查用户是否保持登录成功     https://kyfw.12306.cn/otn/login/checkUser
    2、点击预定    https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest
    3、获取联系人     https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs
    4、检查选票人信息  https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo
    5、提交订单  https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount
    6、确认订单   https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue
    7、排队等待  https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime
    8、订单结果  https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue

说明: 
- 12306运营时间: 23:00 - 06:00
- 
"""

from __future__ import unicode_literals

import os
import time
import datetime
import sys
import logging
import re
import json
import traceback
import random

import urllib3
import pandas as pd
import ssl
import requests
ssl._create_default_https_context = ssl._create_unverified_context
# 禁用urllib3安全警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 不同 python 版本,quote的导入不同
if '2.' in sys.version:
    import urllib2 as parse
    reload(sys)
    sys.setdefaultencoding('utf-8')
    import urllib2 as urllib3
    import urllib2
    from urllib2 import urlopen
else:
    import urllib3
    import parse
    from urllib.request import urlopen
    

from ..base.settings import Config
from .tools_email import Email_Post


class Train_Base(object):
    u"""
    Train_Base: 基础函数类
        - base_dic_val2key      将val转key
        - get_city_code         获取城市字典表
        - get_city_code_csv     生成城市字典表文件
        - base_get_url_var      获取url变量值
        - bprint                封装打印
        - time_wait             等待时间
        - error_email           异常邮件提示
    """
    def __init__(self, *args, **kwargs):
        self.email_ins = Email_Post()

        return 
        username = self.username if not bool(kwargs.get('username')) else kwargs.get('username')
        password = self.password if not bool(kwargs.get('password')) else kwargs.get('password')
        # 用户登录
        if not bool(username): username = raw_input(u'@请输入用户名称:')
        if not bool(password): password = raw_input(u'@请输入用户密码:')
        #if not bool(password): password = getpass.getpass(u'@请输入用户密码:')
        # 站点日期
        if not bool(kwargs.get('startStation')): startStation = raw_input(u'@请输入出发车站:')
        if not bool(kwargs.get('endStation')): endStation = raw_input(u'@请输入到达车站:')
        if not bool(kwargs.get('startDate')): startDate = raw_input(u'@请输入出发日期[2018-10-01]:')
        # 自动订票
        if not bool(kwargs.get('trainNameList')): trainNameList = raw_input(u'@请输入车次[G34,G23]:').split(',')
        logging.info(u'说明: 可选座位类型如下[%s] '%(",".join(self.seatTypeDict.values())))
        if not bool(kwargs.get('seatTypeList')): seatTypeList = raw_input(u'@请输入座位[二等座,一等座]:').split(',')
        logging.info(u'说明: 乘车人姓名/身份证/电话必须已经存在于账号中')
        if not bool(kwargs.get('passengersList')): passengersList = raw_input(u'@请输入乘车人姓名[甲,乙]:').split(',')
 
        pass

    def base_dic_val2key(self, val='',dic={}):
        u""" 将val转为key
        :param val: value值
        :parram dic: 字典
        """
        val = dic.keys()[ dic.values().index(val)]
        return val
    
    
    def get_city_code(self, city_code_filename=os.path.join(Config.TMP_PATH,'train_city_code.csv')):
        u""" 获取城市字典表
        :param city_code_filename: 城市字典表文件名称
    
        """
        print city_code_filename
        logging.debug('>>>> 获取城市字典表开始')
        if not bool(os.path.exists(city_code_filename)):
            logging.warning('>>>>>> 城市字典表文件[%s]不存在,自动生成中!!!')
            self.get_city_code_csv(filename=city_code_filename)
    
        df = pd.read_csv(city_code_filename)
        station_rows = df.to_dict(orient='records')
        station = dict()
        for dic in station_rows:
            station[dic[u'city_name'].decode()] = dic[u'city_code_search'.decode()]
        logging.debug('>>>> 获取城市字典表成功,共[%s]个城市' % str(len(station.keys())))
        return station

    def base_get_url_var(self, url=None, re_pattern=None):
        u""" 获取 HTML内容 指定变量数据
    
        :param url: 链接地址
        :param re_pattern: 正则表达式
        """
        try:
            content = urllib2.urlopen(url).read()
            data = re_pattern.findall(content)
        except Exception as e:
            logging.error('>>>>>>>> 获取数据失败,或存在链接[%s]有误' % url)
            print e
            return False
        return data
    
    def get_city_code_csv(self, filename=None):
        u""" 生成城市 代码-名称 字典表文件
    
        :param filename: 生成的文件名称
        """
        # 参数
        logging.info('>>>> 生成城市字典表文件开始')
        city_code_url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9018"
        pattern = re.compile(
            r"var\s+station_names[=\s]+((?:(?!stortData[=\s]+)[\s\S])*);")
        city_code_header_code = [u'city_code_simpleA', u'city_name', u'city_code_search',
                u'city_code_full', u'city_code_simpleB', u'city_sortno']
        city_code_header_name = [u'城市简称A', u'城市名称', u'查询代码', 
                u'城市全称', u'城市简称B', u'序号']
    
        data = self.base_get_url_var(url=city_code_url, re_pattern=pattern)
        # 解析数据 得到 字典表
        station = dict();
        data = data[0][:-1][1:]
        rows = []
        for city_code in data.split('@'):
            if not bool(city_code):
                continue
            tmp = city_code.split('|')
            rows.append(city_code.split('|'))
    
        df = pd.DataFrame(rows, columns=city_code_header_code)
        df.to_csv(filename, index=False)
        logging.info('>>>> 生成城市字典表文件完成')
        return True
    
    def bprint(self, msg, ltype='debug'):
        if ltype == 'debug':
            # print msg
            logging.debug(msg)
        return msg

    def error_email(self, msg):
        self.email_ins.email_send_info(msg)
    
    def time_wait(self, wait_second, len=5):
        for i in range(wait_second):
            if i % len and i != 0:
                logging.info(">> 等待[%s]秒"%str(len))
        
        logging.info(">> 共计等待[%s]秒"%str(wait_second))
        
        
    
        



if __name__ == '__main__':
    train_base = Train_Base()
