#! -*- coding:utf-8 -*-
"""
一些生成器方法，生成随机数，手机号，以及连续数字等

"""
import sys 
reload(sys)
sys.setdefaultencoding('utf8')    

import random
import string
from faker import Factory

fake = Factory().create('zh_CN')


def random_phone_number():
    """随机手机号"""
    return fake.phone_number()

# zipcode ： 邮编
# company ： 公司

def random_name():
    """随机姓名"""
    return fake.name()


def random_address():
    """随机地址"""
    return fake.address()


def random_email():
    """随机email"""
    return fake.email()


def random_ipv4():
    """随机IPV4地址"""
    return fake.ipv4()


def random_str(min_chars=0, max_chars=8):
    """长度在最大值与最小值之间的随机字符串"""
    return fake.pystr(min_chars=min_chars, max_chars=max_chars)


def factory_generate_ids(starting_id=1, increment=1):
    """ 返回一个生成器函数，调用这个函数产生生成器，从starting_id开始，步长为increment。 """
    def generate_started_ids():
        val = starting_id
        local_increment = increment
        while True:
            yield val
            val += local_increment
    return generate_started_ids

 

def factory_choice_generator(values):
    """ 返回一个生成器函数，调用这个函数产生生成器，从给定的list中随机取一项。 """
    def choice_generator():
        my_list = list(values)
        rand = random.Random()
        while True:
            yield random.choice(my_list)
    return choice_generator

def factory_choice_generator(values): 
    # 由于上面性能较差，改为这种。（对应excel输入变更 factory_choice_generator( [u"00",u"01"])().next()  --> factory_choice_generator( [u"00",u"01"]）
    """ 返回一个生成器函数，调用这个函数产生生成器，从给定的list中随机取一项。 """
    my_list = list(values)
    return random.choice(my_list) 




def Gen_length_Num(length):
    def Gen_length_Num_1(length): 
        u"生成流水号 - 纯数字"
        #随机出数字的个数
        numOfNum = length
        #选中numOfNum个数字
        slcNum = [random.choice(string.digits) for i in range(numOfNum)]
        #打乱这个组合
        slcChar = slcNum
        random.shuffle(slcChar)
        #生成密码
        genPwd = ''.join([i for i in slcChar])
        return genPwd
    genPwd = Gen_length_Num_1(length)
    while genPwd[0] == '0' : # 加入循环，避免生成 0 开头的数据。
        genPwd = Gen_length_Num_1(length)
    return genPwd

print Gen_length_Num(13)


from pypinyin import pinyin,lazy_pinyin
def hanzi2pinyin(string,split2=""):
    u"汉字转拼音"
    if not isinstance(string, (unicode)):
        string = unicode(string)
    pinyin_li = lazy_pinyin(string) # 必须为 Unicode
    pinyin = u""
    for i in pinyin_li:
        pinyin += i
    return pinyin
#print hanzi2pinyin(u"中文")
#print hanzi2pinyin("中文")

import requests,time,codecs
def pinyin2hanzi(pinyin="pinyin"):
    u"拼音转汉字"
    base_url = "http://olime.baidu.com/py"
    playload = {
        "input":pinyin,
        "inputtype":"py",
        "bg":0,
        "ed":1,
        "result":"hanzi",
        "resultcoding":"unicode",
        "ch_en":0,
        "clientinfo":"web",
        "version":1
    }
    json_data = requests.get(base_url,params=playload).json()
    return json_data["result"][0][0][0]
#print pinyin2hanzi()


def factory_choice_generator(values):
    """ 返回一个生成器函数，调用这个函数产生生成器，从给定的list中随机取一项。 """
    my_list = list(values)
    #rand = random.Random()
    #while True:
    return random.choice(my_list)

if __name__ == '__main__':
    args = sys.argv
    print args
