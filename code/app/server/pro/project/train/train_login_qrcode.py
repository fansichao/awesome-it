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
  12306 二维码登录接口
''' 
from __future__ import unicode_literals

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from PIL import Image

from pro.tools.base_import import *
from .train_login_pic import RecoginitionContainer
from .baidu_shitu_tools import BaiDu
from ..base.settings import Config

class Train_Login_QrCode():
    '''
    12306 二维码 登录 
        登录步骤:
          1. create-qr64 获取二维码
          2. checkqr 轮询检查是否扫码登录
        登录二维码url样例：
          https://mobile.12306.cn/otsmobile/h5/otsbussiness/downloadapp/downloadapp.html?loginUUID=
            5XSRku-TJJDYHAGHfew4KO-eeKRJJ0FbsPLuqJhSIFlehjLvwxegERn-SS3u1mZvSPqwyWaCO6O0zi2
        参考链接：
          1. 二维码扫描登录原理: https://blog.csdn.net/zhang_zhenwei/article/details/80847473
          2. 草料二维码扫描器(根据二维码生成url): https://cli.im/deqr
    '''

    def __init__(self, *lis, **kv):

        self.qrcode_png = "a.png"
        # 每次请求 网页唯一ID
        self.uuid = None
        # 二维码链接
        self.qrcode_href = None

        print kv
        self.session = kv.get('session') if bool(kv.get('session')) else requests.session() 
        self.cookies = kv.get('cookies') if bool(kv.get('cookies')) else self.session.cookies 
        
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://kyfw.12306.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4355.400 QQBrowser/9.7.12672.400',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
        }

    def login_pre_index(self):
        u" 获取首页 - 废弃 "
        url = "https://exservice.12306.cn/excater/index.html"
        response = self.session.get(url=url, headers=self.headers,
                                    cookies=self.cookies, verify=False)

    def login_pre_conf(self):
        u" 登录前检查 配置 - 废弃 "
        url = "https://exservice.12306.cn/excater/login/conf"
        data = {}
        response = self.session.post(url=url, data=data, cookies=self.cookies,
                                     headers=self.headers, verify=False)

    def login_pre_check_uamtk(self):
        u" 登录前检查 uamtk - 废弃 "
        url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
        data = {
            "appid": "otn",
            '_json_att': ""
        }
        response = self.session.post(
            url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)

    def login_pre_check(self):
        u" 登录前检查 是否登录 - 废弃 "
        url = "https://exservice.12306.cn/excater/login/checkLogin"
        data = {}
        response = self.session.post(
            url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)

    def get_QrCode(self):
        '''
            获取二维码
        @param 

        '''
        # 生成二维码
        url = "https://kyfw.12306.cn/passport/web/create-qr64"
        data = {'appid': "otn"}

        response = self.session.post(
            url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)
        response_content = response.json()
        # 返回消息样例 {"result_message":"生成二维码成功","result_code":"0","image":"iVBORw0KGgxxxxxxxxxx"}
        # 二维码路径 "data:image/jpg;base64," + response["image"]
        # 链接只可访问一次 第二次失效
        if response_content['result_message'] == '生成二维码成功':
            QrCode_href = "http://data:image/jpg;base64,%s" % response_content["image"]
            logging.info(">>>> 生成二维码成功!!!")
        else:
            self.error = True
            logging.info(">>>> 生成二维码失败!!!")

        self.uuid = response_content['uuid']
        self.qrcode_href = "https://mobile.12306.cn/otsmobile/h5/otsbussiness/downloadapp/downloadapp.html?loginUUID=%s" % self.uuid
        self.qrcode_tran()

    def qrcode_tran(self):
        " 链接转二维码图片 "
        from pro.tools.image_qrcode import url2qrcode
        url2qrcode(self.qrcode_href, filename=self.qrcode_png)
        # TODO 图片转像素

    def check_qrcode(self):
        u" 二维码登录检查 "
        while True:
            data = {
                'uuid': self.uuid,
                'appid':  'otn'
            }
            url = "https://kyfw.12306.cn/passport/web/checkqr"
            response = self.session.post(
                url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)
            # {"result_code":0,"result_message":"二维码状态查询成功"}
            # {"result_code":1,"result_message":"二维码状态查询成功"}
            # {"result_code":2,"result_message":"扫码登录成功",umatk:"5MbpAD67wvTx1UeGNR8e9wv-SPsdPHaq1Tqws6OM9QMgaf1f0"}
            # {"result_code":3,"result_message":"二维码已过期"}
            response_content = response.json()
            logging.debug(response_content)
            if response_content['result_code'] in ["0", "1"]:
                logging.info(">>>>>>>> 请扫码登录 <<<<<<<<<<")
            elif response_content['result_code'] == "2":
                logging.info(">>>>>>>> 扫码登录成功 <<<<<<<<<<")
                return True, response_content['uamtk']
            else:
                logging.info(">>>>>>>> 二维码已过期 <<<<<<<<<<")
                self.main()
            time.sleep(1)

    def check_uamtk(self):
        u" 检查 uamtk "
        url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
        data = {"appid": "excater", "umatk": self.check_qrcode()[1]}
        response = self.session.post(
            url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)
        response_content = response.json()
        if response_content['result_code'] == "1":  # 用户未登录
            return
        logging.debug(response.content)
        newapptk = response_content.get('newapptk')
        return newapptk

    def check_uamauthclient(self):
        u" 检查用户信息 "
        url = "https://exservice.12306.cn/excater/uamauthclient"
        data = {
            'tk': self.check_uamtk()
        }
        response = self.session.post(
            url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)
        response_content = response.json()
        logging.debug(response_content)
        #{"result_code":"4","result_message":"用户已在他处登录"}
        #{"result_code":"2","result_message":"uamtk票据内容为空"}
        #{"result_code":"0","result_message":"验证通过}
        if response_content['result_code'] == '0':
            return True
        return False

    def check_login(self):
        u" 检查登录是否成功 "
        url = "https://exservice.12306.cn/excater/login/checkLogin"
        data = {}
        response = self.session.post(
            url=url, data=data, headers=self.headers, cookies=self.cookies, verify=False)
        response_content = response.json()
        msg = ">> 登录姓名:[%s],手机号:[%s]"%(response_content['data'].get('name'),response_content['data'].get('mobile'))
        logging.debug(response_content)
        logging.info(msg)
        if response_content['data']['flag'] == 1:
            return True
        return False

    def main(self, simple_check=False):
        '''
            入口函数
        @param simple_check: 是否简单检查
        '''
        # 获取登录二维码
        self.get_QrCode()
        if bool(simple_check):
            # 检查二维码是否扫描成功
            self.check_qrcode()
        else:
            # 检查登录是否成功
            self.check_uamauthclient()
            self.check_login()

if __name__ == "__main__":
    train_login = Train_Login_QrCode()
    train_login.main()
