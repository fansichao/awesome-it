#! -*- coding:utf-8 -*-
u"""
    装饰器代码

整合所有可以被封装的装饰器，便于后续调用

"""
import time
import datetime
import functools

###############
#### 接口函数
###############
def decorator_func(text="all",*args,**kwargs):
    u""" 统计函数相关信息 All
    - 函数运行时间
    - 函数名称

    """
    def decorator(func,*args,**kwargs):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            start = datetime.datetime.now()
            data = func(*args, **kwargs)
            runtime = datetime.datetime.now() - start
            msg = "@函数运行信息: 函数类型[%s],函数名称[%s],运行时间[%s秒]"%(text,func.__name__,runtime.total_seconds())
            print(msg)
            msg2 = "@展示信息args[%s],kwargs[%s]"%(str(args),str(kwargs))
            print(msg2)
            return data
        return wrapper
    return decorator

###############
#### 基础函数
###############
class Decorator(object):
    u"""
        装饰器类
    """
    def __init__(self, func):
        self.func = func

    # __call__()是一个特殊方法，它可将一个类实例变成一个可调用对象
    def __call__(self, *args, **kwargs):
        print("decorator start")
        self.func()
        print("decorator end")


if __name__ == '__main__':
    #@decorator_func("all")
    @Decorator
    @decorator_func("all")
    def a(b="cc"):
        for i in range(2):
            time.sleep(1)
        print "函数运行...."
        return b
    a()






