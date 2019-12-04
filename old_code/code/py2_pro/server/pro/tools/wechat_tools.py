#! -*- coding:utf-8 -*-
u"""

    微信Api 

微信小程序：
    https://developers.weixin.qq.com/miniprogram/dev/api/wx.getSystemInfoSync.html

python-wxpy:
    https://pypi.org/project/wxpy/0.3.0/
    官网文档很全,查看官网文档即可
    https://wxpy.readthedocs.io/zh/latest/


"""
from __future__ import unicode_literals

from wxpy import *

from pro.base.settings import Config
from pro.tools.base_datetime_tools import (datetime2str, get_now_datetime,
                                           str2datetime)
from pro.tools.base_import import *


"""
异常问题记录

命令 Bot(console_qr=True)
错误 global name 'FileNotFoundError' is not defined
出现以上异常，可能与文件权限，缓存文件有关

"""


class Wechat_Api(object):
    u"""
        微信 wxpy API
    术语说明
        friend - 好友
        map - 公众号
        group - 群聊

    好友 Friend
    群聊 Group
    群成员 Member
    公众号 MP
    """

    def __init__(self,*args,**kwargs):
        u""" 初始化
        - 登录操作
        """
        cache_path = os.path.join(Config.TMP_PATH,kwargs.get('qr_path') or 'wxpy.pkl')
        qr_path = os.path.join(Config.TMP_PATH,kwargs.get('qr_path') or 'qr.png')
        print cache_path 
        print qr_path 

        # 登录
        # TODO 大号可以扫描登录 小号不能扫描登录 ？？？？
        self.bot = Bot(cache_path=cache_path,console_qr=True,qr_path=qr_path)
        #self.bot = Bot(console_qr=True)
        # 机器人账号
        self.reboot = self.bot.self
        
        # 微信多开
        #self.bot2 = Bot()

        self.suc_flag_dic = {
            True:'成功',
            False:'失败',
        }



    #########################
    #### 调用Api
    #########################
    def send_msg_friends(self,msg_dic={}):
        u""" 批量发送信息 指定信息/时间/人
        msg_dic = {
            '好友A':{   
                datetime.datetime.now():['test2'],
            },
        }
        """
        for friend_name,dic in msg_dic.items():
            for sendTime in sorted(dic.keys()):
                self._send_msg_friends_sendTime(friend_name,dic[sendTime],sendTime)

    def reboot_get(self,rtypes=['all']):
        u""" 获取聊天对象
        @param rtype: 返回的数据类型
        """
        all_rtypes = ['friends','groups','mps','chats']
        if rtypes == ['all']:
            rtypes = all_rtypes
        
        rdic = dict()
        for rtype in rtypes:
            # 所有好友
            if rtype == 'friends':
                data = self.bot.friends(update=True)
            # 所有群聊
            elif rtype == 'groups':
                data = self.bot.groups(update=True,contact_only=False)
            # 所有公众号
            elif rtype == 'mps':
                data = self.bot.mps(update=True)
            # 所有聊天对象
            elif rtype == 'chats':
                data = self.bot.chats(update=True)
            else:
                continue
            rdic[rtype] = data
        
        print(rdic)
        return rdic

    def reboot_search(self,stypes=['all'],sval="陪伴",*args,**kwargs):
        u""" 搜索聊天对象
        @param stypes: 搜索对象
        @param sval: 搜索的值
        """
        all_stypes = ['friends','groups','mps','chats']
        if stypes == ['all']:
            stypes = all_stypes
        
        rdic = dict()
        for rtype in stypes:
                # 搜索好友
                if rtype == 'friends':
                    friends_keys = {'city':None,'sex':None}
                    data = ensure_one(self.bot.friends().search(func_val,**kwargs))
                # 搜索群聊:
                elif rtype == 'groups':
                    wxpy_groups = self.bot.groups().search(func_val)

                    # # 搜索名称包含 'wxpy'，且成员中包含 `游否` 的群聊对象
                    # wxpy_groups = self.bot.groups().search('wxpy', [youfou])

                    # # 在刚刚找到的第一个群中搜索
                    # group = wxpy_groups[0]
                    # # 搜索该群中所有浙江的群友 搜索任何类型的聊天对象 (但不包含群内成员)
                    # found = group.search(province='浙江')
                    # [<Member: 浙江群友 1>, <Group: 浙江群友 2>, <Group: 浙江群友 3> ...]
                # 所有公众号
                #elif rtype == 'mps':
                #    data = self.bot.mps(update=True)
                # 所有聊天对象
                elif rtype == 'chats':
                    # 搜索名称含有 'wxpy' 的任何聊天对象
                    data = self.bot.search(sval)
                else:
                    continue
                rdic[rtype] = data
        print rdic
        return rdic

    def reboot_deal(self,func_type=''):
        u""" 机器人处理功能
        """

        # 获取单个或批量获取多个用户的详细信息(地区、性别、签名等)，但不可用于群聊成员
        self.bot.user_details(user_or_users, chunk_size=50)
        # 上传文件，并获取 media_id
        media_id = self.bot.upload_file(path)
        
        # 添加好友
        self.bot.add_friend(user, verify_content='')
        # 添加公众号
        self.bot.add_mp(user)
        # 接收用户成为好友
        self.bot.accept_friend(user, verify_content='')
        # 创建一个新的群聊
        self.bot.create_group(users, topic='群名称')
        # 自动消除手机端的新消息小红点提醒
        self.bot.auto_mark_as_read(True)



    def reboot_logout(self):
        # 登出当前账号
        self.bot.logout()

    def reboot_pause(self):
        u" 堵塞进程 "
        # 堵塞进程，直到结束消息监听 (例如，机器人被登出时)
        self.bot.join()
    


       

    def tmp(self):
        # 启用 puid 属性，并指定 puid 所需的映射数据保存/载入路径
        self.bot.enable_puid('wxpy_puid.pkl')
        
        # 好友名称或昵称
        my_friend = ensure_one(self.bot.friends().search('陪伴'))
        
        # 查看他的 puid
        print(my_friend.puid)
        # 'edfe8468'



        
    def select_object(self):
        u""" 选择聊天对象
        """
        
        pass
   
    #########################
    #### 基础Api 第一层级
    #########################
    def _send_msg_friends_sendTime(self,friend_name,msgs=['test'],sendTime=None):
        u""" 指定时间 向朋友发送信息
        """
        ## 向文件传输助手发送消息
        #self.bot.file_helper.send(msg)
        try:
            suc_flag = False
            while not suc_flag:
                time_now = get_now_datetime()
                sendTime = sendTime or time_now

                time_now_str = datetime2str(time_now)
                sendTime_str = datetime2str(sendTime)
                
                print time_now_str,sendTime_str
                if sendTime < time_now:
                    logging.error('>> 消息[%s]发送时间[%s]小于当前时间,发送失败!!!'%(str(msgs),sendTime_str))

                if time_now_str == sendTime_str:
                    print friend_name
                    my_friend = ensure_one(self.bot.friends().search(friend_name))
                    for msg in msgs:
                        my_friend.send(msg)
                    suc_flag = True
                time.sleep(0.1)
            logging.info('>> 发送消息 内容:[%s]时间:[%s] %s'%(str(msgs),sendTime_str,self.suc_flag_dic[suc_flag]))
        except Exception as e:
            print e
            print traceback.format_exc()
            logging.error('>> 发送消息 内容:[%s]时间:[%s] %s'%(str(msgs),sendTime_str,self.suc_flag_dic[suc_flag]))
            return False
        return True

    def main_test(self):
        u""" 测试函数入口
        """
        # 指定时间发送消息
        now_time = get_now_datetime()
        msg_dic = {
            '陪伴是最长情的告白':{
                now_time+datetime.timedelta(seconds=1):['Atest1','test2'],
            }
        }
        self.send_msg_friends(msg_dic)

        # 获取信息
        self.reboot_get()
        self.reboot_search()
        self.reboot_else()
        self.reboot_deal()
        pass


class Grap(object):
    u"""
        抓取信息
    """
    def __init__(self):
        pass

    def get_iciba_news(self, contents=None,translation=None):
        u""" 获取api信息 """
        #获取金山词霸每日一句，英文和翻译
        url = "http://open.iciba.com/dsapi/"
        r = requests.get(url)
        if not contents:
            contents = r.json()['content']
            message1 = contents
        if not translation:
            translation= r.json()['translation']
            message2 = translation[5:]

        return [message1,message2]




bot = Bot(console_qr=True)

# 自动接受好友请求
# 注册好友请求类消息
@bot.register(msg_types=FRIENDS)
# 自动接受验证信息中包含 'wxpy' 的好友请求
def auto_accept_friends(msg):
    # 判断好友请求中的验证文本
    if 'wxpy' in msg.text.lower():
        # 接受好友 (msg.card 为该请求的用户对象)
        new_friend = bot.accept_friend(msg.card)
        # 或 new_friend = msg.card.accept()
        # 向新的好友发送消息
        new_friend.send('哈哈，我自动接受了你的好友请求')

my_friend = ensure_one(bot.search(u'陪伴是最长情的告白'))
tuling = Tuling(api_key=os.environ['wechat_tulingreboot_apikey'])

# 使用图灵机器人自动与指定好友聊天
@bot.register(my_friend)
def reply_my_friend(msg):
    tuling.do_reply(msg)

if __name__ == '__main__':
    pass



def test():
    wxpy_api = Wechat_Api()
    wxpy_api.main_test()

if __name__ == '__main__':
    test()
