# -*- coding=utf-8 -*-

u"""
- dateutil 日期工具
- chardet 字符编码
- feedparser  RSS 订阅
pip install python-dateutil chardet feedparser pillow 
"""
import chardet
def str_encoding_analysis(s):
    u""" 字符编码
    """
    print(chardet.detect('���'))
    print(chardet.detect(b'sad'))
    return chardet.detect(s).get('encoding')

import feedparser
def get_rss_info(url):
    u""" RSS订阅
    RSS资源推荐: https://blog.csdn.net/dll635281462/article/details/51201490
    """
    # TODO 大多RSS不支持
    url = 'https://pypi.org/rss/updates.xml'
    for entry in feedparser.parse(url).entries:
        print entry.title
    return
#! -*- coding:utf-8 -*-

"""
二维码相关处理

"""
from pro.tools.base_import  import *


def url2qrcode(url, filename='a.png'):
    " 链接转二维码图片 "
    import qrcode
    qr=qrcode.QRCode(version = 2,error_correction = qrcode.constants.ERROR_CORRECT_L,box_size=10,border=10,)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    img.show()
    img.save(filename)
    logging.info('>> 链接[%s]转换二维码成功[%s]'%(url,filename))

if __name__ == "__main__":
    pass

