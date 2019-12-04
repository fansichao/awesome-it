#!/usr/bin/python
# -*- coding: utf-8 -*-
u"""
PDF API代码

PDF模块
- PyPDF2
- pdfminer



"""
class Pdf_Api(object):
    u""" PDF API 接口 """
    def __init__(self):
        u" 初始化 "
        import PyPDF2

        self.pdf_filename = '2.pdf'
        pass
    def pdf_read(self):
        u" 读取pdf "

        pdfFileObj = open(self.pdf_filename,'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
         
        pdf_nums = pdfReader.numPages
        pageObj = pdfReader.getPage(0) 
        pdf_data = pageObj.extractText()

    def pdf_decrypt(self, password=None):
        u" PDF解密 "
        pdfFile = open('encrypted.pdf','rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFile)
 
        #返回True说明时加密的PDF
        pdfReader.isEncrypted
        >>True
        # 调用decrypt()函数，传入口令字符串，返回1说明口令正确，之后就可以进行读取操作了
        if pdfReader.decrypt(password) == 1:
            print("文档:%s,密码:%s 输入正确,解密成功"%(self.pdf_filename,password))
        else:
            print("文档:%s,密码:%s 输入错误,解密失败"%(self.pdf_filename,password))
        pdfReader.getPage(0).extractText()

        # decrypt()函数只解密了PdfFileReader对象






