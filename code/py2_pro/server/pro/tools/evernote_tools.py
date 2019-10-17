# -*- coding: utf-8 -*-
u"""
    印象笔记 APi

安装evernote
    pip install evernote
官方API链接:
    https://dev.yinxiang.com/doc/reference/NoteStore.html#Fn_NoteStore_createTag
开发者auth_token获取链接
    auth_token: 访问 https://app.yinxiang.com/api/DeveloperToken.action 生成
使用说明
    1. 查看参数 通过官方Api或者NoteStore查看参数
    In [65]: NoteStore.createTag_args()
    Out[65]: createTag_args(authenticationToken=None, tag=None)
    2. 笔记/标签/笔记本等 基本属性都是 guid 等
    3. 类型使用 Types 创建

"""

from .base_import import *

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore


# 印象笔记API 配置文件
EvernoteApi_CONFIG = {
    'evernote_auth_token': os.environ['evernote_auth_token'],
}

class EvernoteApi():
    u""" 印象笔记API封装
   
    功能说明:
        - 获取指定笔记本信息
        - 获取指定笔记信息

        - 创建笔记
        - 添加标签
        - 删除笔记
        - 删除标签
        

    """
    def __init__(self,*args,**kwargs):
        u""" 初始化参数

        @param: str auth_token:开发者token
        """
        self.auth_token = kwargs.get('evernote_auth_token') or EvernoteApi_CONFIG['evernote_auth_token']
        client = EvernoteClient(token=self.auth_token, service_host='app.yinxiang.com')
        try:
            # 用户信息
            self.user_store = client.get_user_store()
            # 笔记信息 笔记本/标签等
            self.note_store = client.get_note_store()
        except Exception as e:
            print u"错误信息:[%s] "%(self.error_code_msg(e.errorCode)[1])
            self.error_code_deal(e.errorCode)

    def get_book_infos():
        u""" 获取笔记本信息
        """
        pass

    def get_note_infos():
        u""" 获取笔记信息
        """
        pass


    def get_tag_infos():
        u""" 获取标签信息
        """
        pass


    def add_book():
        u""" 添加笔记本
        """
        pass

    def add_note():
        u""" 添加笔记
        """
        pass

    def add_tag():
        u""" 添加标签
        """
        pass

    def copy_note():
        u""" 笔记复制
        """
        pass

    def error_code_msg(self,error_code=1):
        u""" 获取异常代码信息
        """
        # 数据来源链接
        #   https://dev.yinxiang.com/doc/reference/Errors.html#Enum_EDAMErrorCode
        error_dic = {
            1:['UNKNOWN','没有关于错误的信息'],
            2:['BAD_DATA_FORMAT','请求数据的格式不正确'],
            3:['PERMISSION_DENIED','不允许执行操作'],
            4:['INTERNAL_ERROR','服务意外问题'],
            5:['DATA_REQUIRED','缺少必需的参数/字段'],
            6:['LIMIT_REACHED','由于数据模型限制,操作被拒绝'],
            7:['QUOTA_REACHED','由于用户存储限制,操作被拒绝'],
            8:['INVALID_AUTH','用户名和/或密码不正确'],
            9:['AUTH_EXPIRED','身份验证令牌已过期'],
            10:['DATA_CONFLICT','由于数据模型冲突,更改被拒绝'],
            11:['ENML_VALIDATION','提交的备注内容格式不正确'],
            12:['SHARD_UNAVAILABLE','包含帐户数据的服务分片暂时关闭'],
            13:['LEN_TOO_SHORT','由于数据模型限制,操作被拒绝,其中诸如字符串长度之类的东西太短'],
            14:['LEN_TOO_LONG','由于数据模型限制,操作被拒绝,其中诸如字符串长度之类的东西太长'],
            15:['TOO_FEW','由于数据模型限制,操作被拒绝,其中某些东西太少.'],
            16:['TOO_MANY','由于数据模型限制,操作被拒绝,其中有太多东西.'],
            17:['UNSUPPORTED_OPERATION','操作被拒绝,因为它当前不受支持.'],
            18:['TAKEN_DOWN','操作被拒绝,因为响应撤销通知,禁止访问相应的对象.'],
            19:['RATE_LIMIT_REACHED','操作被拒绝,因为调用应用程序已达到此用户的每小时API调用限制.'],
        }

        return error_dic.get(error_code,error_dic[1])

    def error_code_deal(self,error_code):
        u""" 错误代码 处理逻辑
        """
        # TODO 其他详细代码错误处理
        if error_code == 19:
            deal_msg = '等待3600s'
            "账号每小时操作次数限制,等待一小时即可.登录也可能会受到影响."
            time.sleep(3600)

    def create_tag(self,tag_names=['test'],parentTagname=None):
        u""" 创建标签 若无父标签名称,会存储在最顶级
        @param tag_names: 创建的标签名称列表
        @param parentTag: 父标签名称
            parentTag/tag_name1、tag_name2
        """
        # 获取父标签 guid
        guid = None
        if bool(parentTagname):
            Tags = self.note_store.listTags(authenticationToken=self.auth_token)
            for tag in Tags:
               if tag.name == parentTagname:
                    guid = tag.guid 
        # 创建标签
        count = 0 
        error_count = 0 
        while bool(tag_names):
            error_new = []
            for tag_name in tag_names:
                msg = " 成功"
                tag = Types.Tag(guid=None,name=tag_name,parentGuid=guid,updateSequenceNum=None)
                try:
                    self.note_store.createTag(self.auth_token,tag)
                    count += 1
                    print tag_name + msg,count
                except Exception as e:
                    error_count +=1
                    msg = u" 失败 [%s] "%(self.error_code_msg(e.errorCode)[1])
                    error_new.append(tag_name)
                    time.sleep(1)
                    print tag_name + msg,error_count

            tag_names = copy.deepcopy(error_new)
            if error_count >= 100:
                print "错误次数大于100,跳出循环,手动处理"
                break




class EvernoteApi():

    def __init__(self,*args,**kwargs):
        u""" 初始化参数
        @param: auth_token: 开发token
        """
        self.auth_token = kwargs.get('evernote_auth_token') or os.environ['evernote_auth_token']
        client = EvernoteClient(token=self.auth_token, service_host='app.yinxiang.com')
        try:
            # 用户信息
            self.user_store = client.get_user_store()
            # 笔记信息 笔记本/标签等
            self.note_store = client.get_note_store()
        except Exception as e:
            print u"错误信息:[%s] "%(self.error_code_msg(e.errorCode)[1])
            self.error_code_deal(e.errorCode)


    def main_test(self):
        u" 测试入口 "
        Tags = self.note_store.listTags(authenticationToken=self.auth_token)
        print "标签:",Tags[0]
        notebooks = self.note_store.listNotebooks()
        print "笔记本:",notebooks[0]
        self.create_tag(tag_names=['test','test2'],parentTagname=None)

if __name__ == '__main__':
    evernote_api = EvernoteApi()
    evernote_api.main_test()

