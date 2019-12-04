# -*- coding: utf-8 -*-
 
'''
@Author: Scfan
@LastEditors: Scfan
@LastEditTime: 2018-12-05 17:53:12
@LastEditTime: 2018-12-20 21:10:44
@Description: 工作&amp;学习&amp;生活
@Email: 643566992@qq.com
@Company: 上海
@version: V1.0

生成文件目录树 & github目录结构
    python Code\dirtree.py ：打印当前目录的目录树；
    python Code\dirtree.py D:\\@vscode ：打印指定目录的目录树；
    python Code\dirtree.py D:\\@vscode dirtree.txt ：打印指定目录的目录树并保存成文件。
'''
home_dir = 'D:\\@vscode\\'

import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

from pathlib import Path

# github 有目录/无目录 文件实际路径
github_hav_dir_url = 'https://github.com/fansichao/Study/tree/master/'
github_not_dir_url = 'https://github.com/fansichao/Study/blob/master/'

class DirectionTree(object):
    """生成目录树
    @ pathname: 目标目录
    @ filename: 要保存成文件的名称
    """
 
    def __init__(self, pathname='.', filename='tree.txt'):
        super(DirectionTree, self).__init__()
        self.pathname = Path(pathname)
        self.filename = filename
        self.tree = ''
        self.href = ''
        self.github_hav_dir_url = github_hav_dir_url
        self.github_not_dir_url = github_not_dir_url
        self.home_dir_dirnames = self.get_base_dir(home_dir)
        self.not_contain_str = ['.git','.vscode','Private']
 
    def set_path(self, pathname):
        self.pathname = Path(pathname)
 
    def set_filename(self, filename):
        self.filename = filename

    def get_base_dir(self,filepath):
        '''
        @msg: 获取文件路径的所有子目录/文件
        filepath = 'D:\@vscode\Code\dirtree.py'
        @return: [WindowsPath('D:/'), '@vscode', 'Code', 'dirtree.py']
        '''
        import copy
        filepath = Path(filepath)
        dirnames = []
        dirname = copy.deepcopy(filepath)
        for i in range(10):
            dir1 = dirname.parent
            name1 = dirname.name
            dirname = copy.deepcopy(dir1)
            if name1 not in dirnames and bool(name1):
                dirnames.insert(0, name1)
            if i == 9:
                dirnames.insert(0, dir1)
        return dirnames

    def generate_tree(self, n=0):
        if self.pathname.is_file():
            dirnames = self.get_base_dir(self.pathname)
            # self.home_dir_dirnames [WindowsPath('D:/'), '@vscode']
            for i in self.home_dir_dirnames:
                # dirnames ['Code', 'dirtree.py']
                dirnames.pop(dirnames.index(i))

            name = self.pathname.name
            self.tree += '    |' * n + '-' * 4 + name + '\n'
            # path_name Code/dirtree.py
            path_name = '/'.join(dirnames)
            self.href += '    '*n + '- [%s](%s)'%(name,self.github_not_dir_url+path_name) + '\n'

        elif self.pathname.is_dir():
            name = str(self.pathname.relative_to(self.pathname.parent))
            self.tree += '    |' * n + '-' * 4 + name + '\\' + '\n'     
            if not bool(self.href):
                self.href += '    '*n + '- [%s](%s)'%(name,self.github_hav_dir_url+'') + '\n'
            else:
                self.href += '    '*n + '- [%s](%s)'%(name,self.github_hav_dir_url+name) + '\n' 

            for cp in self.pathname.iterdir():
                if bool([i for i in self.not_contain_str if str(cp).find(i) != -1]):
                    continue
                self.pathname = Path(cp)
                self.generate_tree(n + 1)
 
    
    def save_file(self):
        #with open(self.filename, 'w',encoding='utf-8') as f:
        with open(self.filename, 'w') as f:
            f.write(self.tree)
 
if __name__ == '__main__':

    dirtree = DirectionTree()
    # 命令参数个数为1，生成当前目录的目录树
    if len(sys.argv) == 1:
        dirtree.set_path(Path.cwd())
        dirtree.generate_tree()
        print(dirtree.tree)
    # 命令参数个数为2并且目录存在存在
    elif len(sys.argv) == 2 and Path(sys.argv[1]).exists():
        dirtree.set_path(sys.argv[1])
        dirtree.generate_tree()
        print(dirtree.tree)
    # 命令参数个数为3并且目录存在存在
    elif len(sys.argv) == 3 and Path(sys.argv[1]).exists():
        dirtree.set_path(sys.argv[1])
        dirtree.generate_tree()
        dirtree.set_filename(sys.argv[2])
        dirtree.save_file()
        print(dirtree.tree)
    else:  # 参数个数太多，无法解析
        print('命令行参数太多，请检查！')
    
    print(dirtree.href)
 