# Python-Faker 使用文档

[toc]

tags: faker 随机 虚拟 造数

Faker是一个Python包，可以为您生成虚假数据。无论您是需要引导数据库，创建外观漂亮的XML文档，填写持久性来对其进行压力测试，还是匿名化从生产服务中获取的数据，Faker都适合您。

## 安装

安装**faker**

```bash
pip install Faker
(env) [scfan@WOM ~]$ faker -h
```

faker官方文档链接:[https://faker.readthedocs.io/en/latest/index.html)](https://faker.readthedocs.io/en/latest/index.html)
faker函数列表参考:
https://www.jianshu.com/p/6bd6869631d9


## 官网函数样例

官网的一些函数样例

## Faker 常用函数

导入模块

```python
from faker import Factory
fake = Factory().create('zh_CN')
```

常用函数

```python
# 实例化对象
In [2]: from faker import Factory
In [3]: fake = Factory().create('zh_CN')
# 身份证号码
In [6]: print(fake.ssn())
41012219881129736X
# 姓名 & 女性姓名 & 男性姓名
In [7]: print fake.name(), fake.name_female(), fake.name_male()
帅秀珍 须金凤 姬健

# 国家 & 国家代码
In [41]: print fake.country() ,fake.country_code()
匈牙利 US
# 省份
In [15]: print(fake.province())
辽宁省
# 城市 & 城市名称 & 城市后缀
In [42]: print fake.city(), fake.city_name(), fake.city_suffix()
张家港市 深圳 县
# 电话号码 & 电话号码前缀
In [47]: print fake.phone_number(), fake.phonenumber_prefix()
18074673371 157
# Email
In [14]: print(fake.email())
tao82@liao.cn
# 公司名称
In [72]: print fake.company()
中建创业传媒有限公司
# 地址
In [94]: print fake.address()
云南省峰县房山正街b座 190919
# 街道地址 & 街道名称 & 街道后缀
In [93]: print fake.street_address(), fake.street_name(), fake.street_suffix()
经路T座 合山路 路
```

## Faker 封装函数

如下主要说明一些常用/基础函数(已封装)

1. factory_choice_generator 随机生成list中一项
2. Gen_length_Num 随机生成指定长度数字
3. hanzi2pinyin 汉字转拼音
4. fake_random_sentence 传入list，生成随机组合的list

```python
import datetime
import logging
import random, string

from pypinyin import pinyin, lazy_pinyin
from faker import Factory
fake = Factory().create('zh_CN')

def factory_choice_generator(values):
    u"""从list中随机选择一个输出

    :param values:列表
    :return:随机取一返回
    """
    my_list = list(values)
    return random.choice(my_list)

def Gen_length_Num(length):
    u"""输入指定长度，生成长度固定的随机数，且开头不为0

    :param length:长度
    :return:长度固定的随机数，且开头不为0
    """
    def Gen_length_Num_1(length):
        u"生成流水号 - 纯数字"
        # 随机出数字的个数
        numOfNum = length
        # 选中numOfNum个数字
        slcNum = [random.choice(string.digits) for i in range(numOfNum)]
        # 打乱这个组合
        slcChar = slcNum
        random.shuffle(slcChar)
        # 生成密码
        genPwd = ''.join([i for i in slcChar])
        return genPwd

    genPwd = Gen_length_Num_1(length)
    while genPwd[0] == '0':  # 加入循环，避免生成 0 开头的数据。
        genPwd = Gen_length_Num_1(length)
    return genPwd

def hanzi2pinyin(string, split2=""):
    u"汉字转拼音"
    if not isinstance(string, (unicode)):
        string = unicode(string)
    pinyin_li = lazy_pinyin(string)  # 必须为 Unicode
    pinyin = u""
    for i in pinyin_li:
        pinyin += i
    return pinyin

def fake_random_sentence(ext_word_list=None):
    u" 传入list随机组合生成列表 "
    my_word_list = [
    'danish','cheesecake','sugar',
    'Lollipop','wafer','Gummies',
    'sesame','Jelly','beans',
    'pie','bar','Ice','oat' ]
    fake.sentence()
    # 'Expedita at beatae voluptatibus nulla omnis.'
    sentence = fake.sentence(ext_word_list=my_word_list)
    # 'Oat beans oat Lollipop bar cheesecake.'
    return sentence
```

## Faker 函数效果一览

生成**函数样例**的代码程序

```python
# -*- coding=utf-8 -*-
import sys
from faker import Factory
reload(sys)
sys.setdefaultencoding('utf8')

fake = Factory().create('zh_CN')
li =  dir(fake)
def get_dir_run():
    with open('somefile.txt', 'wt') as f:
        for i in li:
            a = None
            try:
                cmd = "fake."+i+"()"
                a = eval(cmd)
                print cmd
            except Exception:
                a = None
            if a:
                message = "{0}   # {1} \n".format(cmd,a)
                f.write(message)
get_dir_run()
```

Python-Faker详细**函数样例**

```python
fake.__class__()   # <faker.generator.Generator object at 0x7ff780c23e10>
fake.__hash__()   # 8793824177497
fake.__repr__()   # <faker.generator.Generator object at 0x7ff78c42d590>
fake.__sizeof__()   # 32
fake.__str__()   # <faker.generator.Generator object at 0x7ff78c42d590>
fake.__subclasshook__()   # NotImplemented
fake.address()   # 云南省荣县白云延路y座 648847
fake.am_pm()   # AM
fake.ascii_company_email()   # zhangchao@mao.com
fake.ascii_email()   # yongzheng@hotmail.com
fake.ascii_free_email()   # gongfang@hotmail.com
fake.ascii_safe_email()   # tzhao@example.net
fake.boolean()   # True
fake.bothify()   # 10 Nq
fake.bs()   # productize front-end supply-chains
fake.building_number()   # E座
fake.catch_phrase()   # Visionary logistical initiative
fake.century()   # II
fake.chrome()   # Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_8_9) AppleWebKit/5352 (KHTML, like Gecko) Chrome/14.0.828.0 Safari/5352
fake.city()   # 成都市
fake.city_name()   # 宁德
fake.city_suffix()   # 市
fake.color_name()   # DarkOliveGreen
fake.company()   # 网新恒天信息有限公司
fake.company_email()   # xiongchao@cai.com
fake.company_prefix()   # 维旺明
fake.company_suffix()   # 信息有限公司
fake.country()   # 阿拉伯联合酋长国
fake.country_code()   # ES
fake.credit_card_expire()   # 06/22
fake.credit_card_full()   # JCB 16 digit
柳 冉
3096337563919187 07/23
CVC: 610

fake.credit_card_number()   # 6011172478902092
fake.credit_card_provider()   # Voyager
fake.credit_card_security_code()   # 0753
fake.cryptocurrency_code()   # XDN
fake.currency_code()   # TWD
fake.date()   # 1973-07-31
fake.date_between()   # 2008-01-12
fake.date_between_dates()   # 2017-12-06
fake.date_object()   # 1972-08-01
fake.date_this_century()   # 2008-09-16
fake.date_this_decade()   # 2013-12-26
fake.date_this_month()   # 2017-12-01
fake.date_this_year()   # 2017-09-19
fake.date_time()   # 2016-08-05 03:23:26
fake.date_time_ad()   # 0258-04-07 20:48:11
fake.date_time_between()   # 2006-06-09 01:28:22
fake.date_time_between_dates()   # 2017-12-06 10:47:23
fake.date_time_this_century()   # 2001-11-30 13:58:47
fake.date_time_this_decade()   # 2012-08-25 18:04:34
fake.date_time_this_month()   # 2017-12-04 11:24:57
fake.date_time_this_year()   # 2017-06-02 08:50:48
fake.day_of_month()   # 15
fake.day_of_week()   # Thursday
fake.district()   # 清河
fake.domain_name()   # lu.com
fake.domain_word()   # zhao
fake.ean()   # 5954186746588
fake.ean13()   # 9672235528133
fake.ean8()   # 06171292
fake.email()   # zhengtao@gmail.com
fake.file_extension()   # docx
fake.file_name()   # 品牌.doc
fake.file_path()   # /关于/推荐.pptx
fake.firefox()   # Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_7; rv:1.9.4.20) Gecko/2011-01-16 07:23:04 Firefox/5.0
fake.first_name()   # 玉珍
fake.first_name_female()   # 彬
fake.first_name_male()   # 莹
fake.first_romanized_name()   # Fang
fake.free_email()   # bwen@hotmail.com
fake.free_email_domain()   # yahoo.com
fake.future_date()   # 2017-12-13
fake.future_datetime()   # 2017-12-19 00:29:14
fake.geo_coordinate()   # -172.459902
fake.hex_color()   # #b4e7a9
fake.image_url()   # https://dummyimage.com/517x471
fake.internet_explorer()   # Mozilla/5.0 (compatible; MSIE 6.0; Windows CE; Trident/4.0)
fake.ipv4()   # 6.155.240.182
fake.ipv6()   # 6903:92c5:9e08:5f0c:5fda:b85e:97ec:b885
fake.isbn10()   # 0-02-210237-X
fake.isbn13()   # 978-1-79735-105-6
fake.iso8601()   # 1986-08-09T07:49:59
fake.job()   # Designer, graphic
fake.language_code()   # bs
fake.last_name()   # 逯
fake.last_name_female()   # 申
fake.last_name_male()   # 查
fake.last_romanized_name()   # Dong
fake.latitude()   # 10.6496555
fake.lexify()   # PEdF
fake.license_plate()   # 4-2558G
fake.linux_platform_token()   # X11; Linux i686
fake.linux_processor()   # i686
fake.locale()   # ka_GE
fake.longitude()   # -45.494435
fake.mac_address()   # 70:0a:bf:0f:77:47
fake.mac_platform_token()   # Macintosh; PPC Mac OS X 10_7_7
fake.mac_processor()   # Intel
fake.md5()   # 71f8c16a5f87000130b7df65611c364a
fake.mime_type()   # message/partial
fake.month()   # 11
fake.month_name()   # February
fake.msisdn()   # 6138497580204
fake.name()   # 离莹
fake.name_female()   # 万成
fake.name_male()   # 况丽华
fake.null_boolean()   # True
fake.numerify()   # 877
fake.opera()   # Opera/9.94.(Windows 95; nl-BE) Presto/2.9.171 Version/11.00
fake.paragraph()   # 系列位置由于作品什么特别研究.精华网络或者搜索.主题我们类别这个增加.
fake.paragraphs()   # [u'\u516c\u53f8\u9700\u8981\u65f6\u95f4\u73af\u5883.\u7684\u4eba\u63d0\u4f9b\u79ef\u5206\u5728\u7ebf\u6807\u51c6\u6cd5\u5f8b\u6211\u4eec\u6ce8\u610f.', u'\u8c22\u8c22\u57fa\u672c\u4ec0\u4e48\u4e2d\u6587\u540d\u79f0\u7136\u540e\u9996\u9875\u5de5\u5177.\u539f\u56e0\u6ca1\u6709\u9700\u8981\u8ba1\u5212\u5b9e\u73b0\u89c9\u5f97.\u7ed3\u679c\u5f53\u524d\u7814\u7a76\u5927\u5bb6.', u'\u7684\u8bdd\u90fd\u662f\u4e4b\u95f4\u4e3a\u4ec0\u672c\u7ad9\u89c4\u5b9a\u5927\u5b66.\u5206\u6790\u62e5\u6709\u800c\u4e14\u6587\u4ef6.']
fake.password()   # z@YJ7Wcpgv
fake.past_date()   # 2017-11-22
fake.past_datetime()   # 2017-12-03 18:08:05
fake.phone_number()   # 18597001558
fake.phonenumber_prefix()   # 132
fake.postcode()   # 870942
fake.profile()   # {'website': [u'https://www.hu.net/', u'https://www.zou.cn/', u'https://shen.cn/', u'http://kong.com/'], 'username': u'wanjing', 'name': u'\u79e6\u79c0\u5170', 'blood_group': '0+', 'residence': u'\u8fbd\u5b81\u7701\u5e06\u53bf\u79c0\u82f1\u516d\u76d8\u6c34\u8857u\u5ea7 436149', 'company': u'\u9ec4\u77f3\u91d1\u627f\u4fe1\u606f\u6709\u9650\u516c\u53f8', 'address': u'\u897f\u85cf\u81ea\u6cbb\u533a\u51e4\u5170\u53bf\u5c71\u4ead\u94f6\u5ddd\u8857P\u5ea7 346744', 'birthdate': '1985-04-28', 'sex': 'M', 'job': 'Engineer, mining', 'ssn': u'433125195206070070', 'current_location': (Decimal('-15.7126615'), Decimal('-143.411020')), 'mail': u'fliang@hotmail.com'}
fake.province()   # 广西壮族自治区
fake.pybool()   # True
fake.pydecimal()   # 384.433560097
fake.pydict()   # {u'\u5927\u5bb6': u'https://www.gao.net/categories/categories/index.php', u'\u90a3\u4e48': 4623, u'\u72b6\u6001': datetime.datetime(1994, 3, 19, 8, 6, 12), u'\u80fd\u529b': Decimal('6.96492'), u'\u540c\u65f6': u'JpjrByPDCgnsNDfaNYgd', u'\u5ba2\u6237': 3485}
fake.pyfloat()   # -4099208226.9
fake.pyint()   # 3270
fake.pyiterable()   # [-7155.447707, u'KOQVBTsYxVpaVxpHBXiO', u'https://www.kang.com/index.php', u'jKmLqgUUOEqdXCeTGBID', u'pGVNjKcxmCTQNpdpKbgm', -48.1915257969, datetime.datetime(1975, 9, 27, 18, 22, 43)]
fake.pylist()   # [4770, datetime.datetime(1990, 4, 11, 9, 59, 16), 2546, 8087, -612180.919, 2.3246212976]
fake.pyset()   # set([u'uwFlxgSEwApkViCNpQZk', u'TlijxYEXankqWtWXkHax', u'TPgKtCtIHXIaKxgWMDjo', Decimal('-72118073288.1'), u'LYoqafrVUVggsnWJXKUg', Decimal('-239813.3099'), u'ELLFUOSNKtxYyhtCXPPg', 1371])
fake.pystr()   # GdxudJdOCeExecGzFpJg
fake.pystruct()   # ([u'WTHzKZdDIrwhUfPHrjMb', u'MVXsSqDWyabyceZRSgGr', datetime.datetime(1993, 10, 3, 1, 1, 31), u'sKcZHJgAGVZrCIfIHwMS', 7694, u'wdedDezTMpfOxUQHaVlO', u'iMgUrRzaaYtArWrnxWda', u'tixihvoqNqQVByfEoGsg', u'https://www.qiu.com/search/explore/home.html', 898068606944.83], {u'\u6709\u9650': Decimal('4.3883198'), u'\u8fd9\u4e48': u'UVOyihAmcukcQJcVIOah', u'\u5408\u4f5c': 3743, u'\u4e0d\u540c': datetime.datetime(2005, 2, 23, 7, 35, 45), u'\u63d0\u9ad8': datetime.datetime(1987, 2, 10, 2, 28, 44), u'\u8bc4\u8bba': 8874, u'\u5173\u4e8e': u'apan@wei.net', u'\u7ec4\u7ec7': 468, u'\u60c5\u51b5': 6083, u'\u884c\u4e1a': u'qiang61@long.org'}, {u'\u4e13\u4e1a': {3: u'AkBWAoxmmokgNrRogyYk', 4: [4596, u'nJzscDjtYSbEzPdkOkRK', 5365], 5: {3: 4605, 4: u'chao87@wei.com', 5: [u'xia30@lu.cn', datetime.datetime(2006, 10, 25, 21, 37, 41)]}}, u'\u4e2d\u6587': {8: [u'oYYfArTznrMITieKBrdT', u'QoESvZcnaAZFmaQqjrgk', u'afkzJChqTNmwwcUXcTOu'], 9: {8: u'ughNWEsmKFFnPReWycbf', 9: [-6.41272, -39213.981], 7: u'RKIcxKTOThQLwaIgVFWe'}, 7: u'uIVZuDPnedhnOJVZUzfX'}, u'\u8fd8\u662f': {9: u'JqElYMJfaassiofLGvLn', 10: [4443, u'aZgiftVvonSEzCzTddiO', u'shaowei@yan.com'], 11: {9: 9967, 10: 5143, 11: [u'usmTtsPWPYtObuYObOpB', Decimal('-31192.5654601')]}}, u'\u6765\u81ea': {1: u'sIqUyGCneohdHGgznDuU', 2: [datetime.datetime(2007, 5, 31, 11, 24, 16), 8321, u'pfIJmDxwAquYLyxrpuVz'], 3: {1: u'gliang@hotmail.com', 2: Decimal('33965.0'), 3: [u'AexgPcuhOIziJhYifZtR', datetime.datetime(2003, 3, 24, 22, 28, 43)]}}, u'\u7cfb\u7edf': {4: u'welRgeLqhOQPGkdkviok', 5: [Decimal('-46.5'), u'hmJxbwRBLukmjHylLojM', u'http://www.mao.cn/search/tag/index.html'], 6: {4: u'http://zou.cn/tag/index/', 5: u'uBlLVOtLauDbAMlrpTZM', 6: [u'bqiHwnSArJdlQnvsbKPN', u'RQdmtWPMwiFuaThJrMWm']}}, u'\u6280\u672f': {8: 2626, 9: [Decimal('4719860282.19'), Decimal('-392046163.17'), datetime.datetime(2005, 1, 11, 13, 21, 2)], 10: {8: u'MoUiPqxBcSTrkudFLIza', 9: u'XUQtWQGntEeuayziAnYA', 10: [u'ulhMPZKMdlQzfWdUuYIF', datetime.datetime(1994, 7, 25, 9, 15, 28)]}}, u'\u9009\u62e9': {8: {8: [u'yong58@ren.cn', u'cGFuWyLdFRUzGhTCaFjE'], 6: 7701, 7: datetime.datetime(2010, 8, 15, 10, 6, 13)}, 6: u'zengwei@gmail.com', 7: [6858, 6403, datetime.datetime(1984, 4, 18, 11, 0, 12)]}, u'\u4e00\u70b9': {0: 6620, 1: [u'OrTScuyESDqszlQjOlYX', u'hJahyMWdkPLhNOMzrdfy', u'mmZYqEDMYPodgUuICyct'], 2: {0: -33313798379.385, 1: u'XRpLoRsRMQIROsBqIHlG', 2: [u'xZozzLqTMwXpfdTpMscc', u'https://www.xia.com/']}}, u'\u7531\u4e8e': {2: u'naguo@qian.com', 3: [u'wTVRQMbwJPUNAKbhAKFs', Decimal('-679732200.8'), u'braeyLsfMvOtsSrgwlxX'], 4: {2: u'feviQSXEPjAzICRiXIWU', 3: u'xiuyinghe@gmail.com', 4: [5961281603639.0, u'YNOuECSZEExtHvlGKwwE']}}, u'\u56fe\u7247': {5: datetime.datetime(1977, 3, 29, 23, 38), 6: [u'http://yin.com/main.jsp', u'yanjia@yahoo.com', 632.53909299766], 7: {5: u'RqBzkDuehAQUCHYQCmAZ', 6: 4597, 7: [8421, 7708]}}})
fake.pytuple()   # (u'CJFHMwspGSwiPKfZhCVY', u'IDhxTOsuOiDHOlKtMbbe', 6637, 978, u'RodatDSuaRbwlgTJNzKx', u'fsUVemSiAyPqyLFmfdZD', u'zhujuan@li.cn', u'https://kong.cn/categories/app/login.htm', Decimal('-406039.250589'), 8127)
fake.random_digit()   # 9
fake.random_digit_not_null()   # 6
fake.random_digit_not_null_or_empty()   # 5
fake.random_digit_or_empty()   # 3
fake.random_element()   # a
fake.random_int()   # 4585
fake.random_letter()   # o
fake.random_number()   # 80709883
fake.random_sample()   # ['a', 'c']
fake.random_sample_unique()   # set(['a', 'c', 'b'])
fake.randomize_nb_elements()   # 13
fake.rgb_color()   # 97,134,130
fake.rgb_css_color()   # rgb(39,226,180)
fake.romanized_name()   # Qiang Du
fake.safari()   # Mozilla/5.0 (Windows; U; Windows NT 6.0) AppleWebKit/532.2.5 (KHTML, like Gecko) Version/4.0.2 Safari/532.2.5
fake.safe_color_name()   # yellow
fake.safe_email()   # ming14@example.net
fake.safe_hex_color()   # #ff3300
fake.sentence()   # 方法科技是否只有无法.
fake.sentences()   # [u'\u4ec0\u4e48\u672c\u7ad9\u6280\u672f\u4e00\u6b21\u8868\u793a\u4e0d\u540c\u5904\u7406.', u'\u8fd0\u884c\u65b9\u5f0f\u80fd\u529b\u4e00\u6837\u5f53\u524d.', u'\u6700\u65b0\u901a\u8fc7\u4e00\u4e2a\u5b66\u6821\u5f53\u524d\u4eca\u5e74\u5982\u679c\u5efa\u8bbe.']
fake.sha1()   # 7052c75358562302ddacd77e14e49986926374fa
fake.sha256()   # 27e24e47230c764507a2e54d25a495e2f1f24ebcc23c6bf2b213b21379f8865e
fake.simple_profile()   # {'username': u'nayuan', 'name': u'\u5b87\u9633', 'birthdate': '1975-11-12', 'sex': 'M', 'address': u'\u6c5f\u897f\u7701\u6f5c\u6c5f\u53bf\u6c38\u5ddd\u62d3\u8defj\u5ea7 699193', 'mail': u'guiying19@hotmail.com'}
fake.ssn()   # 410403194106288547
fake.street_address()   # 燕街L座
fake.street_name()   # 广州街
fake.street_suffix()   # 路
fake.text()   # 留言大小看到.成为控制拥有.
电子个人产品产品这么其他文章.国际谢谢公司系统为什.一起其他作品客户一种系列.
事情中国记者.男人为什组织的话.
要求部门希望.很多投资深圳方面操作威望需要.
注意你们这种学生可是所有通过基本.游戏时候日本目前数据生活得到.
市场这是还是学校时间最后.关于之后浏览相关企业支持结果类别.正在专业人员实现.
fake.time()   # 17:02:29
fake.time_delta()   # 8837 days, 21:54:15
fake.time_object()   # 03:34:28
fake.time_series()   # <generator object time_series at 0x7ff7800cb280>
fake.timezone()   # Asia/Jerusalem
fake.tld()   # cn
fake.unix_time()   # 1100321594
fake.uri()   # https://pan.org/terms/
fake.uri_extension()   # .php
fake.uri_page()   # login
fake.uri_path()   # app/category
fake.url()   # http://www.xie.com/
fake.user_agent()   # Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_6; rv:1.9.5.20) Gecko/2016-10-29 04:38:17 Firefox/12.0
fake.user_name()   # jingmo
fake.uuid4()   # f64bcfad-67c4-c748-5e19-86a74848e6fa
fake.windows_platform_token()   # Windows NT 5.2
fake.word()   # 更新
fake.words()   # [u'\u7136\u540e', u'\u5927\u5b66', u'\u7a0b\u5e8f']
fake.year()   # 2001
```
