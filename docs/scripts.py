#! -*- coding:utf-8 -*-

import os
import shutil

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

    ll = ['@', 'Linux软件','Linux基础','Python基础','Python内置包','Python进阶','Python三方包','Win']

    for l in ll:
        if l == '@':
            print "## 文档目录"
        else:
            print "## %s"%l
        print ""
        for name in list_name:
            basename = os.path.basename(name)
            strs = "- [ ] [%s](https://github.com/fansichao/awesome-it/blob/master/docs/%s)"%(basename ,basename)
            if basename.startswith(l):
                print strs
        print ""


        




