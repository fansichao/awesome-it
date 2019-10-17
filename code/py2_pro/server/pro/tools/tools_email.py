#! -*- coding:utf-8 -*-
u"""
- 邮件通知类

@创建时间: 2018-09-08
@创建作者: scfan
@更新时间: 

"""
import time
import datetime
import smtplib
import logging
from email.mime.text import MIMEText

from pro.base.settings import Config

class Email_Post():
    u""" 邮件类 
    
    - email_send_info: 发送消息
    """
    def __init__(self):
        u" 初始化 "
        self.msg_From = Config.msg_from
        self.msg_To = Config.msg_to
        # 发送方的 邮箱授权码
        self.sqm = Config.msg_from_sqm  

        # qq邮箱的smtp Sever地址
        self.smtpSever = 'smtp.qq.com'  

    def email_send_info(self, text=None):
        return
        u""" 发送信息
        :param info:消息
        """
        # 封装发送信息
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['from'] = self.msg_From
        msg['to'] = self.msg_To
        msg['subject'] = 'Python自动邮件-%s' % time.ctime()

        # 建立邮箱服务
        smtp = smtplib.SMTP(self.smtpSever)
        # 登录验证
        smtp.login(self.msg_From, self.sqm)
        # 发送邮件
        smtp.sendmail(self.msg_From, self.msg_To, str(msg))
        smtp.quit()
        logging.info(u">>>>>> 邮件已经发送成功,当前时间:[%s]"%datetime.datetime.now())
    


if __name__ == '__main__':
    email_ins = Email_Post()
    print 'ssssssssssssss'
    email_ins.email_send_info('测试邮件')

 #   # 打印本文件的注释文档
 #   tools_email 文件名称
 #   import tools_email
 #   print help(tools_email)


