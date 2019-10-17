#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 百度AI

参考链接
- https://ai.baidu.com/


安装 百度AI
- pip install baidu-aip


"""
import os
from aip import AipOcr
from aip import AipSpeech

APP_ID = os.environ['baidu_AipSpeech_appid'] 
API_KEY = os.environ['baidu_AipSpeech_api_key'] 
SECRET_KEY = os.environ['baidu_AipSpeech_secret_key']

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(file_path):
    u""" 读取文件
    
    :param str file_path: 文件路径
    """
    with open(file_path, 'rb') as fp:
        return fp.read()

def aipspeech(file_path, dev_pid=1536):
    u""" 语音识别

    :param file_path: 文件名称
    :param dev_pid: 识别模式 1536(普通话简体)
    """
    # xxx.amr
    rtn = client.asr(get_file_content(file_path), 'amr', 16000, {
        'dev_pid': dev_pid,
    })
    print rtn

    speech_text = (rtn['result'][0])
    print speech_text
    return speech_text



if __name__ == '__main__':
    FILE_PATH = "01语音识别.amr"
    aipspeech(FILE_PATH)
    

    # 语音合成
# client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
# 
#  
# 
# str_1 = '''
# 
# 岁月是一条趟过青春的河
# 
# '''
# 
# result  = client.synthesis(str_1, 'zh', 1, {
# 
#     'vol': 5,'per':4,'spd':2,
# 
# })
# 
#  
# 
# # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
# 
# if not isinstance(result, dict):
# 
#     with open('auido.mp3', 'wb') as f:
# 
#         f.write(result)

