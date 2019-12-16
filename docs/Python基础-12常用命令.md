# Python 命令



## 获取 os.system(cmd)的执行结果

```python
由于os.system是没有返回值的，获取返回值有以下三种方式：
1.使用commands内置模块
import commands
resp = commands.getoutput("hostname")
2.使用os.popen获取返回值
resp = os.popen('ps -ef | grep sssss').readlines()
3.使用subprocess内置模块
from subprocess import Popen,PIPE
resp = Popen("ps -ef | grep sssss",shell=True,stdout=PIPE,stderr=PIPE).stdout.readlines()
```

## print 同行替换输出 输出信息再同一行 进度条显示

```python
# python3
>>> import time
>>> for x in range(10):
...     time.sleep(1)
...     print("Progress {:2.1%}".format(x / 10), end="\r")
# 下列三行信息输出在同一行
Progress 30.0%
Progress 50.0%
>>> ress 90.0%
# python2
import time
import sys
for x in range(5):
    time.sleep(1)
    msg = ">>>> %s\r"%str(x)
    sys.stdout.write(msg)
    sys.stdout.flush()
```

## python 文件传入 参数

```python
#! /bin/python
import sys
for arg in sys.argv:
    print arg
```

## Python 生成 md5

```python
import md5
src = 'this is a md5 test.'
m1 = md5.new()
m1.update(src)
print m1.hexdigest()
```

## Excel 处理

在用 xlrd.open_workbook 时，添加对应的参数 formatting_info=True，就可以保留原有格式了

## python 通过字符串调用对象属性或方法的实例讲解

```python
# eval
def getmethod(x,char='just for test'):
    return eval('str.%s' % x)(char)
In [635]: getmethod('upper')
Out[635]: 'JUST FOR TEST'
# getattr
In [650]: def getmethod2(x, char='just for test'):...:
    return getattr(char, x)()...:
In [651]: getmethod2('upper')
Out[651]: 'JUST FOR TEST'
# 利用内置库operator
In [648]: def getmethod3(x, char='just for test'):...:
    return operator.methodcaller(x, char)(str)...:
In [649]: getmethod3('upper')
Out[649]: 'JUST FOR TEST'

```





### 使用 traceback 获取栈信息

traceback.print_exc()
获取详细的程序异常信息。
程序运行异常时会输出完整的栈信息，包括调用顺序、异常发生的语句、错误类型等。
import tarceback

try:
f()
except IndexError as ex:
print "程序异常"
print ex
print traceback.print_exc()#1.错误类型（IndexError）、错误对应的值（list index out of range）、具体的 trace 信息(文件名 行号 函数名 对应的代码)

sys.exc_info()

### 使用 dir 获取模块的方法 dir()

dir(traceback)
