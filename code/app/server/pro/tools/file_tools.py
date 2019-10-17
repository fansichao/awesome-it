#! -*- coding:utf-8
u""" 文件处理

"""
import os
import shutil
 


def file_deal():
    os.remove(path)   #删除文件
    os.removedirs(path)   #删除空文件夹
    shutil.rmtree(path)  #递归删除文件夹

import os,shutil
def copy_file(srcfile,dstfile):
    u""" 复制文件/目录

    :param srcfile: 源文件
    :param dstfile: 目标文件
    
    """
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath=os.path.dirname(srcfile)    #获取文件路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #没有就创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件到默认路径
        print ("copy %s -> %s"%( srcfile,os.path.join(fpath,dstfile)))  


def listdir(path, list_name=[], post_fix=".md"):  
    u"""列出目录下所有文件名称
    """
    for file in os.listdir(path):  
        file_path = os.path.join(path, file)  
        if os.path.isdir(file_path):  
            listdir(file_path, list_name)  
        elif os.path.splitext(file_path)[1]==post_fix:  
            list_name.append(file_path)  
    return list_name

if __name__ == '__main__':

    path = "/vscode/awesome-it/docs"
    list_name = listdir(path)
    for name in list_name:
        basename = os.path.basename(name)
        strs = "- [%s](https://github.com/fansichao/awesome-it/blob/master/docs/%s)"%(basename ,basename)
        print strs


