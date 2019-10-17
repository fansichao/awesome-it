#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
利用百度图像识别api做文字识别，目的是为了做12306的图片校验。

百度API图像识别 注册&使用
参考链接
- https://blog.csdn.net/qq_21165007/article/details/82707918

"""
import os
from aip import AipOcr

class Baidu_Tools(object):
    u"""
        BaiDu Api 封装使用
    """

    def __init__(self, *args, **kwargs):
        # 已有付费账号
        default_dic = {
            'APP_ID': '10508877',
            'API_KEY': 'kpFtUgtOaxmKkNa2C0x7Q7mN',
            'SECRET_KEY': 'TTX5ginIXZyfGtdH8UTO4kF5M41lf3fb'
        }
        APP_ID = os.environ['baidu_appid'] or default_dic['APP_ID']
        API_KEY = os.environ['baidu_api_key'] or default_dic['API_KEY']
        SECRET_KEY = os.environ['baidu_secret_key'] or default_dic['SECRET_KEY']

        # 初始化AipFace对象
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    def get_file_content(self, file_path):
        """获取图片数据"""
        with open(file_path, 'rb') as fp:
            return fp.read()

    def get_result(self, image_url):
        """
            识别结果
        :return:  返回识别结果
        """
        # 定义参数变量
        options = {
            'detect_direction': 'true',
            'language_type': 'CHN_ENG',
        }

        image = self.get_file_content(image_url)
        return self.client.basicGeneral(image, options)


if __name__ == "__main__":
    # 获取图片
    baidu = BaiDu()
    # 得到识别结果
    result = baidu.get_result("../tmp/code.png")
    # 输出识别结果
    print(result)
    print(result['words_result'][0]['words'])
