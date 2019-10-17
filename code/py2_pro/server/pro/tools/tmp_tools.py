#! -*- coding:utf-8 -*-
u"""

常用基础工具
- base_check_exists     检测文件或目录是否存在
- base_check_dirfile    检查目录/文件是否存在,不存在则创建

- hanzi2pinyin          汉字转拼音
- hanzi2num             汉字转为九宫格数字
- get_festival          获取交往纪念日

- get_gitbook_md        将单个MD文件转换为gitbook适用的格式
- base_get_filemd5      获取文件MD5值
- get_html_encoding     自动识别网页编码
"""
import sys
import datetime
import logging
from pprint import pprint
reload(sys)
sys.setdefaultencoding('utf-8')

import base_datetime_tools as datetime_tools
import os

#############
#### 基础模块
#############
def base_check_dirfile(name=None,dtype='file'):
    u""" 检查目录/文件是否存在,不存在则创建

    :param name: 目录/文件 名称
    :param dtype: file/dir 指定类型 
    """
    try:
        if dtype.lower() == 'file':
            os.system('mkdir -p %s'%os.path.split(name)[0])
            os.system('touch %s'%os.path.split(name)[1])
        elif dtype.lower() == 'dir':
            os.system('mkdir -p %s'%name)
        else:
            logging.error(">>>> dtype必须在['file','dir']中")
    except Exception as e:
        logging.error(">>>> 创建目录/文件名称不允许为空")
        
    return True

def base_check_exists(path):
    u""" 检测文件或目录是否存在
    :param name: 名称
    """
    return os.path.exists(path)
    
    
    
#############
#### 其他模块
#############
def hanzi2pinyin(string, split2=""):
    u"汉字转拼音"
    from pypinyin import pinyin, lazy_pinyin
    if not isinstance(string, (unicode)):
        string = unicode(string)
    pinyin_li = lazy_pinyin(string)  # 必须为 Unicode
    pinyin = u""
    for i in pinyin_li:
        pinyin += i
    return pinyin


def hanzi2num(astr="汉字",dic=None):
    u""" 汉字转为九宫格数字

    :param astr:输入的汉字
    """
    if not bool(astr): 
        logging.error('未输入汉字')
        return
    if not bool(dic):
        logging.info('> 未输入字典,采用默认字典')
        # 对应表
        dic = {
            '1':'@-_/', '2':'abc', '3':'def', 
            '4':'ghi', '5':'jkl', '6':'mno',
            '7':'pqrs', '8':'tuv', '9':'wxyz',
        }

    # {'a':'2','b':'2'}
    dic_tran = {}
    for k in dic:
        for i in dic[k]:
            dic_tran[i] = k

    pinyin = hanzi2pinyin(astr)
    anum = str()
    for i in pinyin:
        ni = i if not dic_tran.get(i) else dic_tran.get(i)
        anum += ni
    print(">> 汉字[%s]转为九宫格数字[%s]成功"%(astr,anum))
    return anum
        

def get_festival(startdt='2018-04-06',days=[]):
    u""" 获取交往纪念日

    :param startdt: 开始日期
    :param days: 纪念天数

    return festival_dic: {开始日期:纪念日}
    """
    if not bool(days): 
        logging.info(u"!!!! 未输入纪念天数,采用默认天数")
        days=[
            # 77
            0,77,177,277,377,477,
            # 百天 
            100,100*2,100*3,100*4,
            # 年份
            365,365*2,365*3,
            ]

    festival_dic = dict()
    for day in days:
        festivaldt = datetime_tools.date2str(datetime_tools.str2date(startdt) + datetime.timedelta(day))
        festival_dic[day] = festivaldt
    pprint(festival_dic)
    return festival_dic

def get_gitbook_md(file_path=None, ouput_dir=None):
    u""" 将 单个MD 文件转换为 gitbook 适用的格式
    """
    # gitbook-convert 可用

    if not bool(file_path) or not bool(base_check_exists(file_path)):
        logging.error(u'>>>> 文件名称[%s]不存在'%file_path)
    with open(file_path) as f:
        rows = f.readlines()

    print rows
    for row in rows:
        
        print row
        print type(row)

        if row:
            pass


#############
#### 计算 文件MD5值
#############
import hashlib
import os
import datetime
def base_get_filemd5(filename):
    u""" 计算文件md5值
    """
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

class Dict(dict):
    u"""
        属性访问字典

    Examples:
        d = Dict(a=1, b=2)
        d['a'] = 1
        d.a = 1
    """
    def __init__(self, **kw):
        super(Dict, self).__init__(**kw)
 
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
 
    def __setattr__(self, key, value):
        self[key] = value

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









    
    

if __name__ == '__main__':
   # print(u"输入的参数: %s"%sys.argv)
   # # 汉字装为九宫格数字
   # hanzi2num(astr="我爱你")
   # # 获取交往纪念日
   # get_festival('2018-04-06')
   # get_festival('2018-08-17')
   # # MD文件转换
   # get_gitbook_md(file_path='test.md', ouput_dir=None)
   # 
    filepath = raw_input('请输入文件路径：')
    print base_get_filemd5(filepath)
