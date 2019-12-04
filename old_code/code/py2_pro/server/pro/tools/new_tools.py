#! /usr/bin/python2
#! -*- coding:utf-8 -*-
u"""

一些不常用效果工具
- get_html_encoding 自动识别网页编码
"""





def get_html_encoding(url=None):
    u""" 自动识别网页编码
    :param url: 链接
    """
    if not bool(url):
        url = 'http://www.jd.com/'
    import urllib
    rawdata = urllib.urlopen(url).read()
    import chardet
    data = chardet.detect(rawdata)
    # {'confidence': 0.99, 'encoding': 'utf-8', 'language': ''}
    return data









