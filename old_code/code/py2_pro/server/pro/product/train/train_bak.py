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
1. 检查用户是否保持登录成功     https://kyfw.12306.cn/otn/login/checkUser
2. 点击预定    https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest
3. 获取联系人     https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs
4. 检查选票人信息  https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo
5. 提交订单  https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount
6. 确认订单   https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue
7. 排队等待  https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime
8. 订单结果  https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue

注意事项: 
- 12306运营时间: 23:00 - 06:00
- 购票等session必须为同一个
- 学生票 需要先在12306上添加乘客信息 ADULT
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
    from urllib2 import urlopen
else:
    import urllib3
    import parse
    from urllib.request import urlopen
    
from ..base.settings import Config
from .tools_email import Email_Post
from .train_base import Train_Base
from .train_login import login


class Train12306():
    u""" 12306 自动订票脚本
    步骤流程
        - 检查用户是否保持登录
        - 点击预订
        - 获取联系人
        - 检查选票人信息
        - 提交订单
        - 确认订单
        - 排队等待
        - 订单结果

    函数说明

    - __init__                      初始化
    - 主函数入口
        - main_input                手工输入函数入口
        - main_code                 自动输入函数入口
            - main_login            用户登录函数入口
            - main_search           信息查询函数入口
            - main_buyticket        车票预订函数入口
    - 获取车票等信息
        - get_passenger_info        获取乘客信息
        - search_ticket             搜素车票
        - check_ticket              校验车票
        - check_user                校验用户信息
        - submit_order              提交车次信息
        - confirm_passenger         确认用户信息
        - check_order               校验订单
        - get_buy_image             重复图片验证
    - 预订车票
        - get_queue_count           多人购票队列
        - confirm_single_for_queue  单人购票队列
        - wait_time                 等待队列
    """

    def __init__(self):
        u""" 初始化

        :param self.session: 网络请求会话
        :param self.cookies: 浏览器cookies
        :param self.seatTypeList_name: 座位类型名称
        
        :param self.trainIndexOfBuy: 所买车次索引
        :param self.seatIndexOfBuy: 所买座位类型索引
        :param self.passengerNameList: 乘客姓名列表
        :param self.passengerIdList: 乘客身份证号列表
        :param self.passengerPhoneList: 乘客电话列表

        :param self.seatCodeList: 
        :param self.stationCodeDict: 城市字典表
        :param self.seatTypeDict: 座位类型字典表
        :param self.code: 验证码坐标图
        :param self.headers: 请求头
        
        """
        # 代理IP
        from pro.module.scrapy.scrapy_proxy import use_proxy
        self.session = use_proxy().get('session') if bool(
            use_proxy().get('session')) else requests.session()
        self.cookies = self.session.cookies

        
        self.img_filepath = os.path.join(Config.TMP_PATH,'code.png')
        self.start_datetime = datetime.datetime.now()

        # 实例化
        self.train_base = Train_Base()
        self.email_ins = Email_Post()
        # 用户密码
        self.username = Config.train_username
        self.password = Config.train_password
        # 城市字典表
        self.stationCodeDict = self.train_base.get_city_code()
        # 乘次信息
        self.trainIndexOfBuy = int()
        self.seatIndexOfBuy = int()
        self.passengerNameList = list()
        self.passengerIdList = list()
        self.passengerPhoneList = list()
        self.trainInfoSecretStrList = list()
        # TODO
        self.seatCodeList = ['O','M','1','软座','3','4','F','无座','9','9','6']
        self.seatTypeList_name = [u'二等座',u'一等座',u'硬座',u'软座',
            u'硬卧',u'软卧',u'动卧',u'无座',u'商务座',u'特等座',u'高级软卧']
        # 座位字典表 TODO
        self.seatTypeDict = {
            u'O': u'二等座',
            u'M': u'一等座',
            u'9': u'商务座',
            u'6': u'高级软卧',
            u'4': u'软卧',
            u'F': u'动卧',
            u'3': u'硬卧',
            u'1': u'硬座',
            u'A': u'其他',  # 高级动卧
            # u'软座', # 未知
            # u'无座', # 和所选座位一致
        }
        # 验证码 坐标图
        self.code = [
            None,
            '35,35',
            '105,35',
            '175,35',
            '245,35',
            '35,105',
            '105,105',
            '175,105',
            '245,105']
        # 请求头
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://kyfw.12306.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4355.400 QQBrowser/9.7.12672.400',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
        }

    ###############
    #### 主函数
    ###############
    def main_code(self, *args, **kwargs):
        u""" 程序入口
        :param clickList:       图片验证码数字[2,5](必需要手动输入) TODO
        :param username:        用户名称
        :param password:        用户密码
        :param startStation:    出发车站
        :param endStation:      到达车站
        :param startDate:       出发日期 
        :param trainNameList:   车次名称[G34,G23]
        :param seatTypeList:    座位[二等座,一等座]
        :param passengersList:  乘客姓名[甲,已]
        """
        #### 参数准备
        # 字符串 转 变量对象
        for k,v in kwargs.items():
            if isinstance(v,str) or isinstance(v,unicode):
                var = "{k}='{v}'".format(**{'k':k,'v':v})
                logging.debug("变量赋值情况[%s:%s]"%(k,v))
            else:
                var = "{k}={v}".format(**{'k':k,'v':v})
                for i in v:
                    logging.debug("变量赋值情况[%s:%s]"%(k,i))
            exec(var)

        username = self.username if not bool(kwargs.get('username')) else kwargs.get('username')
        password = self.password if not bool(kwargs.get('password')) else kwargs.get('password')


        # 二维码登录
   #     from pro.tools.train_login_qrcode import Train_Login_QrCode
   #     self.train_login_qrcode = Train_Login_QrCode(session=self.session.cookies=self.cookies)
   #     self.train_login_qrcode.main()
   #     flag = False
   #     while not flag:
   #         flag,umatk = self.train_login_qrcode.check_qrcode()
   #         logging.debug(flag)
   #         time.sleep(1)

   #     # 识图自动登录
   #     login(username, password)

        # 手动输入验证码
        from pro.tools.train_login_input import Train_Login
        train_login = Train_Login(session=self.session,cookies=self.cookies)
        train_login.main_login(username=username, password=password)


        # 仅第一次需要处理 cookies TODO
        # 设置 cookies
        self.cookies['_jc_save_fromDate'] = startDate
        self.cookies['_jc_save_fromStation'] = ( 
            parse.quote( startStation.encode('unicode_escape').decode('latin-1') + ',' + 
            self.stationCodeDict[startStation]).replace( '\\', '%')).upper().replace( '%5CU', '%u')
        self.cookies['_jc_save_toDate'] = startDate
        self.cookies['_jc_save_toStation'] = ( 
            parse.quote( endStation.encode('unicode_escape').decode('latin-1') + ',' + 
            self.stationCodeDict[endStation]).replace( '\\', '%')).upper().replace( '%5CU', '%u')
        self.cookies['_jc_save_wfdc_flag'] = "dc"

        # 异常处理
        main_search_suc = False
        try_count = 0
        while not bool(main_search_suc):
            try_count += 1
            try:
                # 第一次
                main_search_suc = self.main_search( startStation, endStation, startDate, 
                    seatTypeList, passengersList, trainNameList)
            except Exception as e:
                logging.debug(traceback.print_exc())
                logging.error('获取车票信息失败,重新尝试,尝试次数[%s]!!!'%str(try_count))
            time.sleep(5)
            
        # 异常处理
        main_buytticket_suc = False
        try_count = 0
        while not bool(main_buytticket_suc):
            try_count += 1
            try:
                # 第一次
                main_buytticket_suc = self.main_buyticket( startStation, endStation, 
                    startDate, seatTypeList, passengersList )
            except Exception as e:
                logging.error('购买车票失败,重新尝试,尝试次数[%s]!!!'%str(try_count))
                logging.debug(traceback.print_exc())
            time.sleep(5)

        return True

    ###############
    #### 主函数 调用
    ###############
   
    def main_search(self, startStation, endStation, startDate, seatTypeList, passengersList, trainNameList):
        u""" 查票+乘客信息+下单 """
        self.check_ticket( startStation, endStation, startDate, seatTypeList, passengersList, trainNameList)
        self.check_user()
        # 选择车次
        self.submit_order(startStation, endStation, startDate)
        self.confirm_passenger()
        self.get_passenger_info()
        self.check_order(passengersList)
        return True
    
    def main_buyticket(self, startStation, endStation, startDate, seatTypeList, passengersList, clickList=None):
        u""" 买票 """
        self.get_queue_count(startStation, endStation, startDate, seatTypeList)
        self.confirm_single_for_queue(seatTypeList, passengersList, clickList=None)
        self.wait_time()
        self.end_datetime = datetime.datetime.now()
        self.second = self.end_datetime - self.start_datetime
        return True

    ###############
    #### 车票查询模块
    ###############
    def get_passenger_info(self):
        u""" 获取联系人信息
        """
        logging.debug(">>>> 获取联系人信息 开始")
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        data = {
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": self.reSubmitTk
        }

        response = self.session.post( url=url, data=data, headers=self.headers, 
            cookies=self.cookies, verify=False) 
        dic = json.loads(response.content)

        if dic['messages'] != []:
            if dic['messages'][0] == '系统忙,请稍后重试':
                self.train_base.error_email('系统忙,请稍后重试')
                return 'systembusy'
        self.passengerAllInfoList = dic['data']['normal_passengers']
        for a in self.passengerAllInfoList:
            self.passengerNameList.append(a['passenger_name'])
            self.passengerIdList.append(a['passenger_id_no'])
            self.passengerPhoneList.append(a['mobile_no'])
        logging.debug(">>>> 获取联系人信息 成功")
        return self.passengerNameList

    def search_ticket(self, startStation, endStation, startDate, firstrun_flag=True):
        u"""
        # log是判断服务是否正常，用queryA进行查询

        :param firstrun_flag:是否是第一次运行

        """
        logging.debug(">>>> 查询是否有票 开始")

        # 查询 12306服务是否正常
        url1 = 'https://kyfw.12306.cn/otn/leftTicket/log?\
            leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&\
            leftTicketDTO.to_station={}&purpose_codes=ADULT'.format( startDate, 
            self.stationCodeDict[startStation], self.stationCodeDict[endStation]).replace(' ','')
        response1 = self.session.get( url=url1, headers=self.headers, cookies=self.cookies, verify=False)
        dic1 = json.loads(response1.content)
    
        #logging.debug(dic1)
        if dic1['status']:
            logging.debug("12306服务正常")

        # 生成查询链接
        # 由于12306查询链接中自带一个随机字母
        self.query = 'leftTicket/queryA'
        url2 = 'https://kyfw.12306.cn/otn/{}?\
            leftTicketDTO.train_date={}&\
            leftTicketDTO.from_station={}&\
            leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
            self.query, startDate,
            self.stationCodeDict[startStation], self.stationCodeDict[endStation]).replace(' ', '')

        # 拿到正确的链接
        for i in 'ABCDEFGHIJKMNOPQRSTUVWXYZ':
            time.sleep(1)
            que = "query" + i
            url2_mid = url2.replace('queryA',que)
            dic2 = None
            logging.debug(url2_mid)

            try:
                session = requests.session()
                response2 = session.get( url=url2_mid, headers=self.headers, cookies=self.cookies, verify=False)
                dic2 = json.loads(response2.content)
            except Exception as e:
                pass
                #logging.debug(traceback.print_exc())
                #self.train_base.error_email(">>>> query链接错误,重新尝试");
            
            #logging.debug(dic2)
            if dic2 :
                break

        response2 = self.session.get( url=url2_mid, headers=self.headers, cookies=self.cookies, verify=False)
        #logging.debug(response2.content)
        dic2 = json.loads(response2.content)
        #logging.debug(dic2)

        if dic2['status'] is False:
            if 'c_url' in dic2.keys():
                self.query = dic2['c_url']
                return "statusError"
            return "statusError"
        elif dic1["messages"] != []:
            # if dic["messages"][0] == u"选择的查询日期不在预售日期范围内":
            return "search_error002"
        else:
            logging.debug("查询车成功")


        # 每次查询前初始化
        self.trainInfoStartTimeList, self.trainInfoEndTimeList, self.trainInfoSecretStrList, self.trainInfoNameList, self.trainInfoLocationList, self.trainInfoNoList = [], [], [], [], [], []
        self.dw, self.swz, self.ydz, self.edz, self.yz, self.yw, self.wz, self.rw, self.gjrw, self.tdz, self.rz = [
            ], [], [], [], [], [], [], [], [], [], []
        #:param seatTypeList: 所选座位类型
        #:param self.seatTypeList: 所有座位票数情况
        # 二等座,一等座,硬座,软座,硬卧,软卧,动卧,无座,商务座,特等座,高级软卧
        self.seatTypeList = ( self.edz, self.ydz, self.yz, self.rz, self.yw, self.rw, self.dw, self.wz, self.swz, self.tdz, self.gjrw)
 

        # logging.error("sssssssssssssssssssssssssssssss")
        # logging.error(dic2)
        # logging.error(dic2['data']['result'])
        for a in dic2['data']['result']:
            print a
            self.trainInfoSecretStrList.append(a.split("|")[0])
            self.trainInfoNoList.append(a.split("|")[2])
            self.trainInfoNameList.append(a.split("|")[3])
            self.trainInfoStartTimeList.append(a.split("|")[8])
            self.trainInfoEndTimeList.append(a.split("|")[9])
            self.trainInfoLocationList.append(a.split("|")[15])
            self.dw.append(a.split("|")[33])
            self.swz.append(a.split("|")[32])
            self.ydz.append(a.split("|")[31])
            self.edz.append(a.split("|")[30])
            self.yz.append(a.split("|")[29])
            self.yw.append(a.split("|")[28])
            self.wz.append(a.split("|")[26])
            self.tdz.append(a.split("|")[25])
            self.rz.append(a.split("|")[24])
            self.rw.append(a.split("|")[23])
            self.gjrw.append(a.split("|")[21])
        self.seatTypeList = (
        self.edz, self.ydz, self.yz, self.rz, self.yw, self.rw, self.dw,
        self.wz, self.swz, self.tdz, self.gjrw)
        return self.trainInfoNameList

    def check_ticket(self, startStation='湖州', endStation='北京', startDate='2018-10-03',
                     seatTypeList=[u'二等座'], passengersList=['范寺超'], trainNameList=['G34']):
        u""" 检查是否有票

        :param startStation:    出发车站
        :param endStation:      到达车站
        :param startDate:       出发日期 
        :param seatTypeList:    座位[二等座,一等座]
        :param passengersList:  乘客姓名[甲,已]
        :param trainNameList:   车次列表[G23,G34]
        """
        logging.debug(">>>> 检查是否有票 开始")
        searchResult = self.search_ticket(startStation, endStation, startDate)
        error_lists = ["wrongtype", "NetWorkError", "searchFail",
            "statusError", "search_error002"]
        if searchResult in error_lists:
            logging.debug(">>>> 检查是否有票 失败 %s" % searchResult)
            return False

        have_ticket = False
        count = 0
        while not bool(have_ticket):
            count += 1
            # 刷票机制
            for a in trainNameList:
                # 获取 车次在当日所有车次中的 索引index
                if a not in self.trainInfoNameList:
                    logging.error(u"!!! [%s]车次不在可购票的车次中,请检查车次信息"%a)
                    return False
                trainIndex = self.trainInfoNameList.index(a)
                # 座位列获取
                for seatType in seatTypeList:
                    b = self.seatTypeList_name.index(seatType)
                    if self.trainInfoSecretStrList[trainIndex] == 'null':
                        msg = "没票了-trainInfoSecretStrList-密钥错误"
                        continue
                        #break
                    elif self.seatTypeList[b][trainIndex] == u"无" or self.seatTypeList[b][trainIndex] == "":
                        msg = "没票了"
                        continue
                    elif self.seatTypeList[b][trainIndex] == "*":
                        msg = "还没开始售票"
                        continue
                    elif self.seatTypeList[b][trainIndex] != u"有" and len(passengersList) > int(self.seatTypeList[b][trainIndex]):
                        msg = "票没人多"
                        continue
                    else:
                        have_ticket = True
                        msg = "查询到有票"
                        self.trainIndexOfBuy = trainIndex
                        self.seatIndexOfBuy = b

            # TODO
            infos = str();
            #for train_name in trainNameList:
            for seatType in seatTypeList:
                for passenger in passengersList:
                    info = u">>>> 日期:[%s] 车次:[%s] 座位:[%s] 乘客:[%s] 刷票次数[%s] 原因[%s] <<<< \r"%(startDate,trainNameList,seatType,passenger,str(count),msg)
                    sys.stdout.write(info)
                    sys.stdout.flush()
                    infos += info + '\n'

            # TODO 进入 12306 错误页面了
            # DEBUG  : "GET /mormhweb/logFiles/error.html HTTP/1.1" 200 2042

            # 没有成功抢到票,重新检索是否有票
            time.sleep(2)
            try:
                searchResult = self.search_ticket(startStation, endStation, startDate, firstrun_flag=False)
            except Exception as e:
                time.sleep(10)
                try:
                    searchResult = self.search_ticket(startStation, endStation, startDate, firstrun_flag=False)
                except Exception as e:
                    logging.debug(traceback.print_exc())
                    return False

            if count == 1:
                self.email_ins.email_send_info(">>>> 已经开始抢票了\n"+infos)
            
            if count % 7200 == 0:
                self.email_ins.email_send_info(infos)
                        
        logging.debug("查询到有票")
        self.email_ins.email_send_info(u"@@@@@@@@ 有票啦 @@@@@@@@\n"+infos)

        return self.seatTypeList[b][trainIndex]

    def check_user(self):
        u""" 验证用户是否在线
        """
        logging.debug(">>>> 验证用户 开始")
        url = 'https://kyfw.12306.cn/otn/login/checkUser'
        data = {"_json_att": ""}
        # self.headers["Cache-Control"] = "no-cache"
        # self.headers["If-Modified-Since"] = "0"
        response = self.session.post( url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)
        #logging.error(response.content)
        dic = json.loads(response.content)
        if dic['data']['flag']:
            logging.info("用户在线验证成功")
            return True
        else:
            logging.error('检查到用户不在线,请重新登陆')
            return False

    def submit_order(self, startStation, endStation, startDate):
        u""" 提交车次订单
        """
        logging.debug(">>>> 提交订单 开始")
        url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        logging.debug(self.trainInfoSecretStrList)
        logging.debug(self.trainIndexOfBuy)
        data = {
                 "secretStr": parse.unquote(self.trainInfoSecretStrList[self.trainIndexOfBuy]),
                 "train_date": startDate,
                 "back_train_date": startDate,
                 "tour_flag": "dc",
                 "purpose_codes": "ADULT",
                 "query_from_station_name": startStation,
                 "query_to_station_name": endStation,
                 "undefined": ""
                 }
        response = self.session.post( url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)
        # logging.error(response.content)
        dic = json.loads(response.content)
        print response
        #dic = json.loads(response)
        # TODO ???????

        if dic['status']:
            logging.debug('提交订单成功')
            return True
        elif dic['messages'] != []:
            if dic['messages'][0] == "车票信息已过期,请重新查询最新车票信息":
                logging.debug('车票信息已过期,请重新查询最新车票信息')
                return "ticketInfoOutData"
        else:
            logging.debug("提交失败")
            return False

    def confirm_passenger(self):
        u""" 确认用户信息
        """
        logging.debug('>>>> 确认用户信息 开始')
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        data = {"_json_att": ''}
        response = self.session.post( url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)
        try:
            # logging.error('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            # logging.error(response.text)
            self.reSubmitTk = re.findall( u'globalRepeatSubmitToken = \'(\S+?)\'', response.text)[0]
            self.keyIsChange = re.findall( u'key_check_isChange\':\'(\S+?)\'', response.text)[0]
            self.leftTicketStr = re.findall( u'leftTicketStr\':\'(\S+?)\'', response.text)[0]
            logging.debug('>>>> 确认用户信息 成功')
        except:
            logging.debug(traceback.print_exc())
            self.train_base.error_email(">>>> 确认用户信息 失败");
            logging.debug('>>>> 确认用户信息 失败')
            return 'NetWorkError'

    def check_order(self, passengersList):
        logging.debug(">>>> 验证订单 开始")

        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        passengerTicketStr = ""
        oldPassengerStr = ""


        try:
            for passenger_name in passengersList:
                a = passengersList.index(passenger_name)
                passengerTicketStr += self.seatCodeList[self.seatIndexOfBuy] + ",0,1,{},1,{},{},N_".format(
                    self.passengerNameList[a], self.passengerIdList[a], self.passengerPhoneList[a])

                oldPassengerStr += "{},1,{},1_".format( self.passengerNameList[a], self.passengerIdList[a])
                print oldPassengerStr
        except Exception as e:
            logging.debug(traceback.print_exc())
            logging.error('网站车票信息错误，请稍后重试。(车站查询有票，但是实际无票，无法预订)!!')
            self.train_base.error_email('网站车票信息错误，请稍后重试。(车站查询有票，但是实际无票，无法预订)!!')
            logging.error(traceback.print_exc())
            return

        data = {
            "cancel_flag": "2",
            "bed_level_order_num": "000000000000000000000000000000",
            "passengerTicketStr": passengerTicketStr,
            "oldPassengerStr": oldPassengerStr,
            "tour_flag": "dc",
            "randCode": "",
            "whatsSelect": "1",
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": self.reSubmitTk
        }
        response = self.session.post( url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)
        dic = json.loads(response.content)
        if dic['data']['submitStatus'] is True:
            if dic['data']['ifShowPassCode'] == 'N':
                return True
            if dic['data']['ifShowPassCode'] == 'Y':
                return "Need Random Code"
        else:
            logging.debug("checkOrderFail")
            return False
        logging.debug(">>>> 验证订单 成功")


    def get_buy_image(self):
        u""" 购票紧张时，额外环节

        # 1.在这个过程之前,12306会get一张新验证码图片,在购票紧张的时候会在购票时候弹出给你填,如果购票不紧张就不会有但是我们要get到这张图
        # 2.判断要不要填这个验证的key在上面代码里’ifShowPassCode’ == ‘Y’就是要填,我们要做判断.这里给出新验证码的获取代码
        """
        logging.debug(">>>> 获取忙碌购票时图片验证码 开始")

        url = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp&{}'.format(
            random.random())
        response = self.session.get( url=url, headers=self.headers, cookies=self.cookies, verify=False)
        if os.path.exists(self.img_filepath):
            os.system('rm -f %s' % self.img_filepath)
        with open(self.img_filepath, 'wb') as f:
            f.write(response.content)
        logging.debug(">>>> 获取忙碌购票时图片验证码 成功")

    ###############
    #### 订票模块
    ###############
    def get_queue_count(self, startStation, endStation, startDate, seatType):
        u""" 获取用户队列 """
        logging.debug(">>>> 获取用户队列 开始")

        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        thatdaydata = datetime.datetime.strptime(startDate, "%Y-%m-%d")
        train_date = "{} {} {} {} 00:00:00 GMT+0800 (中国标准时间)".format(thatdaydata.strftime('%a'),
                                                                     thatdaydata.strftime(
                                                                         '%b'), startDate.split('-')[2],
                                                                     startDate.split('-')[0])
        data = {
            "train_date": train_date,
            "train_no": self.trainInfoNoList[self.trainIndexOfBuy],
            "stationTrainCode": self.trainInfoNameList[self.trainIndexOfBuy],
            "seatType": self.seatCodeList[self.seatIndexOfBuy],
            "fromStationTelecode": self.stationCodeDict[startStation],
            "toStationTelecode": self.stationCodeDict[endStation],
            "leftTicket": self.leftTicketStr,
            "purpose_codes": "00",
            "train_location": self.trainInfoLocationList[self.trainIndexOfBuy],
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": self.reSubmitTk
        }
        response = self.session.post( url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)
        dic = json.loads(response.content)
        if dic['status']:
            logging.debug(">>>> 获取用户队列 成功")
        else:
            logging.debug("进入队列失败")
            return False
        return True

    def confirm_single_for_queue( self, seatType, passengersList, clickList=None):
        u""" 获取单一变量 """
        logging.debug(">>>> 获取单一队列 开始")

        url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        passengerTicketStr = ""
        oldPassengerStr = ""
        # 
        for passenger_name in passengersList:
            a = passengersList.index(passenger_name)
            passengerTicketStr += self.seatCodeList[self.seatIndexOfBuy] + ",0,1,{},1,{},{},N_".format(
                self.passengerNameList[a], self.passengerIdList[a], self.passengerPhoneList[a])
            oldPassengerStr += "{},1,{},1_".format(
    self.passengerNameList[a], self.passengerIdList[a])

        if clickList is not None:
            verifyList = []
            for a in clickList:
                verifyList.append(self.code[int(a)])
            codeList = ','.join(verifyList)
            #logging.debug(codeList)
        else:
            codeList = ''

        data = {
            "passengerTicketStr": passengerTicketStr,
            "oldPassengerStr": oldPassengerStr,
            "randCode": codeList,
            "purpose_codes": "00",
            "key_check_isChange": self.keyIsChange,
            "leftTicketStr": self.leftTicketStr,
            "train_location": self.trainInfoLocationList[self.trainIndexOfBuy],
            "choose_seats": "",
            "seatDetailType": "000",
            "whatsSelect": "1",
            "roomType": "00",
            "dwAll": "N",
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": self.reSubmitTk
        }
        response = self.session.post( url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)
        dic = json.loads(response.content)

        if 'data' in dic.keys():
            if dic['data']['submitStatus'] is True:
                logging.debug("提交订单成功")
                return True
            elif dic['data']['errMsg'] == u"验证码输入错误！":
                return "wrongCode"

        else:
            logging.debug("提交订单失败")
            return False
        logging.debug(">>>> 获取单一队列 成功")

    # 等待时间
    def wait_time(self):
        u""" 取票排队 """
        logging.debug('>>>> 获取等待时间 开始')
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/\
            queryOrderWaitTime?random={}&tourFlag=dc&\
            _json_att=&REPEAT_SUBMIT_TOKEN={}'.format( round(time.time() * 1000), 
            self.reSubmitTk).replace(' ','')
        response = self.session.get( url=url, headers=self.headers, cookies=self.cookies, verify=False)
        dic = json.loads(response.content)
        wait_second = None
        if dic['status']:
            if dic['data']['queryOrderWaitTimeStatus']:
                if dic['data']['waitTime'] == -1:
                    self.orderId = dic['data']['orderId']
                wait_second = dic['data']['waitTime']
        if bool(wait_second):
            logging.debug(">>>> 获取等待时间 成功")
            self.train_base.time_wait(wait_second)
        else:
            logging.error(">>>> 获取等待时间 失败")
        return True

if __name__ == '__main__':
    train=Train12306()
    train.main_code(
        startStation='北京西', endStation='九江', startDate='2019-01-26',
        #trainNameList=[u'Z67'], seatTypeList=[u'硬卧'], passengersList=[u'朱亚芬']
        trainNameList=[u'Z67'], seatTypeList=[u'硬卧'], passengersList=[u'朱亚芬']
    )

