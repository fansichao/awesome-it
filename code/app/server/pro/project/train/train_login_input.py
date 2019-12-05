#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
@Author: Scfan
@Date: 2018-12-06 15:03:37
@LastEditors: Scfan
@LastEditTime: 2018-12-25 20:35:45
@Description: 工作&amp;学习&amp;生活
@Email: 643566992@qq.com
@Company: 上海
@version: V1.0
  12306 登录 手动输入
''' 
from __future__ import unicode_literals
from pro.tools.base_import import *

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from PIL import Image

from pro.tools.base_import import *
from .train_login_pic import RecoginitionContainer
from .baidu_shitu_tools import BaiDu
from ..base.settings import Config
    
from ..base.settings import Config
from .tools_email import Email_Post
from .train_base import Train_Base



class Train_Login():

    u"""
    - 用户登录
        - main_login            用户登录函数入口
        - get_verification_code     获取图片验证码
        - check_verification_code   验证图片验证码
        - login
            - login_web             网络登录
            - login_uamtk
            - login_newapptk
    """

    ###############
    # 登录模块
    ###############
    def __init__(self, *lis, **kv):
        # 回话链接
        print kv
        self.session = kv.get('session') if bool(kv.get('session')) else requests.session() 
        self.cookies = kv.get('cookies') if bool(kv.get('cookies')) else self.session.cookies 

        self.img_filepath = os.path.join(Config.TMP_PATH, 'code.png')

        self.start_datetime = datetime.datetime.now()
        # 实例化
        self.email_ins = Email_Post()
        self.train_base = Train_Base()
        # 用户密码
        self.username = Config.train_username
        self.password = Config.train_password
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

        pass

    def main_login(self, username, password, auto=False):
        u""" 用户登录 """
        self.get_verification_code()
        get_picture_code = RecoginitionContainer(Config.TMP_PATH)

        if auto:
            codeList = get_picture_code.get_text(self.img_filepath)
        else:
            clickList = raw_input('>>>> 输入验证码[5,8]:').split(',')
            codeList = self.tran_verification_code(clickList)

        self.check_verification_code(codeList)
        self.login(username, password)
        return True

    def get_verification_code(self):
        u""" 获取图片验证码

        """
        url = "https://kyfw.12306.cn/passport/captcha/captcha-image?\
            login_site=E&module=login&rand=sjrand&{}".format(random.random())
        url = url.replace(' ', '')
        response = self.session.get(url=url, headers=self.headers,
                                    cookies=self.cookies, verify=False)
        if os.path.exists(self.img_filepath):
            os.system('rm -f %s' % self.img_filepath)
        with open(self.img_filepath, 'wb') as f:
            f.write(response.content)
        return True

    def tran_verification_code(self, clickList):
        u""" 将输入的数字 转换为坐标轴
        """
        #=======================================================================
        # 根据打开的图片识别验证码后手动输入,输入正确验证码对应的位置,例如：2,5
        # ---------------------------------------
        #         |         |         |
        #    1    |    2    |    3    |     4
        #         |         |         |
        # ---------------------------------------
        #         |         |         |
        #    5    |    6    |    7    |     8
        #         |         |         |
        # ---------------------------------------
        #=======================================================================
        verifyList = []
        for a in clickList:
            verifyList.append(self.code[int(a)])
        codeList = ','.join(verifyList)
        return codeList

    def check_verification_code(self, codeList):
        u""" 验证图片验证码
        """
        logging.debug(">>>> 验证图片验证码 开始")
        try:
            url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
            data = {
                'answer': codeList,
                'login_site': 'E',
                'rand': 'sjrand',
                '_json_att': "",
            }
            response = self.session.post(url=url, data=data,
                                         headers=self.headers, cookies=self.cookies, verify=False)
            dic = json.loads(response.content)

            logging.debug(">> 返回值[%s,%s]" %
                          (dic['result_code'], dic['result_message']))
            if str(dic['result_code']) == "4":
                logging.debug(">>>> 验证图片验证码 成功")
            else:
                logging.debug(">>>> 验证图片验证码 失败")
        except Exception as e:
            self.train_base.error_email(">>>> 验证图片验证码 失败")
            logging.debug(">>>> 验证图片验证码 失败")
        return True

    def login(self, account, password):
        u""" 用户登录
        """
        logging.debug(">>>> 用户登录 开始")
        dic = self.login_web(account, password)
        dic2 = self.login_uamtk(account, password, dic)
        self.login_newapptk(account, password, dic2)
        logging.debug(">>>> 用户登录 成功")
        return True

    def login_web(self, account, password):
        u""" 用户登录A - web登录 """
        logging.debug(">>> 用户登录web 开始")
        url = 'https://kyfw.12306.cn/passport/web/login'
        data = {
            'username': account,
            'password': password,
            'appid': 'otn',
            '_json_att': "",
        }
        response = self.session.post(
            url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)
        dic = json.loads(response.content)
        resultCode = dic['result_code']
        resultMsg = dic['result_message']
        self.loginInfo = resultMsg
        if resultCode == 0:
            logging.debug(">>> 用户登录web 成功")
        else:
            logging.debug(">>> 用户登录web 失败")
            return "loginFail"
        return dic

    def login_uamtk(self, account, password, dic):
        u""" 用户登录B - uamtk验证 """
        logging.debug(">>> 用户登录验证uamtk 开始")
        try:
            if 'uamtk' in dic.keys():
                self.uamtk = dic['uamtk']

            url2 = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
            data2 = {
                "appid": "otn",
                '_json_att': ""
            }
            # self.cookies['uamtk'] = self.uamtk
            response2 = self.session.post(
                url=url2, data=data2, headers=self.headers, cookies=self.cookies, verify=False)

            dic2 = json.loads(response2.content)
            resultCode2 = dic['result_code']
            resultMsg2 = dic['result_message']
            self.loginInfo = resultMsg2
            if resultCode2 == 0:
                logging.debug(">>> 用户登录验证uamtk 成功")
            else:
                logging.debug(">>> 用户登录验证uamtk 失败")
        except Exception as e:
            self.train_base.error_email(">>>> 手动输入验证码失败,重新开始")
            logging.debug("手动输入验证码失败,重新开始")
            return "authFail"
        return dic2

    def login_newapptk(self, account, password, dic2):
        u""" 用户登录C - newapptk验证 """
        logging.debug(">>> 用户登录验证newapptk 开始")
        if 'newapptk' in dic2.keys():
            self.tk = dic2["newapptk"]
            # self.cookies.pop('uamtk')
            # self.cookies['tk'] = self.tk

        url3 = 'https://kyfw.12306.cn/otn/uamauthclient'
        data3 = {"tk": self.tk,
                 '_json_att': "",
                 }
        response3 = self.session.post(
            url=url3, data=data3, headers=self.headers, cookies=self.cookies, verify=False)
        dic3 = json.loads(response3.content)
        resultCode3 = dic3['result_code']
        resultMsg3 = dic3['result_message']
        self.loginInfo = resultMsg3
        if resultCode3 == 0:
            logging.debug(">>> 用户登录验证newapptk 成功")
            return "LoginSuccessful"
        else:
            logging.debug(">>> 用户登录验证newapptk 失败")
            return False
    
    def main_input(self,**dic):
        u""" 程序入口

        """
        import getpass
        # 用户登录
        username = raw_input(u'@请输入用户名称:')
        password = raw_input(u'@请输入用户密码:')
        #password = getpass.getpass(u'@请输入用户密码:')
        # 站点日期
        startStation = raw_input(u'@请输入出发车站:')
        endStation = raw_input(u'@请输入到达车站:')
        startDate = raw_input(u'@请输入出发日期[2018-10-01]:')
        # 自动订票
        trainNameList = raw_input(u'@请输入车次[G34,G23]:').split(',')
        logging.info(u'说明: 可选座位类型如下[%s] '%(",".join(self.seatTypeDict.values())))
        seatTypeList = raw_input(u'@请输入座位[二等座,一等座]:').split(',')
        logging.info(u'说明: 乘车人姓名/身份证/电话必须已经存在于账号中')
        passengersList = raw_input(u'@请输入乘车人姓名[甲,乙]:').split(',')
    
        self.main_code(
            username=username,password=password,
            startStation=startStation,endStation=endStation,
            trainNameList=trainNameList,seatTypeList=seatTypeList,passengersList=passengersList
        )



