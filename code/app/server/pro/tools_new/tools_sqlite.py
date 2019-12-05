#! -*- coding:utf-8 -*-
u"""
    Sqlite 数据库

sqlite-python: 
    https://docs.python.org/2/library/sqlite3.html
sqlite-sql:
    http://www.runoob.com/sqlite/sqlite-create-database.html
"""

from .base_import import *
from ..base.settings import Config

import sqlite3

class Sqlite():

    def __init__(self):
        self.dbname = Config.SQLITE_CONFIG
        conn = sqlite3.connect(self.dbname)
        self.c = conn.cursor()
        pass
    
    def conn(self):
        return self.c

    def exec_sql(self, sql):
        res = self.c.execute(sql)
        print sql
        return res

    def exec_sql_muti(self,sql,lis):
        u" 批量执行 "
        self.c.executemany(sql, lis)
        self.c.commit()

    def close(self):
        self.c.close()
