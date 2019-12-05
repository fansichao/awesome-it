#! -*- coding:utf-8 -*-
u"""
    Excel_Api/Csv_Api 模块 

- read_xlsx     读取Excel
- write_xlsx    写入Excel

@Author: Scfan
@Date: 2019-01-11 16:17:44
@LastEditors: Scfan
@LastEditTime: 2019-01-11 16:20:11
@Description: 工作&amp;学习&amp;生活
@Email: 643566992@qq.com
@Company: 上海
@version: V1.0

"""

import csv
from collections import OrderedDict

import openpyxl
import pandas as pd
# pyexcel_xls 以 OrderedDict 结构处理数据
import xlrd
import xlwt
from pyexcel_xls import get_data, save_data
from xlrd import xldate_as_tuple
from xlutils.copy import copy as xlutil_copy

import base_import


class Excel_Api(object):
    u""" Spark 相关基础函数
    Spark_Excel_ApiBase_Func 基础函数
        - read_xlsx 读取Excel文件
        - read_excel_simple 简单读取Excel
        - read_csv  读取csv文件
        - write_csv 写入csv文件
        - write_xlsx 写入xlsx
        - delete_sheet 删除sheet
        - main_test 测试函数入口
    """

    def __init__(self):
        # csv reader/writer 参数说明
        self.csv_default_kv = {
            # 分隔符
            'delimiter': ',',
            'doublequote': True,
            # 逃避分隔符
            'escapechar': None,
            # 行尾识别符
            'lineterminator': '\r\n',
            # 包含符
            'quotechar': '"',
            'quoting': csv.QUOTE_MINIMAL,
            # 忽略分隔符后面的空格
            'skipinitialspace': False,
            # 忽略异常
            'strict': False,
        }

    # 读取
    def read_xlsx(self, file_path="input.xlsx", sheet_name=None):
        """ 读取xlsx文件内容
        @param file_path: 文件名称
        @param sheet_name: 表格名称，None时，默认取第一个
        """
        if not bool(file_path) or os.path.exists(file_path):
            print(">>>> 文件不存在[%s]" % file_path)
            return

        try:
            file_path = file_path.decode('utf-8')
            sheet_name = sheet_name.decode('utf-8')
        except Exception:
            print traceback.print_exc()

        # rbook = xlrd.open_workbook(file_path,formatting_info=True) # 保留excel样式
        rbook = xlrd.open_workbook(file_path)
        # 所有 sheet_name
        sheet_names = rbook.sheet_names()
        sheet_name = sheet_names[0] if not bool(sheet_name) else sheet_name
        if sheet_name not in sheet_names:
            print(">>>> 表名称[%s]不存在文件[%s]所有表[%s]中" %
                  (sheet_name, file_path, sheet_names))
            return

        sheet = rbook.sheet_by_name(sheet_name)
        rows = sheet.nrows
        cols = sheet.ncols
        all_content = []
        for i in range(rows):
            row_content = []
            for j in range(cols):
                ctype = sheet.cell(i, j).ctype  # 表格的数据类型
                cell = sheet.cell_value(i, j)
                if ctype == 2 and cell % 1 == 0:  # 如果是整形
                    cell = int(cell)
                elif ctype == 3:
                    # 转成datetime对象
                    date = datetime.datetime(*xldate_as_tuple(cell, 0))
                    a = date.strftime('%Y-%m-%d %H:%M:%S')
                    cell = str(a).split(' ')[0]
                    # cell = date.strftime('%Y/%d/%m %H:%M:%S')
                elif ctype == 4:
                    cell = True if cell == 1 else False
                row_content.append(cell)
            all_content.append(row_content)
            # print '[' + ','.join("'" + str(element) + "'" for element in row_content) + ']'
        return all_content

    def read_excel_simple(self, file_name, sheet_name):
        ''' 简答读取 excel
        '''
        # 打开文件
        # ,formatting_info=True  formatting_info 保留原有格式
        workbook = xlrd.open_workbook(file_name, formatting_info=True)
        # 获取所有 sheet名称
        # print workbook.sheet_names()
        # 根据 sheet索引或者名称获取 sheet内容
        # sheet_data = workbook.sheet_by_index(1) # sheet索引从0开始
        sheet_data = workbook.sheet_by_name(sheet_name)
        return sheet_data

    def read_csv(self, file_path, **kv):
        ''' 读取csv 
        @description: 
        @param {type} 
        @return: 
        '''
        # 删除 无效key
        for k in kv.keys():
            if k not in self.csv_default_kv.keys():
                del kv[k]
        default_kv = copy.deepcopy(self.csv_default_kv)
        default_kv.update(kv)
        rows = list()
        # 文件读取
        import codecs
        csv_file = codecs.open(file_path, 'r', kv.get('encoding', 'utf-8'))
        reader = csv.reader(csv_file, **default_kv)
        # 读取的行数
        if kv.get('line_num'):
            reader = reader.line_num(int(kv['line_num']))

        for user in reader:
            rows.append(user)
        csv_file.close()
        return rows

       # with open(filename, 'r') as csv_file:
       #     reader = csv.reader(csv_file,**default_kv)
       #     # 读取的行数
       #     if kv.get('line_num'):
       #         reader = reader.line_num(int(kv['line_num']))

       #     for user in reader:
       #         rows.append(user)
       #     return rows

    # 写入
    def write_csv(self, file_path, rows, **kv):
        u"""
        # 生成 竖线分隔，存放在一个单元格中
        :param file_path:文件名称
        :param rows:数据格式 [row,row,row,,,,]
        :return:None
        """
        # 删除 无效key
        for k in kv.keys():
            if k not in self.csv_default_kv.keys():
                del kv[k]
        default_kv = copy.deepcopy(self.csv_default_kv)
        default_kv.update(kv)

        import codecs
        csvfile = codecs.open(file_path, 'ab', kv.get('encoding', 'utf-8'))
        writer = csv.writer(csvfile, **default_kv)
        for row in rows:
            writer.writerow(row)
        csvfile.close()
        # with open(file_path, 'ab') as csvfile:
        #    writer = csv.writer(csvfile,**default_kv)
        #    for row in rows:
        #        writer.writerow(row)
        print(">>>> 文件[%s]保存成功" % file_path)

    def write_xlsx(self, input_file, output_file, sheet_name, rows):
        u"""excel写入公用函数"""
        a = datetime.datetime.now()

        input_file = self.delete_sheet(input_file,sheet_name)

        old_xls = xlrd.open_workbook(input_file, formatting_info=True)
        new_xls = xlutil_copy(old_xls)
        sheet_names = old_xls.sheet_names()
        if sheet_name not in sheet_names:
            new_xls.add_sheet(sheet_name)
        #sheet_data = new_xls.sheet_by_name(sheet_name)

        for i in range(len(rows)):
            row = rows[i]
            for j in range(len(row)):
                new_xls.get_sheet(sheet_name).write(i, j, row[j])
        new_xls.save(output_file)
        b = datetime.datetime.now()
        print b - a

    # 处理
    def delete_sheet(self, input_file, sheet_name):
        u"删除已经存在的sheet"
        old_xls = xlrd.open_workbook(input_file, formatting_info=True)
        sheet_names = old_xls.sheet_names()

        if sheet_name in sheet_names:
            wb = openpyxl.Workbook(input_file)
            wb.remove_sheet(wb.get_sheet_by_name(sheet_name))
            wb.save(input_file)
        return input_file

    # 测试
    def main_test(self, *lis, **kv):
        u""" 测试函数 入口
        """
        local_path = kv.get('local_path') or '/home/scfan/tmp/record.csv'
        write_path = kv.get('write_path') or '/home/scfan/tmp/record_w.csv'
        local_xlsx_path = kv.get(
            'local_xlsx_path') or '/home/scfan/tmp/record.xlsx'

        # 读取 csv
        data = self.read_csv(local_path)
        # 写入 csv
        self.write_csv(write_path, data)
        # 读取 xlsx
        #data = self.read_xlsx(local_xlsx_path)


if __name__ == '__main__':
    excel_api = Excel_Api()
    excel_api.main_test()
