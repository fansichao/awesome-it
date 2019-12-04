# -*- coding: utf-8 -*-
u"""
   批量 创建日期标签
"""
import logging
import datetime
import time
import os
import copy

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from ..tools.tools_evernote import EvernoteApi


def get_datetime_tags():
    u" 获取一段日期 "
    # 2019-01-23 周三
    weekday_chinese_map = {
        0: '周一',
        1: '周二',
        2: '周三',
        3: '周四',
        4: '周五',
        5: '周六',
        6: '周日',
    }

    st = datetime.datetime(2020,11,12)
    ed = datetime.datetime(2020,12,31)
    msgs = list()
    while st<=ed:
        msg = str(st)[0:10] + ' ' + weekday_chinese_map[datetime.datetime.weekday(st)]
        st = st + datetime.timedelta(1)
        msgs.append(msg)
    return msgs
    
def test():
    evernoteapi = EvernoteApi()
    tag_names = get_datetime_tags()
    evernoteapi.create_tag(tag_names=tag_names,parentTagname='test')

if __name__ == '__main__':
    evernoteapi = EvernoteApi()
    tag_names = get_datetime_tags()
    evernoteapi.create_tag(tag_names=tag_names,parentTagname='test')

