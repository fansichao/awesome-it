#! /usr/bin/python2
# -*- coding:utf-8 -*-
u"""
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

# 程序无法运行
# 程序不便于维护
# 程序写法不爽

class Train12306():

    def __init__(self, *lis, **kwargs):
        u""" 初始化
        """
        # 代理IP
        from pro.module.scrapy.scrapy_proxy import use_proxy
        self.session = use_proxy().get('session') if bool(
            use_proxy().get('session')) else requests.session()
        # TODO
        self.session = requests.session()
        self.cookies = self.session.cookies
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://kyfw.12306.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4355.400 QQBrowser/9.7.12672.400',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
        }
 

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
        self.code = [ None, '35,35', '105,35', '175,35', '245,35', '35,105', '105,105', '175,105', '245,105']

        self.start_datetime = datetime.datetime.now()

        # 实例化
        self.train_base = Train_Base()
        self.email_ins = Email_Post()
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
        self.init_train(*lis, **kwargs)

    def init_train(self, *lis, **kwargs):
        u''' 参数初始化
        :param clickList:       图片验证码数字[2,5](必需要手动输入) TODO
        :param username:        用户名称
        :param password:        用户密码
        :param self.startStation:    出发车站
        :param self.endStation:      到达车站
        :param self.startDate:       出发日期 
        :param self.trainNameList:   车次名称[G34,G23]
        :param self.seatTypeList:    座位[二等座,一等座]
        :param self.passengersList:  乘客姓名[甲,已]
        '''
        # 初始化信息
        init_info = ["self.startStation", "self.endStation", "self.startDate", "self.seatTypeList", "self.passengersList", "self.trainNameList"]
        #### 参数准备
        # 字符串 转 变量对象
        for k,v in kwargs.items():
            if isinstance(v,str) or isinstance(v,unicode):
                var = "self.{k}='{v}'".format(**{'k':k,'v':v})
                logging.debug("变量赋值情况[%s:%s]"%(k,v))
            else:
                var = "self.{k}={v}".format(**{'k':k,'v':v})
                for i in v:
                    logging.debug("变量赋值情况[%s:%s]"%(k,i))
            exec(var)

        self.img_filepath = os.path.join(Config.TMP_PATH,'code.png')
        # 用户密码
        self.username = Config.train_username if not bool(kwargs.get('username')) else kwargs.get('username')
        self.password = Config.train_password if not bool(kwargs.get('password')) else kwargs.get('password')
        logging.info(kwargs)
        logging.info(lis)

        # 仅第一次需要处理 cookies TODO
        # 设置 cookies
        self.cookies['_jc_save_fromDate'] = self.startDate
        self.cookies['_jc_save_fromStation'] = ( 
            parse.quote( self.startStation.encode('unicode_escape').decode('latin-1') + ',' + 
            self.stationCodeDict[self.startStation]).replace( '\\', '%')).upper().replace( '%5CU', '%u')
        self.cookies['_jc_save_toDate'] = self.startDate
        self.cookies['_jc_save_toStation'] = ( 
            parse.quote( self.endStation.encode('unicode_escape').decode('latin-1') + ',' + 
            self.stationCodeDict[self.endStation]).replace( '\\', '%')).upper().replace( '%5CU', '%u')
        self.cookies['_jc_save_wfdc_flag'] = "dc"
        
        self.trainInfoNameList = list()

    ###############
    #### 主函数
    ###############
    def main(self, *args, **kwargs):
        u""" 程序入口
        :param password:        用户密码
        """
        # 登录模块
        self.main_login()
        # 检查票是否存在
        u""" 查票+乘客信息+下单 """
        self.check_ticket()
        self.check_user()
        # 选择车次
        self.submit_order()
        self.confirm_passenger()
        self.get_passenger_info()
        self.check_order()
        u""" 买票 """
        self.get_queue_count()
        self.confirm_single_for_queue(clickList=None)
        self.wait_time()
        self.end_datetime = datetime.datetime.now()
        self.second = self.end_datetime - self.start_datetime
        return True
        
    def main_login(self,login_type="input"):    
        u'''登录模块
        @param login_type:登录方式
        '''
        if login_type.lower() not in ['all','pic','qrcode','input']:
            logging.error(u"登录方式输入[%s]不合法,应该为[all,pic,qrcode,input]"%(login_type))
            exit()

        # 识图自动登录
        if login_type.lower() in ['all','pic']:
            login(self.username, self.password)
            if self.check_user():
                return True
        # 二维码登录
        if login_type.lower() in ['all','qrcode']:
            from pro.tools.train_login_qrcode import Train_Login_QrCode
            self.train_login_qrcode = Train_Login_QrCode(session=self.session,cookies=self.cookies)
            self.train_login_qrcode.main()
            if self.check_user():
                return True
        # 手动输入验证码
        if login_type.lower() in ['all','input']:
            from pro.tools.train_login_input import Train_Login
            train_login = Train_Login(session=self.session,cookies=self.cookies)
            train_login.main_login(username=self.username, password=self.password)
            if self.check_user():
                return True
        return False

    ###############
    #### 主函数 调用
    ###############
   
    def main_search(self):
        u""" 查票+乘客信息+下单 """
        self.check_ticket()
        self.check_user()
        # 选择车次
        self.submit_order()
        self.confirm_passenger()
        self.get_passenger_info()
        self.check_order()
        return True
    
    def main_buyticket(self, clickList=None):
        u""" 买票 """
        self.get_queue_count()
        self.confirm_single_for_queue(clickList=None)
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

    def mid_search_service(self):
        u""" 查询12306服务是否正常
        """
        url = 'https://kyfw.12306.cn/otn/leftTicket/log?\
            leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&\
            leftTicketDTO.to_station={}&purpose_codes=ADULT'.format( self.startDate, 
            self.stationCodeDict[self.startStation], self.stationCodeDict[self.endStation]).replace(' ','')
        response = self.session.get( url=url, headers=self.headers, cookies=self.cookies, verify=False)
        dic = json.loads(response.content) or None
        if not dic or not dic['status']:
            logging.debug(dic)
            logging.error(">> 检查12306服务 失败")
            return False
        logging.error(">> 检查12306服务 成功")
        return True

    def mid_search_queryurl(self):
        u""" 生成查询链接
        """
        # 生成查询链接
        # 由于12306查询链接中自带一个随机字母
        query = 'leftTicket/queryA'
        url2 = 'https://kyfw.12306.cn/otn/{}?\
            leftTicketDTO.train_date={}&\
            leftTicketDTO.from_station={}&\
            leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
            query, self.startDate,
            self.stationCodeDict[self.startStation], self.stationCodeDict[self.endStation]).replace(' ', '')

        dic2 = None
        # 拿到正确的链接
        for i in 'ABCDEFGHIJKMNOPQRSTUVWXYZ':
            time.sleep(1)
            url2_mid = url2.replace('queryA',"query"+i)
            logging.debug(url2_mid)

            try:
                response = self.session.get( url=url2_mid, headers=self.headers, cookies=self.cookies, verify=False)
                dic2 = json.loads(response.content)
            except Exception as e:
                pass
                #logging.debug(traceback.print_exc())
                #self.train_base.error_email(">>>> query链接错误,重新尝试");
            if dic2:
                if dic2['status']:
                    logging.debug(dic2)
                    logging.info(">> 查询车票列表 成功")
                    return dic2
        # TODO 所有 status 都是 false ???

        #    # if dic["messages"][0] == u"选择的查询日期不在预售日期范围内":
        #    return "search_error002"
        logging.error(">> 查询车票列表 失败")
        exit()
        return dic2

    def search_ticket(self, firstrun_flag=True):
        u"""
        # log是判断服务是否正常，用queryA进行查询

        :param firstrun_flag:是否是第一次运行

        """
        logging.debug(">>>> 查询是否有票 开始")
        
        if not self.mid_search_service():
            return 

        dic2 = self.mid_search_queryurl()

        # 每次查询前初始化
        self.trainInfoStartTimeList, self.trainInfoEndTimeList, self.trainInfoSecretStrList, self.trainInfoNameList, self.trainInfoLocationList, self.trainInfoNoList = [], [], [], [], [], []
        #:param self.seatTypeList: 所选座位类型
        #:param self.seatTypeList: 所有座位票数情况
        # 二等座,一等座,硬座,软座,硬卧,软卧,动卧,无座,商务座,特等座,高级软卧

        self.seatTypeList = list()
        
        # 车次信息
        self.TicketList = list()
        for a in dic2['data']['result']:
            tmp_dic = {
                u'二等座': ll[30],
                u'一等座': ll[30],
                u'硬座': ll[30],
                u'二等座': ll[30],
                u'二等座': ll[30],
                u'二等座': ll[30],
                u'二等座': ll[30],
                u'二等座': ll[30],
                u'二等座': ll[30],
            }
            ll = a.split('|')

            seatTypeList_name = [
                u'二等座',u'一等座',u'硬座',u'软座', u'硬卧',
                u'软卧',u'动卧',u'无座',u'商务座',u'特等座',
                u'高级软卧']
            row = [
                ll[30],ll[31],ll[29],ll[24],ll[28],
                ll[23],ll[33],ll[26],ll[32],ll[25],
                ll[21],
            ]

            self.seatTypeList.append(row)
            self.trainInfoSecretStrList.append(a.split("|")[0])
            self.trainInfoNoList.append(a.split("|")[2])
            self.trainInfoNameList.append(a.split("|")[3])
            self.trainInfoStartTimeList.append(a.split("|")[8])
            self.trainInfoEndTimeList.append(a.split("|")[9])
            self.trainInfoLocationList.append(a.split("|")[15])

        
        


        return self.trainInfoNameList

    def check_ticket(self):
        u""" 检查是否有票
        """
        logging.info(">>>> 检查是否有票 开始")

        self.search_ticket(firstrun_flag=True)

        have_ticket = False
        count = 0
        while not bool(have_ticket):
            count += 1
            # 刷票机制
            for a in self.trainNameList:
                # 获取 车次在当日所有车次中的 索引index
                if a not in self.trainInfoNameList:
                    logging.error(u"!!! [%s]车次不在可购票的车次中 或当前日期未开始预售 请检查车次信息"%a)
                    return False
                trainIndex = self.trainInfoNameList.index(a)
                # 座位列获取
                for seatType in self.seatTypeList:
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
                    elif self.seatTypeList[b][trainIndex] != u"有" and len(self.passengersList) > int(self.seatTypeList[b][trainIndex]):
                        msg = "票没人多"
                        continue
                    else:
                        have_ticket = True
                        msg = "查询到有票"
                        self.trainIndexOfBuy = trainIndex
                        self.seatIndexOfBuy = b

            # TODO
            infos = str();
            #for train_name in self.trainNameList:
            for seatType in self.seatTypeList:
                for passenger in self.passengersList:
                    info = u">>>> 日期:[%s] 车次:[%s] 座位:[%s] 乘客:[%s] 刷票次数[%s] 原因[%s] <<<< \r"%(self.startDate,self.trainNameList,seatType,passenger,str(count),msg)
                    sys.stdout.write(info)
                    sys.stdout.flush()
                    infos += info + '\n'

            # TODO 进入 12306 错误页面了
            # DEBUG  : "GET /mormhweb/logFiles/error.html HTTP/1.1" 200 2042

            # 没有成功抢到票,重新检索是否有票
            searchResult = self.search_ticket(self.startStation, self.endStation, self.startDate, firstrun_flag=False)

           
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

    def submit_order(self):
        u""" 提交车次订单
        """
        logging.debug(">>>> 提交订单 开始")
        url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        logging.debug(self.trainInfoSecretStrList)
        logging.debug(self.trainIndexOfBuy)
        data = {
                 "secretStr": parse.unquote(self.trainInfoSecretStrList[self.trainIndexOfBuy]),
                 "train_date": self.startDate,
                 "back_train_date": self.startDate,
                 "tour_flag": "dc",
                 "purpose_codes": "ADULT",
                 "query_from_station_name": self.startStation,
                 "query_to_station_name": self.endStation,
                 "undefined": ""
                 }
        response = self.session.post( url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)
        # logging.error(response.content)
        dic = json.loads(response.content)
        print response
        #dic = json.loads(response)

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

    def _post_data(self,url,data,dtype="dic"):
        u" post 获取数据 "
        response = self.session.post( url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)
        if dtype == 'response':
            return response
        dic = json.loads(response.content)
        return dic
        

    def confirm_passenger(self):
        u""" 确认用户信息
        """
        logging.debug('>>>> 确认用户信息 开始')
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        data = {"_json_att": ''}
        response = self._post_data(url,data,dtype='response')

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
            logging.info('>>>> 确认用户信息 失败')
            return 'NetWorkError'

    def check_order(self):
        logging.debug(">>>> 验证订单 开始")

        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        passengerTicketStr = ""
        oldPassengerStr = ""


        try:
            for passenger_name in self.passengersList:
                a = self.passengersList.index(passenger_name)
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
    def get_queue_count(self):
        u""" 获取用户队列 """
        logging.debug(">>>> 获取用户队列 开始")

        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        thatdaydata = datetime.datetime.strptime(self.startDate, "%Y-%m-%d")
        train_date = "{} {} {} {} 00:00:00 GMT+0800 (中国标准时间)".format(thatdaydata.strftime('%a'),
                                                                     thatdaydata.strftime(
                                                                         '%b'), self.startDate.split('-')[2],
                                                                     self.startDate.split('-')[0])
        data = {
            "train_date": train_date,
            "train_no": self.trainInfoNoList[self.trainIndexOfBuy],
            "stationTrainCode": self.trainInfoNameList[self.trainIndexOfBuy],
            "seatType": self.seatCodeList[self.seatIndexOfBuy],
            "fromStationTelecode": self.stationCodeDict[self.startStation],
            "toStationTelecode": self.stationCodeDict[self.endStation],
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

    def confirm_single_for_queue( self, clickList=None):
        u""" 获取单一变量 """
        logging.debug(">>>> 获取单一队列 开始")

        url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        passengerTicketStr = ""
        oldPassengerStr = ""
        # 
        for passenger_name in self.passengersList:
            a = self.passengersList.index(passenger_name)
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
    train=Train12306(
        startStation='北京西', endStation='九江', startDate='2019-01-28',
        #self.trainNameList=[u'Z67'], self.seatTypeList=[u'硬卧'], self.passengersList=[u'朱亚芬']
        trainNameList=[u'Z67'], seatTypeList=[u'硬卧'], passengersList=[u'朱亚芬']
    )
    train.main()
    
    

