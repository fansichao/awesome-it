# Python命令

## Python 字典根据 Value顺序排序
sort_sum  = sorted(sum_dic.items(),key=lambda item:item[1],reverse=False)
[('北京', 714),
 ('上海', 660),]

## 获取os.system(cmd)的执行结果

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

## print同行替换输出 输出信息再同一行 进度条显示
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
## Python生成md5
```python
import md5
src = 'this is a md5 test.'
m1 = md5.new()
m1.update(src)
print m1.hexdigest()
```

## Excel处理

在用xlrd.open_workbook时，添加对应的参数formatting_info=True，就可以保留原有格式了


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

## Python由Value取Key

说明：
	* 不同key同value，转换中必然存在问题。
	* 不同方法不是完全可行的，仅仅做参考。

```python
# 测试数据
student = {'a': '1', 'b': '1', 'c': 2, 'd': [1, 2]}
# 方法2 调用函数
def get_key (dict, value):    
    return [k for k, v in dict.items() if v == value]
# 测试说明
In [37]: get_key(student,1)Out[37]: []
In [38]: get_key(student,'1')Out[38]: ['a', 'b']
In [39]: get_key(student,[1,2])Out[39]: ['d']
```
## python中检测某个变量是否有定义

参考链接：http://www.cnblogs.com/starspace/archive/2008/12/03/1347007.html
```python
第一种方法：      
'var'   in   locals().keys()
第二种方法：    
try:         
    print   var    
except   NameError:         
    print   'var   not   defined'
第三种方法：      'var'   in   dir()
```


## 判断list列表是否包含Flase布尔值 any/all

Python内置函数any(iterable)可以用来判断列表里是否存在元素可以使bool(element)为True
```python
>>> l= [None, 1, 0]
>>> any(l)
True
>>> all(l)
False
```


### 去除list重复值

myList = list(set(myList))



### 使用traceback获取栈信息

traceback.print_exc()
获取详细的程序异常信息。
程序运行异常时会输出完整的栈信息，包括调用顺序、异常发生的语句、错误类型等。
import tarceback

try:
     f()
except IndexError as ex:
     print "程序异常"
     print ex
     print traceback.print_exc()#1.错误类型（IndexError）、错误对应的值（list index out of range）、具体的trace信息(文件名 行号 函数名 对应的代码)

sys.exc_info()

### 使用dir获取模块的方法dir()

dir(traceback)