# -*- coding:utf-8 -*-
u"""
使用sqlalchemy的
数据库相关的代码，包括了数据库模型的定义，数据库配置等相关的东东。由于目前还不太清楚后续的框架
变化方向，这里定义的东西后续可能改动较大
"""
from sqlalchemy import Integer, Column, Table, ForeignKey, Sequence, String, Date, DateTime, UniqueConstraint, Index, Boolean, Float, CLOB
#TODO:这个是因为sqlite不支持big int autoincrement
from sqlalchemy import Integer as BigInteger, PrimaryKeyConstraint
from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker, mapper, relationship, backref, scoped_session
from sqlalchemy.inspection import inspect
from sqlalchemy.pool import NullPool
from sqlalchemy import func
import datetime
import logging

from flask import g, current_app

from ..base.settings import Config

import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

#TODO:后续改进一个公用的Base类
from sqlalchemy.ext.declarative import declarative_base
Base=declarative_base()

def to_dict(self):
    attrlist = [a for a in self.__dict__.keys() if not a.startswith('_')]
    data = {}
    for name in attrlist:
        d = getattr(self, name, None)
        if isinstance(d, datetime.datetime):
            d = d.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(d, datetime.date):
            d = d.strftime('%Y-%m-%d')
        elif isinstance(d, datetime.time):
            d =  d.strftime('%H:%M:%S')
        data[name] = d
    return data

setattr(Base, 'to_dict', to_dict)


def get_session(subject):
    stat=inspect(subject)
    return stat.session


class Database(object):

    """ Database Manager Object"""

    def __init__(self, configure, name, echo=False):
        self.configure = configure
        self.engine = create_engine(self.get_url(name), echo=echo, pool_size=200, pool_recycle=3600, 
                                    encoding="utf-8", convert_unicode=False)
        self.Session = scoped_session(sessionmaker(bind=self.engine, autocommit=False, autoflush=False))

    def __getattr__(self, name):
        if name == "session":
            return self.Session()

    def get_url(self, config_name):
        self.url = self.configure.get(config_name)
        return self.url

local_db = Database({'url':Config.SQLALCHEMY_DATABASE_URL}, 'url')

#engine = create_engine(Config.SQLALCHEMY_DATABASE_URL, echo=False, pool_size=200, pool_recycle=3600, 
#                        encoding='utf8', convert_unicode=True)
#Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

engine = local_db.engine
current_engine = engine

def simple_session(url=Config.SQLALCHEMY_DATABASE_URL, process=False):
    if process:
        return Database({'url':Config.SQLALCHEMY_DATABASE_URL}, 'url').session
    else:
        return local_db.session

def scope_session(url=Config.SQLALCHEMY_DATABASE_URL):
    return local_db.Session

def now():
    u"""
    取得当前时间，并返回
    """
    if current_app:
        from ..model.date import SystemCalendar
        now = g.db_session.query(SystemCalendar.system_date).first()
        if not now or not now[0]:
            return datetime.datetime.now()
        return now[0]
    return datetime.datetime.now()

#from types import Text

if __name__=='__main__':
    s=simple_session()
    print dir(s.bind)
    print s.bind.url
    print type(s.bind.url)
    print dir(s.bind.url)

