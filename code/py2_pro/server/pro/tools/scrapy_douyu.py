# -*- coding:utf-8 -*-
u"""
@Author: Scfan
@Date: 2018-12-03 17:26:18
@LastEditors: Scfan
@LastEditTime: 2018-12-03 17:26:44
@Description: 工作&amp;学习&amp;生活
@Email: 643566992@qq.com
@Company: 上海
@version: V1.0
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

# 设置 代理服务器
scrapy_proxy.get_proxy_main()
session = scrapy_proxy.use_proxy().get('session')

#################
# 斗鱼 
#################
u"""
斗鱼视频格式
- flv头 + m4s视频流
- flv头: https://tc-tct.douyucdn2.cn/dyliveflv3a/1126960r2h8YKuHh.flv
- m4s视频流: https://p2ptest1.p2p.liveplay.myqcloud.com/video/1126960r2h8YKuHh/info/v_1126960r2h8YKuHh_1543647602.m4s

"""

    #GET https://p2ptest1.p2p.liveplay.myqcloud.com/video/1126960r2h8YKuHh/info/v_1126960r2h8YKuHh_1543646947.m4s HTTP/1.1
    #HTTP/1.1 200 OK
    #Server: MC_VCLOUD_LIVE
    #Date: Sat, 01 Dec 2018 06:49:17 GMT
    #Content-Type: video/MP2T
    #Content-Length: 73
    #Connection: keep-alive
    #Cache-Control: max-age=15
    #Last-Modified: Sat, 01 Dec 2018 14:49:17 GMT
    #Access-Control-Allow-Credentials: true
    #Access-Control-Allow-Origin: https://www.douyu.com
    #X-NWS-LOG-UUID: bfa0459a-dfd0-4225-a0ef-2b6f8d7f6e6d

def get_data(room_id='1126960'):
    u" 获取页面数据 "
    headers = {
        # Client
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        # Miscellaneous
        'Referer': 'https://www.douyu.com/%s'%room_id,
        # Scurity
        'Origin': 'https://www.douyu.com',
        # Transport
        'Connection': 'keep-alive',
        'Host': 'p2ptest1.p2p.liveplay.myqcloud.com',
    }
    url = "https://www.douyu.com/1126960"
    response = session.get(url, headers=headers, verify=False)
    print response
    print response.content
    print dir(response)
    return 

def get_video_flow(room_id=None,room_val=None,time_num=None):
    u" 获取直播视频流 "
    import os
    time_num = str(int(time.time()))
    url = "https://p2ptest1.p2p.liveplay.myqcloud.com/video/%s%s/info/v_%s%s_%s.m4s"%(room_id,room_val,room_id,room_val,time_num)
    # 下载m4s视频流
    os.system('wget %s'%url)
    print url
    return url

#更新:确实是腾讯的切片，不过是flv格式，前4字节为数据长度，剩下的是flv的tag数据，多个m4s文件拼接再加上flv头即可播放。
#是腾讯p2p切片数据，可以查看js看它如何解码的，应该是mp4切片加上一些视频信息，我后续看一下再更


def get_video_flv(room_id=None,room_val=None):
    headers = {
        'Host': 'tc-tct.douyucdn2.cn',
        'Connection': 'keep-alive',
        'Origin': 'https://www.douyu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://www.douyu.com/%s'%room_id,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    url = 'https://tc-tct.douyucdn2.cn/dyliveflv3a/%s%s.flv'%(room_id,room_val)



    # https://hdls3a.douyucdn.cn/live/4517962rQZTPeBTV.flv?wsAuth=53d02469c660aad55406dc12f5f60901&token=web-douyu-224824414-4517962-a086adf574d883dc5986f25e3181c209&logo=0&expire=0&did=10000000000000000000000000001501&ver=Douyu_218112961&pt=2&st=0&mix=0
    print url
    os.system('wget %s'%url)
    

def m4s2mp4():
    from ffmpy import FFmpeg
    # ffmpeg -i in.flv -f avi -vcodec mpeg4 -acodec libmp3lame out.avi
    
    cmd = "ffmpeg -i in.flv -f avi -vcodec mpeg4 -acodec libmp3lame out.avi"
    text = execCmd(cmd)

    # flv + m4s -> mp4 ???
    # cat flv >> mp4
    # cat m4s >> mp4
    # cat init.mp4 $(ls -vx segment-*.m4s) > source.mp4
    # ffmpeg -i in.flv -f avi -vcodec mpeg4 -acodec libmp3lame out.avi



def main(room_id=None):
    room_id = '1126960'
    val = 'r2h8YKuHh'
    room_id = '5429365'
    room_val = 'rGNdAQOv7'
    get_video_flv(room_id=room_id,room_val=room_val)
    get_video_flow(room_id=room_id,room_val=room_val)
    for i in range(10):
        time.sleep(1)
        get_video_flow()





if __name__ == '__main__':
   
    main()







#####################
### 牛散掘金
#####################
u"""
功能模块:
- 一个新的HTML框架
- 视频 转接
- 聊天室 转接
- 登录 转接
- 其他信息 转接




















# http://www.8zpd.cn/6001
video = CK%3A3aOWqxfMRrTbS665HCM7skS%2BYTd9tufUfoJVCguCGzgVX7xpMeeOMLq6gamd40Cu



def 

<embed src="http://www.ckplayer.com/ckplayer/x/ckplayer.swf" flashvars="video=视频地址"  quality="high" width="480" height="400" align="middle" allowScriptAccess="always" allowFullscreen="true" type="application/x-shockwave-flash"></embed>

聊天室 
http://47.97.4.253:7272/
聊天室头部
GET http://47.97.4.253:7272/ HTTP/1.1
Host: 47.97.4.253:7272
Connection: Upgrade
Pragma: no-cache
Cache-Control: no-cache
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36
Upgrade: websocket
Origin: http://www.8zpd.cn
Sec-WebSocket-Version: 13
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Sec-WebSocket-Key: HdnB84Q0BFJzoD9fINXBag==
Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits

HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Sec-WebSocket-Version: 13
Connection: Upgrade
Sec-WebSocket-Accept: N8w6citENheAmM97zIDahFwdu6E=
Server: workerman/3.5.6





def execCmd(cmd):
    # 执行计算命令时间
    r = os.popen(cmd)
    text = r.read().strip()
    r.close()
    return text
    

"""




