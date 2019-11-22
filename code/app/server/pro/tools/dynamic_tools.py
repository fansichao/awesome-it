# -* - coding: UTF-8 -* -
u""" 动态文件


动态配置 Python 等

- 动态创建 变量
- 动态创建 函数

- 动态调用 函数
- 动态调用 函数
- ...

exp:
- https://www.cnblogs.com/technologylife/p/9211324.html
"""
import sys
import os
from types import FunctionType

import inspect


def dynamic_cre_func(func_name, func_str):
    u""" 动态创建函数

    :param func_str:
    :return:

    exp:
        https://www.jb51.net/article/158464.htm
    """
    foo_code = compile('def foo(): return "bar"', "<string>", "exec")
    foo_func = FunctionType(foo_code.co_consts[0], globals(), "foo")

    print(foo_func())


def dynamic_cre_var(var_name, var_val):
    u""" 动态创建变量

    :param var_name: 变量名称
    :param var_val:  变量值
    :return:
    """
    var_name = 'a1'
    var_val = "a2"

    names = locals()
    names[var_name] = val_val

    print(a1)
    print(names.get('a1', end=' '))
    return names


class TestClass(object):
    u"""
    类中动态创建变量
    """

    def __init__(self):
        names = self.__dict__
        for i in range(5):
            names['n' + str(i)] = i


t = TestClass()
print(t.n0, t.n1, t.n2, t.n3, t.n4)


class TestClass1(object):
    u"""
    类中动态创建变量
    """

    def __init__(self):
        dic = {'a': '123', 'b': '456'}
        for key in dic.keys():
            setattr(self, key, dic[key])  # 第一个参数是对象，这里的self其实就是test.第二个参数是变量名，第三个是变量值
        print(self.a)
        print(self.b)


t = TestClass1()


def get_variable_name(variable_val):
    u""" 根据变量值获取变量名


    https://testerhome.com/topics/19633
    得到Python变量名是困难的。那么，为什么无法直接得到Python变量名呢？查阅相关资料后发现，
    在Python中，变量名字是对象(object)的单向(而不是双向)引用。也就是说，根据变量名，能够直接得到它所指向的对象；反之，根据对象，是无法得到指向它的变量名的。
    之所以有这么一个规定，是基于成本考虑的。在程序中，往往存在大量的变量(整型，字符串，列表，字典，布尔...)。
    如果每一个变量都需要有一个包含指向它的变量名的列表，那么这些列表的创建和维护的成本(实现成本，执行成本...)将变得难以承受。

    :param variable_val: 变量值
    :return:
    """
    # TODO 根据变量值来获取变量名称，不一定准确, 无实际意义
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is variable_val]


def get_variable_val(variable_name, variable_list=[]):
    u""" 根据变量名获取变量值

    :param variable_name: 变量名称
    :param variable_list: 变量列表
    :return: exp: [('myvar', 12)]
    """

    def var_append(name, list_):
        list_.append((name, sys._getframe().f_back.f_locals[name]))
        return list_

    return var_append(variable_name, variable_list)


def get_current_function_name():
    u""" 获得当前函数名称
    """
    func_name = sys._getframe().f_code.co_name
    print(func_name)
    return func_name 


# 使用inspect模块动态获取当前运行的函数名（或方法名称）

# coding:utf-8
import inspect

def get__function_name():
    '''获取正在运行函数(或方法)名称'''
    return inspect.stack()[1][3]

def yoyo():
    print("函数名称：%s"%get__function_name())

class Yoyo():
    def yoyoketang(self):
        print("获取当前类名称.方法名：%s.%s" % (self.__class__.__name__, get__function_name()))

# if __name__ == "__main__":
#     yoyo()
#     Yoyo().yoyoketang()
# 运行结果：
# 
# 函数名称：yoyo
# 获取当前类名称.方法名：Yoyo.yoyoketang

if __name__ == '__main__':
    a = 's'
    b = 's'
    print(get_variable_name(a))
