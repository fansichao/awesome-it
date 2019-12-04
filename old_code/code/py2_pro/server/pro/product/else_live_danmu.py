#! -*- coding:utf-8 -*-
u"""
    获取 直播 弹幕

"""
from __future__ import unicode_literals

import requests 
import datetime
import time

import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

def danmu_bilibili(room_id='521429'):
    u""" 获取 B站 弹幕
    @param room_id: 房间ID
    """
    # TODO 需要在直播，否则会卡主
    url ='https://api.live.bilibili.com/ajax/msg'
    # 构造POST提交参数
    form = {
        'csrf_token':'',
        'roomid':room_id,
        'token':''
    }

    while True:
        # 开始提交数据
        html1 = requests.post(url,data=form)
        # 弹幕数据1
        text1 = list(map(lambda ii: html1.json()['data']['room'][ii]['text'],range(10)))

        # 暂停5秒,再提交数据(太快提交会导致重复,暂停也可能重复)
        time.sleep(5)
        html2 = requests.post(url,data=form)
        # 弹幕数据2
        text2 = list(map(lambda ii: html2.json()['data']['room'][ii]['text'],range(10)))
        # 比较两个弹幕信息,列表推导弹幕信息
        bilibili_txt = [item for item in text2 if item not in text1]
        for danmu in bilibili_txt:
            now_time = str(datetime.datetime.now())[0:19]
            print('[%s] 直播间实时弹幕：%s'%(now_time,danmu))

            
def danmu_douyu(room_id=None):
    u""" 获取斗鱼主播弹幕
    @param room_id: 房间ID
    """
    pass
    
# 启动程序
if __name__ == '__main__':
    room_ids = [
        5096,521429,39936
    ]
    # B站 弹幕
    for room_id in room_ids:
        danmu_bilibili(str(room_id))
    # 斗鱼 弹幕
    danmu_douyu(room_id=None)

