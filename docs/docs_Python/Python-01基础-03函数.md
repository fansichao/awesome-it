# Python 基础-03 函数

## 函数

函数是组织好的，可重复使用的，用来实现单一，或相关联功能的代码段。

### 参数

**参数种类:**

- **必备参数** 必备参数须以正确的顺序传入函数。调用时的数量必须和声明时的一样 arg1
- **默认参数** 调用函数时,默认参数的值如果没有传入,则被认为是默认值。 arg1=None
- **不定长参数** 参数长度未知时，使用此参数 \*args
- **未知参数** 参数未知时，使用此参数 \*\*kwargs

```python
def demo1(arg1, arg2, file_path=None, *args, **kwargs):
	pass
```

### 匿名函数 lambda

使用 lambda 来创建匿名函数.

**匿名函数的特点:**

- 表达式简单，只有一行。便于阅读和维护
- 独立命名空间，只能访问 lambda 中的参数
- 只封装简单逻辑，走精简风。

**函数语法:**

```python
# 表达式语法
lambda [arg1 [,arg2,.....argn]]:expression
# 样例
sum = lambda arg1, arg2: arg1 + arg2;
```

### 变量作用域

**变量作用域:**

- 局部作用域: 只作用在某个范围，函数或类中。
- 全局作用域 作用在整个程序中，程序中任何位置都可以读取和修改全局变量，但是不建议项目使用。

```python
global_arg = 0
def demo1(count=0)
	global global_arg
	global_arg += 1
	print("demo1 %d"%global_arg)
	demo2()

def demo2():
	global global_arg
	print("demo2 1 %d"%global_arg)
	global_arg += 1
	print("demo2 2 %d"%global_arg)
# count 是函数demo1中的 局部变量
# global_arg 是程序的全局变量
```

## 类

**类(Class)**: 用来描述具有相同的属性和方法的对象的集合。它定义了该集合中每个对象所共有的属性和方法。对象是类的实例。

类的三大特性： **继承 多态 封装**

http://www.cnblogs.com/ajaxa/p/9049518.html

## 模块

Python 模块(Module)，是一个 Python 文件，以 .py 结尾，包含了 Python 对象定义和 Python 语句。

代码样例

```python
# file demo.py
def func(arg):
	return arg
```

模块的使用

```python
import demo
print demo.func(1)

from demo import func
print func(1)

```

使用 **dir()** 获取模块中所有函数列表

## 包

如果将整个目录作为包，需要目录中含有 **\_\_init\_\_.py** 文件

代码样例

```python
# demo/demo1.py
def get_val(arg):
	return arg

# demo/__init__.py
#! -*- coding:utf-8 -*-

# demo/demo2.py
from demo.demo1 import get_val
def func(arg):
	get_val(arg)
if __name__ == '__main__':
	func(2)
```

将模块当成脚本运行 python -m
python -m demo.demo2

## 文档风格

如下是**reST**文档风格

```python
# 文件中内置包引用，统一管理
import datetime
def demo1(arg1, arg2, file_path=None, *args, **kwargs):
    u""" 函数注释(和下方param空行)

    :param arg1: 参数1  (格式说明  :param+空格+参数+:+空格+参数解释)
    :type arg1: int
    :param arg2: 参数2
    :type arg2: int

    :returns: The return value. True for success, False otherwise.
    :rtype: bool

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

	"""
	# 延迟调用
    import pandas as pd
    if file_path:
    	pd.read_csv(file_path,**kwargs)

    now_time = datetime.datetime.now()
    return arg3 if bool(arg3) else arg1 + arg2

if __name__ == '__main__':
	demo1(1,2)
```

## 参考资源

Python 函数说明 https://www.runoob.com/python/python-functions.html
Python 模块说明 https://www.runoob.com/python/python-modules.html
面向对象 类说明 https://www.runoob.com/python3/python3-class.html
类的详解 https://blog.csdn.net/weixin_42105064/article/details/80151587
