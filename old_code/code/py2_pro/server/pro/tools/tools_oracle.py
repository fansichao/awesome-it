#! -*- coding:utf-8 -*-
u"""

Oracle 工具

检查数据是否迁移正确

检查项
- 表/视图
- 数据条数
- 字段类型 
- 数据值

"""
import sys
import logging
import unittest
import traceback
        
from sqlalchemy import create_engine
from sqlalchemy.orm import aliased
from sqlalchemy.orm import sessionmaker
from nose.tools import eq_, raises, assert_true

from ..database.sqlal import simple_session

class Oracle_Tool(object):
    u""" Oracle 脚本

    - re_create_table   单表重建
    - re_create_tables  多表重建

    """
    def __init__(self):

        self.session = simple_session()
        pass
    
    ###############
    ### get 查询
    ###############
    def get_tables_name(self,owner='FDM'):
        u""" 获取用户表名称
        
        :param owner:用户名称
        """
        sql = """ select * from sys.user_tables where owner=%s """%owner.upper()
        res = self.session.execute(sql).fetchall()
        tabs = [ t[0] for t in res]
        return tabs
        
    def get_tab_count(self,tab=None):
        u""" 获取表数据条数
    
        :param tab: 表名称
        """
        sql = """ select count(1) from %s """ %tab


    def get_all_user_table_names(self, user=None):
        u""" 查询 指定用户下 所有表名称 """
        if not bool(user):
            sql = """ select table_name,owner from sys.all_tables """
        else:
            sql = """ select table_name,owner from sys.all_tables where owner='%s' """% user.upper()
        res = self.session.execute(sql).fetchall()
        names = []
        for row in res:
            print row
            names.append(row[0])
        return names

    def get_all_use_sequence_names(self, user=None):
        u""" 查询 指定用户下 所有序列名称 """
        if not bool(user):
            sql = """ select sequence_name,sequence_owner from sys.all_sequences """
        else:
            sql = """ select sequence_name,sequence_owner from sys.all_sequences where sequence_owner = '%s' """% user.upper()
        res = self.session.execute(sql).fetchall()
        names = []
        for row in res:
            names.append(row[0])
        return names
        
    ###############
    ### drop 删除
    ###############
    def drop_tabs_seqs(self, names=[], run_flag=False, dtype='table'):
        u""" 删除 表/序列

        :param names: 名称
        :param run_flag: 是否运行
        :param dtype: 指定名称类型 表/序列 table/sequence

        """
        dtype_name = '序列' if dtype=='sequence' else '表'
        count = 0
        count_suc = 0
        for name in names:
            count += 1
            sql = """ drop %s %s """ % (dtype, name)
            if run_flag:
                print(">>>> 运行中,删除%s[%s],命令为[%s]"%(dtype_name,name,sql))
                try:
                    self.session.execute(sql)
                    self.session.commit()
                    count_suc += 1
                except Exception as e:
                    print traceback.print_exc()
                    print("运行失败,%s[%s],命令为[%s]"%(dtype_name,name,sql))
            else:
                print(">>>> 未运行,删除%s[%s],命令为[%s]"%(dtype_name,name,sql))
        print("共运行%s数量[%d],成功运行数量[%d],失败运行数量[%d]"%(dtype_name,count,count_suc,count-count_suc))
        return True 
        


    def re_create_table(ORM):
        u""" 单表重建 """
        try:
            ORM.__table__.drop(current_engine)
        except Exception ,e:
            print u"表不存在"
            #print Exception ,e
        ORM.__table__.create(current_engine)
        return True
    
    def re_create_tables(ORMS):
        u""" 多表重建 """
        for orm in ORMS:
            try:
                orm.__table__.drop(current_engine)
                pass
            except Exception ,e:
                print u"表不存在"
                #print Exception ,e
        ORMS.reverse()
        for orm in ORMS:
            orm.__table__.create(current_engine)
        return True

def test():
    oracle_tool = Oracle_Tool()
    table_names = oracle_tool.get_all_user_table_names(user='fdm')
    sequence_names = oracle_tool.get_all_use_sequence_names(user='fdm')
    oracle_tool.drop_tabs_seqs(names=table_names,run_flag=True,dtype='table')
    oracle_tool.drop_tabs_seqs(names=sequence_names,run_flag=True,dtype='sequence')
        

    

if __name__ == '__main__':
    oracle_tool = Oracle_Tool()

    pass

