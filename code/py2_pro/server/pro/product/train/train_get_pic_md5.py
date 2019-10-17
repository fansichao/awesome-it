#! /usr/bin/python2
# -*- coding:utf-8 -*-
u"""
12306图片验证码 MD5-标签
1. 海量获取 图片 - 标签
2. 算法处理 将图片 - 标签一一对应 
    1. md5图片, 增加标签 1/8 概率
    2. md5图片，累计同一标签，概率。
    3. 当某项标签概率远超其他人，则说明此图片和标签绑定

涉及问题
1.图片切割问题
2.海量获取的反爬虫机制

"""
import os
import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from PIL import Image
import pandas as pd

from fdm.module.scrapy import scrapy_proxy
from fdm.base.settings import Config
from fdm.tools.base_tools import base_get_filemd5

headers = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

session = requests.session()


# 设置 代理服务器
scrapy_proxy.get_proxy_main()
session = scrapy_proxy.use_proxy().get('session')

def get_picture(get_pic_url, image_code):
    response = session.get(get_pic_url, headers=headers, verify=False)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        with open(image_code, "wb") as f:
            f.write(response.content)
            print("图片下载成功,地址[%s]"%image_code)
        return True
    else:
        print("图片下载失败，正在重试....")
        get_picture(get_pic_url, image_code)

def get_title_pic(img_url, img_title, time):
    u" 获取 image中 文字图片"
    # 读取图片
    if time == 1:
        box = (116, 0, 175, 30)
    else:
        box = (175, 0, 238, 30)
    image = Image.open(img_url)
    image.convert("L")
    t = image.crop(box)
    t.save(img_title)
    t.close()

def get_title_context(image_code, image_title):
    """
    两次识别文字标题
    :param image_code:
    :param image_title:
    :return:
    """
    from .baidu_shitu_tools import BaiDu
    # 标题内容
    result = list()
    #print("调用百度API进行标题识别:")
    for index in range(1, 3):
        try:
            get_title_pic(image_code, image_title, index)
        except:
            continue
        try:
            baidu = BaiDu()
            res = baidu.get_result(image_title)
            #print("标题识别返回原始数据")
            #print(res)
            if len(res['words_result']) != 0:
                result.append(res['words_result'][0]['words'])
        except Exception:
            import  traceback
            import time
            print(traceback.print_exc())
            print("出现识别异常，正在重试!")
            get_title_context(image_code, image_title)
            time.sleep(10)

    return result

def main(csv_file='test.csv',num=10000,timeout=2):
    u" 循环获取数据 "
    get_pic_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.6523880813900003' ;
    image_title = os.path.join(Config.TMP_PATH,'temp_title.png')    
    image_code = os.path.join(Config.TMP_PATH,'code.png')   
    rows = []

    for i in range(num):
        now_time = str(datetime.datetime.now()).replace(' ','').replace('-','').replace(':','')[0:14]
        image_path = image_code.replace('code.png','code_%s.png'%now_time)
        image_title_path = image_title.replace('temp_title.png','temp_title_%s.png'%now_time)
        # 运行
        get_picture(get_pic_url, image_path)
        time.sleep(1)
        result = get_title_context(image_path, image_title_path)
        time.sleep(1)

        # 获取 图片路径+文字名称
        if bool(('|').join(result)) and ',' not in ('|').join(result):
            # 切割图片
            img_paths = pic_split(pic_path=image_path)
            for img_path in img_paths:
                # 获取切割后 图片路径+md5值
                img_path_md5 = base_get_filemd5(img_path)
                row = [('|').join(result) , image_path, img_path, img_path_md5]
                rows.append(row)
        
        #print('等待时间[%s]'%timeout)
        time.sleep(timeout)

        if i % 10 == 0:
            df = pd.DataFrame(rows,columns=['words','image_code','img_code','img_code_md5'])
            df.to_csv(csv_file, mode='a', header=False,  index=False)
            rows = []
            print i
    # 追加数据
    df = pd.DataFrame(rows,columns=['words','image_code','img_code','img_code_md5'])
    df.to_csv(csv_file, mode='a', header=False,  index=False)
    return 

def pic_split(pic_path=None):
    u" 图片切割 "
    im = Image.open(pic_path)
    img_paths = []
    def save_pic(id,xy):
        img_path = pic_path + "_%d.png"%id
        # x1,y1,x2,y2
        img = im.crop(xy)
        img.save(img_path)
        img_paths.append(img_path)
        img.close()
        
    id=1;xy=(5  ,41 ,72 ,108);save_pic(id,xy)
    id=2;xy=(77 ,41 ,144,108);save_pic(id,xy)
    id=3;xy=(149,41 ,216,106);save_pic(id,xy)
    id=4;xy=(221,41 ,288,106);save_pic(id,xy)
    id=5;xy=(5  ,113,72 ,180);save_pic(id,xy)
    id=6;xy=(77 ,113,144,180);save_pic(id,xy)
    id=7;xy=(149,113,216,180);save_pic(id,xy)
    id=8;xy=(222,113,288,180);save_pic(id,xy)
    #print('图片切割成功')
    return img_paths


if __name__ == '__main__':

    main()
