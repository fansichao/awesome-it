#! -*- coding:utf-8 -*-

import os
import shutil

def listdir(path, list_name=[], post_fix=".md"):  
    u"""列出目录下所有文件名称
    """
    print(">>>>>>>>>> 1")
    print(path)

    print(os.listdir(path))
    for file in os.listdir(path):  
        file_path = os.path.join(path, file)  
        if os.path.isdir(file_path):  
            listdir(file_path, list_name)  
        elif os.path.splitext(file_path)[1]==post_fix:  
            list_name.append(file_path)  
    return list_name


def get_all_dirs(path='.'):
    u""" 获取指定路径下所有目录
    """
    return [file for file in os.listdir(path) if os.path.isdir(os.path.join(path, file))]

if __name__ == '__main__':

    path = "/vscode/awesome-it/docs"

    ll = ['@', 'Linux软件','Linux基础','Python基础','Python内置包','Python进阶','Python三方包','Win']

    # for l in ll:
    #     if l == '@':
    #         print "## 文档目录"
    #     else:
    #         print "## %s"%l
    #     print ""
    #     for name in list_name:
    #         basename = os.path.basename(name)
    #         strs = "- [%s](https://github.com/fansichao/awesome-it/blob/master/docs/%s)"%(basename ,basename)
    #         if basename.startswith(l):
    #              print strs
    #     print ""

    # TODO 不支持多层目录
    all_dir = bool([]) or get_all_dirs(path=path)
    for one_dir in all_dir:
        one_dir_path = os.path.join(path, one_dir)
        # file_name_lis = listdir(one_dir_path)
        file_name_lis = os.listdir(one_dir_path)

        print(f"## {one_dir}")
        print("")
        for file_name in file_name_lis:
            basename = os.path.basename(file_name)
            strs = "- [%s](https://github.com/fansichao/awesome-it/blob/master/docs/%s/%s)"%(basename, one_dir, basename)
            print(strs)
        print("")


        




