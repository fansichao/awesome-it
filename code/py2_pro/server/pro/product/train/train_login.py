#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Author: Scfan
@Date: 2018-12-06 15:03:37
@LastEditors: Scfan
@LastEditTime: 2018-12-24 18:35:22
@Description: 工作&amp;学习&amp;生活
@Email: 643566992@qq.com
@Company: 上海
@version: V1.0
@Msg:
    12306登录接口，获取到了验证码标题的内容
'''
from __future__ import unicode_literals
import logging
import traceback

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from PIL import Image

from pro.tools.base_import  import *
from .train_login_pic import RecoginitionContainer
from .baidu_shitu_tools import BaiDu
from ..base.settings import Config

headers = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }

req = requests.session()


def get_title_pic(img_url, img_title, time):
    # 读取图片
    if time == 1:
        box = (116, 0, 175, 30)
    else:
        box = (175, 0, 238, 30)
    image = Image.open(img_url)
    image.convert("L")
    t = image.crop(box)
    t.save(img_title)

def get_picture(get_pic_url, image_path):
    # 读取图片
    response = req.get(get_pic_url, headers=headers, verify=False)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        with open(image_path, "wb") as f:
            f.write(response.content)
            logging.debug("图片下载成功")
    else:
        logging.debug("图片下载失败，正在重试....")
        get_picture(get_pic_url, image_path)
    return True


def del_file(path):

    os.system("rm -f %s" % os.path.join(Config.TMP_PATH, 'temp_title.png'))
    os.system("rm -f %s" % os.path.join(Config.TMP_PATH, 'code.png'))
    os.system("rm -f %s" % os.path.join(Config.TMP_PATH, 'query*.png'))

    return
    for i in os.listdir(path):
        # 取文件绝对路径
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            del_file(path_file)


def get_title_context(image_code, image_title):
    """
    两次识别文字标题
    :param image_code:
    :param image_title:
    :return:
    """
    # 标题内容
    result = list()
    logging.debug("调用百度API进行标题识别:")
    for index in range(1, 3):
        get_title_pic(image_code, image_title, index)
        try:
            baidu = BaiDu()
            res = baidu.get_result(image_title)
            logging.debug("标题识别返回原始数据")
            logging.debug(res)
            if len(res['words_result']) != 0:
                result.append(res['words_result'][0]['words'])
        except Exception:
            import traceback
            import time
            logging.debug(traceback.logging.debug_exc())
            logging.debug("出现识别异常，正在重试!")
            get_title_context(image_code, image_title)
            time.sleep(10)

    return result


def login_get_data(url, image_code, image_title):
    # 删除images所有文件
    del_file(Config.TMP_PATH)
    get_picture(url, image_code)

    # 由于验证码难度升级，成了两个东西，比如：本子，订书机这种形式，那么
    # 我需要进行两次分割，并进行循环判断才可以
    point = list()
    result = get_title_context(image_code, image_title)
    if len(result) == 0:
        logging.debug("识别标题失败,正在重新尝试....")
        login_get_data(url, image_code, image_title)
    else:
        logging.debug("标题识别结果：")
        logging.debug(result)

        # 对图片内容进行识别
        pass
    logging.debug("开始对图片内容进行识别....")
    c = RecoginitionContainer(Config.TMP_PATH)
    # 得到了坐标和识别出来的内容，或者相似图片的标题
    lists = c.get_text(image_code)
    # 进行内容比对
    logging.debug("正在进行内容比对......")
    for li in lists:
        # 得到每一个坐标点和内容
        # 循环标题，进行比对
        for title_text in result:
            for po, value in li.items():
                if title_text in value:
                    # 判断当前坐标点是否存在
                    if po not in point:
                        logging.debug("识别出一个坐标点")
                        point.append(po)
            # 再次对标题进行分割
            for tx in title_text:
                for po, value in li.items():
                    if tx in value:
                        # 判断当前坐标点是否存在
                        if po not in point:
                            logging.debug("识别出一个坐标点")
                            point.append(po)
    # 打印出图片的内容
    logging.debug(point)
    return point


def check_captcha(point):
    # 验证码地址
    check_url = "https://kyfw.12306.cn/passport/captcha/captcha-check"
    data = {
        "answer": ",".join(point),
        "login_site": "E",
        "rand": "sjrand"
    }
    response = req.post(check_url, data=data,
                        headers=headers, verify=False)
    logging.debug(response.text)
    if response.status_code != 200:
        return False
    code = response.json()['result_code']
    # 取出验证结果，4：成功  5：验证失败  7：过期
    if str(code) == '4':
        return True
    else:
        return False


def login(username, password):
    ''' 用户登录 12306
    @param username: 用户名称
    @param password: 用户密码
    '''
    url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.6523880813900003"
    image_title = os.path.join(Config.TMP_PATH, 'temp_title.png')
    image_code = os.path.join(Config.TMP_PATH, 'code.png')
    point = login_get_data(url, image_code, image_title)
    if len(point) != 0:
        # 进行登录操作
        logging.debug("进行尝试登录....")
        check = check_captcha(point)
        if check is True:
            logging.debug("验证码验证成功......")
            loginUrl = "https://kyfw.12306.cn/passport/web/login"
            data = {
                'username': username,
                'password': password,
                'appid': 'otn'
            }
            result = req.post(url=loginUrl, data=data,
                              headers=headers, verify=False)
            logging.debug("登录返回结果:")
            logging.debug(result.text)
        else:
            logging.debug("验证码验证失败，正在重新尝试....")
            login(username, password)
    else:
        # 再次调用识别
        logging.debug("未能成功识别图片内容，正在重试.....")
        login(username, password)

    return True


from .tools_email import Email_Post


if __name__ == "__main__":

    exit()
    login()
    A01 = raw_input('Y/N 使用默认用户密码?')
    if A01.upper() == 'Y':
        username = os.environ['train_username']
        password = os.environ['train_password']
    else:
        username = raw_input('请输入用户名称:')
        password = raw_input('请输入用户名称:')

    try:
        #login(username, password)
        get_picture()
    except Exception as e:
        logging.error(traceback.print_exc())
        logging.error('>>>> 请检查输入的用户名[%s]密码[%s]' % (username, password))


