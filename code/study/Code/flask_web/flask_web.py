#! -*- coding:utf-8 -*-
'''
@Author: Scfan
@Date: 2018-12-23 18:10:28
@LastEditors: Scfan
@LastEditTime: 2019-01-21 07:54:24
@Description: 工作&amp;学习&amp;生活
@Email: 643566992@qq.com
@Company: 上海
@version: V1.0
@Msg:
    Flask官网
    BootStrap官网


flask扩展-官方链接:
    http://flask.pocoo.org/extensions/
# flask扩展安装
pip install flask
# SQLAlchemy database migrations
pip install flask-migrate
# 命令行解释器
pip install flask-script
# 邮件
pip install flask-email flask-mail
# 前端框架
pip install flask-bootstrap
# 本地化时间和日期
pip install flask-moment
# Flask-WTF-简化表单处理、防跨站请求伪造（CSRF）攻击
pip install flask-wtf

'''
from __future__ import unicode_literals
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from flask import Flask

# 初始化
app = Flask(__name__)

# 路由和视图函数
@app.route('/')
def index():
    return 'sss'
    
@app.route('/user/<name>')
def user(name):
    return 'sss  %s'%name

from flask import request
# 请求上下文
@app.route('/index_http')
def index_http():
    user_agent = request.headers.get('User-Agent')
    return '浏览器的user_agent是[%s]'%user_agent
    

# 请求与相应循环  
''' 
# 程序上下文和请求上下文
current_app 程序上下文 当前激活程序的程序实例
g 程序上下文           处理请求时用作临时存储的对象.每次请求都会重设变量
request 请求上下文
session 请求上下文
# 请求调度
收到客户端发来请求，找到对应的视图函数。app.route或app.add_url_rule()生成映射
app.url_map
# 请求钩子
在处理请求之前或之后执行代码，处理钩子使用修饰器实现
1. before_first_request: 注册一个函数，在处理第一个请求时运行
2. before_request: 注册一个函数，在每次请求之前运行
3. after_request: 注册一个函数，若无异常，每次请求之后运行
4. teardown_request: 处理一个函数，即使有异常，每次请求之后也会运行。

'''
# 2.5.4 响应
from flask import make_response

# 创建响应对象和 cookie
@app.route('/')
def index2():
    response = make_response('<h1>This document carries a cookie</h1>')
    response.set_cookie('answer','42')
    return response
# 网址重定向
from flask import redirect
@app.route('/study_redirect')
def study_redirect():
    return redirect('http://wwww.baidu.com')
# abort 处理错误，返回错误到 Web服务器
from flask import abort
@app.route('/study_abort/<id>')
def get_user(id):
    user = id
    if not user:
        abort(404)
    return 'hello %s'%user.name
# 2.6 Flask 扩展 
''' 
Flask相关插件，便于项目开发
'''

# Flask-Script 支持命令行选项
# pip install flask-script
#from flask.ext.script import Manager
from flask_script import Manager
manager = Manager()

# 第三章 模板
''' 
使用模板，易于维护且代码结构良好。
''' 
# 3.1 Jinja2 模板

# 3.1.1 渲染模板
' Flask默认会在程序文件夹下的 templates 中寻找模板 '
from flask import Flask, render_template
@app.route('/A03/A01')
def A03_A01():
    return render_template('index.html')
@app.route('/A03/<name>')
def A03(name):
    return render_template('user.html',name=name)
# 3.1.2 变量
'''
Jinja2 部分常用变量过滤器，完整见官网
exp:
     hello, {{name|capitalize}}
safe 渲染时不转义(安全考虑，默认转义)
capitalize 首字母大写，其他小写
lower 转小写
upper 转大写
title 每个单词中首字母转为大写
trim 去除首尾空格
striptags 渲染之前去除所有html的标签
''' 
# 3.1.3 控制结构
''' 
Jinja2 提供了多种控制结构，用于修改模板渲染流程。
详见 base.html extends 衍生模板
''' 
# 3.2 Flask-Bootstrap TODO
#from flask.ext.bootstrap import Bootstrap
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
'''
{% extends 'bootstrap/base.html' %}
继承bootstrap后，可以使用bootstrap中css、style等
''' 

# 3.3 自定义错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

# 3.4 链接
'''
url_for 使用程序生成对应url

url_for('user',name='join',_external=True) 相当于 /user/join
''' 

# 3.5 静态文件
''' 
默认 Flask 会在 static 中寻找静态文件。
''' 

# 3.6 Flask-Moment 本地化日期时间插件
pass


# 第四章 Web表单 TODO

# 获取 请求中的表单信息
#print request.form

# 4.1 跨站请求伪造保护

''' 
默认情况下 Flask-WTF 会保护表单免受跨站请求伪造攻击。

app = Flask(__name__)
# 设置密钥免于被攻击
app.config['SECRET_KEY'] = 'sssssssssss'
''' 
# TODO 重定向 POST-重定向-get
# 数据存储在用户会话中
# @app.route('/',methods=['POST','GET'])

# 第五章 数据库

# 5.1 SQL数据库
''' 
关系型数据库将数据存储在表中，表模拟程序中不同的实体。
''' 
# 5.2 NoSql数据库
''' 
不遵循关系型数据库的都为NoSql数据库。
多存储为文档，数据冗余，但是查询速度也会对应提升。
''' 

# 5.3 SQL和NOSQL的选择

''' 
SQL 擅长高效紧凑的形式存储结构化数据。需要大量精力保持数据一致性。
NOSQL 放宽了数据一致性的要求，拥有性能和大数据量的优势，
当前大数据情况下，NOSQL成为主流，逐渐替代SQL
''' 
# 5.4 Python 数据库框架
'''
Python数据库框架考虑因素:
易用性
性能
可移植性
Flask集成程度
''' 

# 5.5 使用 Flask-SQLAlchemy 管理数据库 pip install flask-sqlalchemy
''' 
数据库URL样例
MYSQL mysql://username:password@host/database
Postgres postgresql://username:password@host/database
Sqlite sqlite:////absolute/path/to/database
''' 
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABSE_URI'] = "sqlite:///" + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


# 5.6 定义模型  建立ORM表结构
pass
''' 
# 常用sqlalchemy字段类型
TODO 48page


''' 

# 5.7 关系 表结构关系建立

# 5.8 数据库命令

# 5.9 flask-migrate 数据库迁移
''' 
# hello.py
from flask.ext.migrate import Migrate,MigrateCommand
migrate = Migrate(app, db)
manager.add_comment('db',MIgrateCommand)

# 先创建迁移仓库
python hello.py db init
''' 

# 第六章 电子邮件
''' 
flask-email 插件 SMTP服务器配置
程序集中发送email 异步发送email 统一发给celery处理
''' 
# 邮件服务器的主机名/IP地址
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
# 启用传输层安全 TLS协议
app.config['MAIL_USE_TLS'] = True
# 启用安全套接层 SSL协议
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ['scfan_username']
app.config['MAIL_PASSWORD'] = os.environ['scfan_password']

from flask_mail import Message
# 异步邮件
from threading import Thread

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX'] + subject,
        sender = app.configp['FLASK_MAIL_SENDER'],recipients=[to]
    )
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template+'.html',**kwargs)
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr



 





print  app.url_map

if __name__ == '__main__':
    host_ip = '192.168.172.70'
    app.run(debug=True,port=9999,host=host_ip)
    
    # 支持命令行输入参数 python Code\flask_web.py runserver --help
    #manager.run()











u"""
问题记录

问题1: ImportError: No module named ext.script
由于现有版本导入扩展方式变更导致的
from flask.ext.script import Manager
修改为如下方式即可
from flask_script import Manager
"""



