---
title: Python基础-00菜鸟教程.md
tags: 2019年 08月 10号
notebook: 00技术笔记
---

## Python-菜鸟驿站

[toc]

## 简介说明  

以下全文来自于[菜鸟驿站官网](http://www.runoob.com/python/python-tutorial.html)，如需跳转请点击。

各类程序员学习路线图：http://www.runoob.com/coder-learn-path

学习资料站点地图：http://www.runoob.com/sitemap

### Python简介
Python是一种解释型、面向对象、动态数据类型的高级程序设计语言。
Python由Guido van Rossum于1989年底发明，第一个公开发行版发行于1991年。
像Perl语言一样, Python 源代码同样遵循 GPL(GNU General Public License)协议。

Python 是一个高层次的结合了**解释性、编译性、互动性和面向对象**的脚本语言。
Python 的设计具有很强的可读性，相比其他语言经常使用英文关键字，其他语言的一些标点符号，它具有比其他语言更有特色语法结构。

Python 是一种解释型语言： 这意味着开发过程中没有了编译这个环节。类似于PHP和Perl语言。

Python 是交互式语言： 这意味着，您可以在一个Python提示符，直接互动执行写你的程序。

Python 是面向对象语言: 这意味着Python支持面向对象的风格或代码封装在对象的编程技术。

Python 是初学者的语言：Python 对初级程序员而言，是一种伟大的语言，它支持广泛的应用程序开发，从简单的文字处理到 WWW 浏览器再到游戏。


### Python 发展历史
Python 是由 Guido van Rossum 在八十年代末和九十年代初，在荷兰国家数学和计算机科学研究所设计出来的。
Python 本身也是由诸多其他语言发展而来的,这包括 ABC、Modula-3、C、C++、Algol-68、SmallTalk、Unix shell 和其他的脚本语言等等。
像 Perl 语言一样，Python 源代码同样遵循 GPL(GNU General Public License)协议。
现在 Python 是由一个核心开发团队在维护，Guido van Rossum 仍然占据着至关重要的作用，指导其进展。

### Python 特点
1. 易于学习：Python有相对较少的关键字，结构简单，和一个明确定义的语法，学习起来更加简单。
2. 易于阅读：Python代码定义的更清晰。
3. 易于维护：Python的成功在于它的源代码是相当容易维护的。
4. 一个广泛的标准库：Python的最大的优势之一是丰富的库，跨平台的，在UNIX，Windows和Macintosh兼容很好。
5. 互动模式：互动模式的支持，您可以从终端输入执行代码并获得结果的语言，互动的测试和调试代码片断。
6. 可移植：基于其开放源代码的特性，Python已经被移植（也就是使其工作）到许多平台。
7. 可扩展：如果你需要一段运行很快的关键代码，或者是想要编写一些不愿开放的算法，你可以使用C或C++完成那部分程序，然后从你的Python程序中调用。
8. 数据库：Python提供所有主要的商业数据库的接口。
9. GUI编程：Python支持GUI可以创建和移植到许多系统调用。
10. 可嵌入: 你可以将Python嵌入到C/C++程序，让你的程序的用户获得"脚本化"的能力。


### Python环境变量

**PYTHONPATH**
是Python搜索路径，默认我们import的模块都会从PYTHONPATH里面寻找。

**PYTHONSTARTUP**
Python启动后，先寻找PYTHONSTARTUP环境变量，然后执行此变量指定的文件中的代码。

**PYTHONCASEOK**
加入PYTHONCASEOK的环境变量, 就会使python导入模块的时候不区分大小写.

**PYTHONHOME**
另一种模块搜索路径。它通常内嵌于的PYTHONSTARTUP或PYTHONPATH目录中，使得两个模块库更容易切换。


**#!/usr/bin/python **: 
是告诉操作系统执行这个脚本的时候，调用 /usr/bin 下的 python 解释器；

**#!/usr/bin/env python(推荐）**: 
这种用法是为了防止操作系统用户没有将 python 装在默认的 /usr/bin 路径里。
当系统看到这一行的时候，首先会到 env 设置里查找 python 的安装路径，再调用对应路径下的解释器程序完成操作。

#!/usr/bin/python 相当于写死了python路径;

#!/usr/bin/env python 会去环境设置寻找 python 目录,推荐这种写法

### Python运行参数

Python启动交互式界面参数。
```python
$ python # Unix/Linux
```

- -d 在解析时显示调试信息
- -O 生成优化代码 ( .pyo 文件 )
- -S 启动时不引入查找Python路径的位置
- -V 输出Python版本号
- -X 从 1.6版本之后基于内建的异常（仅仅用于字符串）已过时。
- -c cmd 执行 Python 脚本，并将运行结果作为 cmd 字符串。
- file 在给定的python文件执行python脚本。

### Python保留字符

Python 保留字符下面的列表显示了在Python中的保留字。这些保留字不能用作常数或变数，或任何其他标识符名称。
所有 Python 的关键字只包含小写字母。

and exec not assert finally or

break for pass class from print

continue global raise def if 

return del import try elif in

while else is with except lambda yield

## Python函数
### Python数学函数

数学函数需要导入 math或cmath包
```python
improt math
```

| 函数 | 返回值 ( 描述 ) | 
| ------ | ------ |
|abs(x)        |返回数字的绝对值，如abs(-10) 返回 10                                             |
|ceil(x)         |返回数字的上入整数，如math.ceil(4.1) 返回 5                                      |
|cmp(x, y)    |如果 x < y 返回 -1, 如果 x == y 返回 0, 如果 x > y 返回 1                        |
|exp(x)          |返回e的x次幂(ex),如math.exp(1) 返回2.718281828459045                             |
|fabs(x)         |返回数字的绝对值，如math.fabs(-10) 返回10.0                                      |
|floor(x)        |返回数字的下舍整数，如math.floor(4.9)返回 4                                      |
|log(x)          |如math.log(math.e)返回1.0,math.log(100,10)返回2.0                                |
|log10(x)        |返回以10为基数的x的对数，如math.log10(100)返回 2.0                               |
|max(x1, x2,...) |返回给定参数的最大值，参数可以为序列。                                           |
|min(x1, x2,...) |返回给定参数的最小值，参数可以为序列。                                           |
|modf(x)         |返回x的整数部分与小数部分，两部分的数值符号与x相同，整数部分以浮点型表示。       |
|pow(x, y)       |x**y 运算后的值。                                                                |
|round(x [,n])   |返回浮点数x的四舍五入值，如给出n值，则代表舍入到小数点后的位数。                 |
|sqrt(x)         |返回数字x的平方根                                                                |

### Python随机数函数
随机数可以用于数学，游戏，安全等领域中，还经常被嵌入到算法中，用以提高算法效率，并提高程序的安全性。

**Python包含以下常用随机数函数：**

| 函数 | 返回值 ( 描述 ) | 
| ------ | ------ |
|choice(seq)|从序列的元素中随机挑选一个元素，比如random.choice(range(10))，从0到9中随机挑选一个整数|
|randrange ([start,] stop [,step])|从指定范围内，按指定基数递增的集合中获取一个随机数，基数缺省值为1|
|random()|随机生成下一个实数，它在[0,1)范围内。|
|seed([x])|改变随机数生成器的种子seed。如果你不了解其原理，你不必特别去设定seed，Python会帮你选择seed。|
|shuffle(lst)|将序列的所有元素随机排序|
|uniform(x, y)|随机生成下一个实数，它在[x,y]范围内。|


### Python三角函数
| 常量 | 返回值 ( 描述 ) | 
|:-: |:-:|
|cos(x)|返回x的反余弦弧度值。|
|asin(x)|返回x的反正弦弧度值。|
|atan(x)|返回x的反正切弧度值。|
|atan2(y, x)|返回给定的X及Y坐标值的反正切值。|
|cos(x)|返回x的弧度的余弦值。|
|hypot(x, y)|返回欧几里德范数sqrt(x\*x + y\*y)。|
|sin(x)|返回的x弧度的正弦值。|
|tan(x)|返回x弧度的正切值。|
|degrees(x)|将弧度转换为角度,如degrees(math.pi/2),返回90.0|
|radians(x)|将角度转换为弧度|


### Python数学常量

| 常量 | 返回值 ( 描述 ) | 
| ------ | ------ |
|pi|数学常量 pi（圆周率，一般以π来表示）|
|e|数学常量 e，e即自然常数（自然常数）。|


### 匿名函数

python 使用 lambda 来创建匿名函数。
lambda只是一个表达式，函数体比def简单很多。
lambda的主体是一个表达式，而不是一个代码块。仅仅能在lambda表达式中封装有限的逻辑进去。
lambda函数拥有自己的命名空间，且不能访问自有参数列表之外或全局命名空间里的参数。
虽然lambda函数看起来只能写一行，却不等同于C或C++的内联函数，后者的目的是调用小函数时不占用栈内存从而增加运行效率。
```python
语法lambda函数的语法只包含一个语句，如下：
lambda [arg1 [,arg2,.....argn]]:expression

sum = lambda arg1, arg2: arg1 + arg2;
# 调用sum函数
print "相加后的值为 : ", sum( 10, 20 )
```





## Python 异常

### 异常说明

异常即是一个事件，该事件会在程序执行过程中发生，影响了程序的正常执行。
一般情况下，在Python无法正常处理程序时就会发生一个异常。
异常是Python对象，表示一个错误。
当Python脚本发生异常时我们需要捕获处理它，否则程序会终止执行。

捕捉异常可以使用try/except语句。
try/except语句用来检测try语句块中的错误，从而让except语句捕获异常信息并处理。
如果你不想在异常发生时结束你的程序，只需在try里捕获它。
语法：
以下为简单的try....except...else的语法：
```python
try:
<语句> #运行别的代码
except <名字>：
<语句> #如果在try部份引发了'name'异常
except <名字>，<数据>:
<语句> #如果引发了'name'异常，获得附加的数据
else:
<语句> #如果没有异常发生
```

### 异常处理
#### 指定标准异
对指定标准异常进行解释。只能识别之地指定标准异常。
```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
try:
    fh = open("testfile", "w")
    fh.write("这是一个测试文件，用于测试异常!!")
except IOError:
    print "Error: 没有找到文件或读取文件失败"
else:
    print "内容写入文件成功"
    fh.close()
```
#### 使用except不带异常类型
可以捕获所有异常，但是无法识别出具体异常信息。


#### 使用except带多种异常类型
捕获多个标准异常
```python
try:
    正常的操作
except(Exception1[, Exception2[,...ExceptionN]]]):
    发生以上多个异常中的一个，执行这块代码
else:
    如果没有异常执行这块代码
```
#### Try-finally语句
try-finally 语句无论是否发生异常都将执行最后的代码。
退出try时总会执行finally中语句。
```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
try:
    fh = open("testfile", "w")
    fh.write("这是一个测试文件，用于测试异常!!")
finally:
    print "Error: 没有找到文件或读取文件失败"
```
#### 异常的参数
一个异常可以带上参数，可作为输出的异常信息参数。
你可以通过except语句来捕获异常的参数，如下所示
```python
try:
    正常的操作
except ExceptionType, Argument:
    你可以在这输出 Argument 的值...
    变量接收的异常值通常包含在异常的语句中。在元组的表单中变量可以接收一个或者多个值。
    元组通常包含错误字符串，错误数字，错误位置。实例
    以下为单个异常的实例：

#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 定义函数
def temp_convert(var):
    try:
        return int(var)
    except ValueError, Argument:
        print "参数没有包含数字\n", Argument

# 调用函数
temp_convert("xyz");
以上程序执行结果如下：
$ python test.py
参数没有包含数字
invalid literal for int() with base 10: 'xyz'触发异常
```
#### raise触发异常
我们可以使用raise语句自己触发异常
raise语法格式如下：
raise [Exception [, args [, traceback]]]
语句中 Exception 是异常的类型（例如，NameError）参数标准异常中任一种，args 是自已提供的异常参数。
最后一个参数是可选的（在实践中很少使用），如果存在，是跟踪异常对象。实例
一个异常可以是一个字符串，类或对象。 Python的内核提供的异常，大多数都是实例化的类，这是一个类的实例的参数。
定义一个异常非常简单，如下所示：
```python
def functionName( level ):
if level < 1:
raise Exception("Invalid level!", level)
# 触发异常后，后面的代码就不会再执行
注意：为了能够捕获异常，"except"语句必须有用相同的异常来抛出类对象或者字符串。
例如我们捕获以上异常，"except"语句如下所示：

try:
正常逻辑
except Exception,err:
触发自定义异常
else:
其余代码实例

#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 定义函数
def mye( level ):
if level < 1:
raise Exception,"Invalid level!"
# 触发异常后，后面的代码就不会再执行
try:
mye(0) # 触发异常
except Exception,err:
print 1,err
else:
print 2
执行以上代码，输出结果为：

$ python test.py
1 Invalid level!
```
#### 用户自定义异常
通过创建一个新的异常类，程序可以命名它们自己的异常。异常应该是典型的继承自Exception类，通过直接或间接的方式。
以下为与RuntimeError相关的实例,实例中创建了一个类，基类为RuntimeError，用于在异常触发时输出更多的信息。
在try语句块中，用户自定义的异常后执行except块语句，变量 e 是用于创建Networkerror类的实例。
```python
class Networkerror(RuntimeError):
def __init__(self, arg):
self.args = arg
在你定义以上类后，你可以触发该异常，如下所示：

try:
raise Networkerror("Bad hostname")
except Networkerror,e:
print e.args
```
### 标准异常说明
菜鸟驿站异常处理: http://www.runoob.com/python/python-exceptions.html

**Python常见标准异常说明**
|异常代码|异常说明| 
|:-|:-:|
|BaseException|所有异常的基类|
|SystemExit|解释器请求退出|
|KeyboardInterrupt|用户中断执行(通常是输入^C)|
|Exception|常规错误的基类|
|StopIteration|迭代器没有更多的值|
|GeneratorExit|生成器(generator)发生异常来通知退出|
|StandardError|所有的内建标准异常的基类|
|ArithmeticError|所有数值计算错误的基类|
|FloatingPointError|浮点计算错误|
|OverflowError|数值运算超出最大限制|
|ZeroDivisionError|除(或取模)零 (所有数据类型)|
|AssertionError|断言语句失败|
|AttributeError|对象没有这个属性|
|EOFError|没有内建输入,到达|
|EOF|标记|
|EnvironmentError|操作系统错误的基类|  
|IOError|输入/输出操作失败|  
|OSError|操作系统错误|  
|WindowsError|系统调用失败|  
|ImportError|导入模块/对象失败|  
|LookupError|无效数据查询的基类|  
|IndexError|序列中没有此索引(index)|  
|KeyError|映射中没有这个键|  
|MemoryError|内存溢出错误(对于|Python解释器不是致命的)|  
|NameError|未声明/初始化对象 (没有属性)|  
|UnboundLocalError|访问未初始化的本地变量| 
|ReferenceError|弱引用(|Weak reference)试图访问已经垃圾回收了的对象| 
|RuntimeError|一般的运行时错误| 
|NotImplementedError|尚未实现的方法|  
|SyntaxErrorPython|语法错误| 
|IndentationError|缩进错误|  
|TabErrorTab|和空格混用|
|SystemError|一般的解释器系统错误| 
|TypeError|对类型无效的操作|  
|ValueError|传入无效的参数|  
|UnicodeErrorUnicode|相关的错误|  
|UnicodeDecodeErrorUnicode|解码时的错误| 
|UnicodeEncodeErrorUnicode|编码时错误| 
|UnicodeTranslateErrorUnicode|转换时错误| 
|Warning|警告的基类| 
|DeprecationWarning|关于被弃用的特征的警告|  
|FutureWarning|关于构造将来语义会有>改变的警告|  
|OverflowWarning|旧的关于自动提升为长整型(long)的警告|  
|PendingDeprecationWarning|关于特性将会被废弃的警告|  
|RuntimeWarning|可疑的运行时行为(runtime behavior)的警告|  
|SyntaxWarning|可疑的语法的警告|  
|UserWarning|用户代码生成的警告| 



## Python内置函数

菜鸟驿站参考链接： http://www.runoob.com/python/python-built-in-functions.html

### 重要内置函数

**open()或file()**
打开文件，创建file对象。 注意点： file对象的方法 + 打开模式

**staticmethod** 
返回函数的静态方法
```python
In [16]: class C():
    ...:     @staticmethod
    ...:     def a():
    ...:         pass
    ...:     def b():
    ...:         pass
In [18]: C.a()
In [20]: # 以上实例声明了静态方法 f，类可以不用实例化就可以调用该方法 C.f()，当然也可以实例化后调用 C().f()。vvvvv
```
**classmethod** 
修饰符对应的函数不需要实例化，不需要 self 参数，但第一个参数需要是表示自身类的 cls 参数，可以来调用类的属性，类的方法，实例化对象等
```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
class A(object):
    bar = 1
    def func1(self):  
        print ('foo') 
    @classmethod
    def func2(cls):
        print ('func2')
        print (cls.bar)
        cls().func1()   # 调用 foo 方法
 
A.func2()               # 不需要实例化
```

**getattr()** 
用于返回一个对象属性值。
```python
>>>class A(object):
...     bar = 1
... 
>>> a = A()
>>> getattr(a, 'bar')        # 获取属性 bar 值
1
```



**eval()** 
函数用来执行一个字符串表达式，并返回表达式的值

**isinstance()** 
函数来判断一个对象是否是一个已知的类型，类似 type()
```python
In [42]: a=2;print isinstance (a,int); print isinstance (a,(str,int,list))    # 是元组中的一个返回 True
True
True
In [43]: # 推荐使用 isinstance ，isinstance和type()区别，type（）不会考虑继承问题
In [44]: # int，float，bool，complex，str(字符串)，list，dict(字典)，set，tuple

# basestring() 方法是 str 和 unicode 的超类（父类），也是抽象类basestring() 函数。
# basestring() 可以被用来判断一个对象是否为 str 或者 unicode 的实例
>>>isinstance("Hello world", str)
True
>>> isinstance("Hello world", basestring)
True
>>> isinstance(u"Hello world", basestring)
True
```

**issubclass()**
用于判断参数 class 是否是类型参数 classinfo 的子类。
```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
class A:
    pass
class B(A):
    pass
    
print(issubclass(B,A))    # 返回 True
```

**super() TODO**
super() 函数是用于调用父类(超类)的一个方法。

super 是用来解决多重继承问题的，直接用类名调用父类方法在使用单继承的时候没问题，但是如果使用多继承，会涉及到查找顺序（MRO）、重复调用（钻石继承）等种种问题。

MRO 就是类的方法解析顺序表, 其实也就是继承父类方法时的顺序表。






### 基础内置函数


**abs**
返回函数绝对值。

**divmod(a,b)**
取余。
```python
>>> divmod(7,2)
(3,1)
```
**input()** 
接收一个合法的python表达式

**raw_input()**
接收任何字符，输出为 字符串

**all()**
判断 列表或元组中是否都为 True
```python
In [22]: all(['a', 'b', 'c', 'd'])  # 列表list，元素都不为空或0
Out[22]: True
In [23]: all(['a', '', 0, 'c', 'd'])  # 列表list，存在为空或0的元素
Out[23]: False
# 注意点 空列表或空元组 返回True
In [24]: all([])
Out[24]: True
```

**enumerate()** 
函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，
同时列出数据和数据下标，一般用在 for 循环当中
```python
In [29]:  list(enumerate(seasons, start=1))       # 下标从 1 开始
Out[29]: [(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]
```

**int()** 
函数用于将一个字符串或数字转换为整型

**ord()** 
返回对应十进制

**str()**
函数将对象转化为适于人阅读的形式。

**any()**
判断 元组或列表 是否全部为False. 与all()相反

**pow()**
方法返回 xy（x的y次方） 的值。
```python
improt math
math.power(2,4): 16.0
```

**sum()** 
对系列进行求和计算。

**bin() **
返回一个整数 int 或者长整数 long int 的二进制表示。
```python
In [47]: bin(10)
Out[47]: '0b1010'
```

**iter()** 
生成迭代器

**property()** 
函数的作用是在新式类中返回属性值。

**filter()** 
函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表。

**range()** 
函数可创建一个整数列表，一般用在 for 循环中。
```python
函数语法
range(start, stop[, step])
参数说明：

start: 计数从 start 开始。默认是从 0 开始。例如range（5）等价于range（0， 5）;
stop: 计数到 stop 结束，但不包括 stop。例如：range（0， 5） 是[0, 1, 2, 3, 4]没有5
step：步长，默认为1。例如：range（0， 5） 等价于 range(0, 5, 1)
```

**bytearray()** 
方法返回一个新字节数组。这个数组里的元素是可变的，并且每个元素的值范围: 0 <= x < 256。

**float()** 
函数用于将整数和字符串转换成浮点数。

**list()** 
方法用于将元组转换为列表。

**unichr()** 
函数 和 chr()函数功能基本一样， 只不过是返回 unicode 的字符。

**callable()** 
函数用于检查一个对象是否是可调用的。如果返回True，object仍然可能调用失败；但如果返回False，调用对象ojbect绝对不会成功。

对于函数, 方法, lambda 函式, 类, 以及实现了 __call__ 方法的类实例, 它都返回 True。

**str.format()**
它增强了字符串格式化的功能。 TODO

**locals()**
函数会以字典类型返回当前位置的全部局部变量

**reduce()**
函数会对参数序列中元素进行累积。
函数将一个数据集合（链表，元组等）中的所有数据进行下列操作：用传给 reduce 中的函数 function（有两个参数）先对集合中的第 1、2 个元素进行操作，得到的结果再与第三个数据用 function 函数运算，最后得到一个结果。
reduce(function, iterable[, initializer])
参数
function -- 函数，有两个参数
iterable -- 可迭代对象
initializer -- 可选，初始参数

**chr()**
用一个范围在 range（256）内的（就是0～255）整数作参数，返回一个对应的字符。

**frozenset()**
返回一个冻结的集合，冻结后集合不能再添加或删除任何元素。

**long()**
函数将数字或字符串转换为一个长整型。

**reload()**
用于重新载入之前载入的模块。

**vars()**
函数返回对象object的属性和属性值的字典对象。

**map()**
会根据提供的函数对指定序列做映射。
第一个参数 function 以参数序列中的每一个元素调用 function 函数，返回包含每次 function 函数返回值的新列表。
```python
>>>def square(x) :            # 计算平方数
...     return x ** 2
... 
>>> map(square, [1,2,3,4,5])   # 计算列表各个元素的平方
[1, 4, 9, 16, 25]
```

**repr()**
函数将对象转化为供解释器读取的形式。

**xrange()**
函数用法与 range 完全相同，所不同的是生成的不是一个数组，而是一个生成器。

**cmp(x,y)**
函数用于比较2个对象，如果 x < y 返回 -1, 如果 x == y 返回 0, 如果 x > y 返回 1。

**globals()**
函数会以字典类型返回当前位置的全部全局变量。

**max()**
方法返回给定参数的最大值，参数可以为序列。

**reverse()**
函数用于反向列表中元素。

**zip()** 
函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
如果各个迭代器的元素个数不一致，则返回列表长度与最短的对象相同，利用 * 号操作符，可以将元组解压为列表。
```python
>>>a = [1,2,3]
>>> b = [4,5,6]
>>> c = [4,5,6,7,8]
>>> zipped = zip(a,b)     # 打包为元组的列表
[(1, 4), (2, 5), (3, 6)]
>>> zip(a,c)              # 元素个数与最短的列表一致
[(1, 4), (2, 5), (3, 6)]
>>> zip(*zipped)          # 与 zip 相反，*zipped 可理解为解压，返回二维矩阵式
[(1, 2, 3), (4, 5, 6)]
```

**compile()**
函数将一个字符串编译为字节代码。

**hasattr()** 
函数用于判断对象是否包含对应的属性。

**memoryview()** 
函数返回给定参数的内存查看对象(Momory view)。
所谓内存查看对象，是指对支持缓冲区协议的数据进行包装，在不需要复制对象基础上允许Python代码访问。

**round()** 
方法返回浮点数x的四舍五入值。

**__import__()** 
函数用于动态加载类和函数 。
如果一个模块经常变化就可以使用 __import__() 来动态载入。

**complex()**
函数用于创建一个值为 real + imag * j 的复数或者转化一个字符串或数为复数。如果第一个参数为字符串，则不需要指定第二个参数。。

**hash()**
用于获取取一个对象（字符串或者数值等）的哈希值。

**min()** 
方法返回给定参数的最小值，参数可以为序列。

**set()**
函数创建一个无序不重复元素集，可进行关系测试，删除重复数据，还可以计算交集、差集、并集等。

**delattr**
函数用于删除属性。 delattr（x，'foobar'）相等于del x.foobar。

**help()** 
函数用于查看函数或模块用途的详细说明。

**next()** 
返回迭代器的下一个项目.

**setattr()** 
函数对应函数 getattr()，用于设置属性值，该属性必须存在。

**dict()**
函数用于创建一个字典

**hex()** 
函数用于将10进制整数转换成16进制，以字符串形式表示

**slice()**
函数实现切片对象，主要用在切片操作函数里的参数传递。

**dir()**
函数不带参数时，返回当前范围内的变量、方法和定义的类型列表；带参数时，返回参数的属性、方法列表。如果参数包含方法__dir__()，该方法将被调用。如果参数不包含__dir__()，该方法将最大限度地收集参数信息。

**id()**
函数用于获取对象的内存地址。

**oct()**
函数将一个整数转换成8进制字符串。

**sorted(list) 有返回值** 
**list.sort() 无返回值，直接修改原list** 
函数对所有可迭代的对象进行排序操作

**exec()** 
执行储存在字符串或文件中的Python语句，相比于 eval，exec可以执行更复杂的 Python 代码


## Python模块

### 模块搜索顺序
搜索路径当你导入一个模块，Python 解析器对模块位置的搜索顺序是：

1. 当前目录
2. 如果不在当前目录，Python 则搜索在 shell 变量 PYTHONPATH 下的每个目录。
3. 如果都找不到，Python会察看默认路径。UNIX下，默认路径一般为/usr/local/lib/python/。
模块搜索路径存储在 system 模块的 sys.path 变量中。变量里包含当前目录，PYTHONPATH和由安装过程决定的默认目录。命名空间和作用域
变量是拥有匹配对象的名字（标识符）。命名空间是一个包含了变量名称们（键）和它们各自相应的对象们（值）的字典。
一个 Python 表达式可以访问局部命名空间和全局命名空间里的变量。如果一个局部变量和一个全局变量重名，则局部变量会覆盖全局变量。

**dir()** 
函数一个排好序的字符串列表，内容是一个模块里定义过的名字。
返回的列表容纳了在一个模块里定义的所有模块，变量和函数。

**globals() 和 locals() 函数**
根据调用地方的不同，globals() 和 locals() 函数可被用来返回全局和局部命名空间里的名字。
如果在函数内部调用 locals()，返回的是所有能在该函数里访问的命名。
如果在函数内部调用 globals()，返回的是所有在该函数里能访问的全局名字。
两个函数的返回类型都是字典。所以名字们能用 keys() 函数摘取。

**reload() 函数**
当一个模块被导入到一个脚本，模块顶层部分的代码只会被执行一次。
因此，如果你想重新执行模块里顶层部分的代码，可以用 reload() 函数。该函数会重新导入之前导入过的模块。

### sys模块
**系统相关的信息模块: import sys**

- sys.argv 是一个 list,包含所有的命令行参数.
- sys.stdout sys.stdin sys.stderr 分别表示标准输入输出,错误输出的文件对象.
- sys.stdin.readline() 从标准输入读一行 sys.stdout.write("a") 屏幕输出a
- sys.exit(exit_code) 退出程序
- sys.modules 是一个dictionary，表示系统中所有可用的module
- sys.platform 得到运行的操作系统环境
- sys.path 是一个list,指明所有查找module，package的路径.
### os模块
**操作系统相关的调用和操作: import os**

- os.environ 一个dictionary 包含环境变量的映射关系
- os.environ["HOME"] 可以得到环境变量HOME的值
- os.chdir(dir) 改变当前目录 os.chdir('d:\\outlook')
注意windows下用到转义
- os.getcwd() 得到当前目录
- os.getegid() 得到有效组id os.getgid() 得到组id
- os.getuid() 得到用户id os.geteuid() 得到有效用户id
- os.setegid os.setegid() os.seteuid() os.setuid()
- os.getgruops() 得到用户组名称列表
- os.getlogin() 得到用户登录名称
- os.getenv 得到环境变量
- os.putenv 设置环境变量
- os.umask 设置umask
- os.system(cmd) 利用系统调用，运行cmd命令
内置模块(不用import就可以直接使用)常用内置函数：
- help(obj) 在线帮助, obj可是任何类型
- callable(obj) 查看一个obj是不是可以像函数一样调用
- repr(obj) 得到obj的表示字符串，可以利用这个字符串eval重建该对象的一个拷贝
- eval_r(str) 表示合法的python表达式，返回这个表达式
- dir(obj) 查看obj的name space中可见的name
- hasattr(obj,name) 查看一个obj的name space中是否有name
- getattr(obj,name) 得到一个obj的name space中的一个name
- setattr(obj,name,value) 为一个obj的name
space中的一个name指向vale这个object
- delattr(obj,name) 从obj的name space中删除一个name
- vars(obj) 返回一个object的name space。用dictionary表示
- locals() 返回一个局部name space,用dictionary表示
- globals() 返回一个全局name space,用dictionary表示
- type(obj) 查看一个obj的类型
- isinstance(obj,cls) 查看obj是不是cls的instance
- issubclass(subcls,supcls) 查看subcls是不是supcls的子类


### OS模块-文件目录
os 模块提供了非常丰富的方法用来处理文件和目录。常用的方法如下表所示：

- **os.access(path, mode)**:检验权限模式2
- **os.chdir(path)**:改变当前工作目录3
- **os.chflags(path, flags)**:设置路径的标记为数字标记。4
- **os.chmod(path, mode)**:更改权限5
- **os.chown(path, uid, gid)**:更改文件所有者6
- **os.chroot(path)**:改变当前进程的根目录7
- **os.close(fd)**:关闭文件描述符 fd8
- **os.closerange(fd_low, fd_high)**:关闭所有文件描述符，从 fd_low (包含) 到 fd_high (不包含), 错误会忽略9
- **os.dup(fd)**:复制文件描述符 fd10
- **os.dup2(fd, fd2)**:将一个文件描述符 fd 复制到另一个 fd211
- **os.fchdir(fd)**:通过文件描述符改变当前工作目录12
- **os.fchmod(fd, mode)**:改变一个文件的访问权限，该文件由参数fd指定，参数mode是Unix下的文件访问权限。13
- **os.fchown(fd, uid, gid)**:修改一个文件的所有权，这个函数修改一个文件的用户ID和用户组ID，该文件由文件描述符fd指定。14
- **os.fdatasync(fd)**:强制将文件写入磁盘，该文件由文件描述符fd指定，但是不强制更新文件的状态信息。15
- **os.fdopen(fd[, mode[, bufsize]])**:通过文件描述符 fd 创建一个文件对象，并返回这个文件对象16
- **os.fpathconf(fd, name)**:返回一个打开的文件的系统配置信息。name为检索的系统配置的值，
它也许是一个定义系统值的字符串，这些名字在很多标准中指定（POSIX.1, Unix 95, Unix 98, 和其它）。17
- **os.fstat(fd)**:返回文件描述符fd的状态，像stat()。18
- **os.fstatvfs(fd)**:返回包含文件描述符fd的文件的文件系统的信息，像 statvfs()19
- **os.fsync(fd)**:强制将文件描述符为fd的文件写入硬盘。20
- **os.ftruncate(fd, length)**:裁剪文件描述符fd对应的文件, 所以它最大不能超过文件大小。21
- **os.getcwd()**:返回当前工作目录22
- **os.getcwdu()**:返回一个当前工作目录的Unicode对象23
- **os.isatty(fd)**:如果文件描述符fd是打开的，同时与tty(-like)设备相连，则返回true, 否则False。24
- **os.lchflags(path, flags)**:设置路径的标记为数字标记，类似 chflags()，但是没有软链接25
- **os.lchmod(path, mode)**:修改连接文件权限26
- **os.lchown(path, uid, gid)**:更改文件所有者，类似 chown，但是不追踪链接。27
- **os.link(src, dst)**:创建硬链接，名为参数 dst，指向参数 src28
- **os.listdir(path)**:返回path指定的文件夹包含的文件或文件夹的名字的列表。29
- **os.lseek(fd, pos, how)**:设置文件描述符 fd当前位置为pos, how方式修改: SEEK_SET 或者 0 设置从文件开始的计算的pos; 
SEEK_CUR或者 1 则从当前位置计算; os.SEEK_END或者2则从文件尾部开始. 在unix，Windows中有效30
- **os.lstat(path)**:像stat(),但是没有软链接31
- **os.major(device)**:从原始的设备号中提取设备major号码 (使用stat中的st_dev或者st_rdev field)。32
- **os.makedev(major, minor)**:以major和minor设备号组成一个原始设备号33
- **os.makedirs(path[, mode])**:递归文件夹创建函数。像mkdir(), 但创建的所有intermediate-level文件夹需要包含子文件夹。34
- **os.minor(device)**:从原始的设备号中提取设备minor号码 (使用stat中的st_dev或者st_rdev field )。35
- **os.mkdir(path[, mode])**:以数字mode的mode创建一个名为path的文件夹.默认的 mode 是 0777 (八进制)。36
- **os.mkfifo(path[, mode])**:创建命名管道，mode 为数字，默认为 0666 (八进制)37
- **os.mknod(filename[, mode=0600, device])**:创建一个名为filename文件系统节点（文件，设备特别文件或者命名pipe）。38
- **os.open(file, flags[, mode])**:打开一个文件，并且设置需要的打开选项，mode参数是可选的39
- **os.openpty()**:打开一个新的伪终端对。返回 pty 和 tty的文件描述符。40
- **os.pathconf(path, name)**:返回相关文件的系统配置信息。41
- **os.pipe()**:创建一个管道. 返回一对文件描述符(r, w) 分别为读和写42
- **os.popen(command[, mode[, bufsize]])**:从一个 command 打开一个管道43
- **os.read(fd, n)**:从文件描述符 fd 中读取最多 n 个字节，返回包含读取字节的字符串，文件描述符 fd对应文件已达到结尾, 返回一个空字符串。44
- **os.readlink(path)**:返回软链接所指向的文件45
- **os.remove(path)**:删除路径为path的文件。如果path 是一个文件夹，将抛出OSError; 查看下面的rmdir()删除一个 directory。46
- **os.removedirs(path)**:递归删除目录。47
- **os.rename(src, dst)**:重命名文件或目录，从 src 到 dst48
- **os.renames(old, new)**:递归地对目录进行更名，也可以对文件进行更名。49
- **os.rmdir(path)**:删除path指定的空目录，如果目录非空，则抛出一个OSError异常。50
- **os.stat(path)**:获取path指定的路径的信息，功能等同于C API中的stat()系统调用。51
- **os.stat_float_times([newvalue])**:决定stat_result是否以float对象显示时间戳52
- **os.statvfs(path)**:获取指定路径的文件系统统计信息53
- **os.symlink(src, dst)**:创建一个软链接54
- **os.tcgetpgrp(fd)**:返回与终端fd（一个由os.open()返回的打开的文件描述符）关联的进程组55
- **os.tcsetpgrp(fd, pg)**:设置与终端fd（一个由os.open()返回的打开的文件描述符）关联的进程组为pg。56
- **os.tempnam([dir[, prefix]])**:返回唯一的路径名用于创建临时文件。57
- **os.tmpfile()**:返回一个打开的模式为(w+b)的文件对象 .这文件对象没有文件夹入口，没有文件描述符，将会自动删除。58
- **os.tmpnam()**:为创建一个临时文件返回一个唯一的路径59
- **os.ttyname(fd)**:返回一个字符串，它表示与文件描述符fd 关联的终端设备。如果fd 没有与终端设备关联，则引发一个异常。60
- **os.unlink(path)**:删除文件路径61
- **os.utime(path, times)**:返回指定的path文件的访问和修改的时间。62
- **os.walk(top[, topdown=True[, onerror=None[, followlinks=False]]])**:输出在文件夹中的文件名通过在树中游走，向上或者向下。63
- **os.write(fd, str)**:写入字符串到文件描述符 fd中. 返回实际写入的字符串长度


### 类型转换
**类型转换** 

- int(x) 将字符转为整型
- chr(i) 把一个ASCII数值,变成字符
- ord(i) 把一个字符或者unicode字符,变成ASCII数值
- oct(x) 把整数x变成八进制表示的字符串
- hex(x) 把整数x变成十六进制表示的字符串
- str(obj) 得到obj的字符串描述
- list(seq) 把一个sequence转换成一个list
- tuple(seq) 把一个sequence转换成一个tuple
- dict(),dict(list) 转换成一个dictionary
- int(x) 转换成一个integer
- long(x) 转换成一个long interger
- float(x) 转换成一个浮点数
- complex(x) 转换成复数
- max(...) 求最大值
- min(...) 求最小值
- repr(x)    将对象 x 转换为表达式字符串
- eval(str) 用来计算在字符串中的有效Python表达式,并返回一个对象
- tuple(s) 序列 s 转换为一个元组
- set(s) 转换为可变集合。
- frozenset(s) 转换为不可变集合
- unichr(x) 将一个整数转换为Unicode字符
- ord(x) 将一个字符转换为它的整数值
- hex(x) 将一个整数转换为一个十六进制字符串


### Python转义符
在需要在字符中使用特殊字符时，python用反斜杠(\)转义字符。如下表：

- \(在行尾时)续行符
- \\反斜杠符号
- \'单引号
- \"双引号
- \a响铃
- \b退格(Backspace)
- \e转义
- \000空
- \n换行
- \v纵向制表符
- \t横向制表符
- \r回车
- \f换页
- \oyy八进制数，yy代表的字符，例如：
- \o12代表换行
- \xyy十六进制数，yy代表的字符，例如：
- \x0a代表换行
- \other其它的字符以普通格式输出

**Python字符串格式化符号**

- **%c** 格式化字符及其ASCII码  - **%s** 格式化字符串
- **%d** 格式化整数
- **%u** 格式化无符号整型
- **%o** 格式化无符号八进制数
- **%x** 格式化无符号十六进制数
- **%X** 格式化无符号十六进制数（大写）
- **%f** 格式化浮点数字，可指定小数点后的精度
- **%e** 用科学计数法格式化浮点数
- **%E** 作用同%e，用科学计数法格式化浮点数
- **%g** %f和%e的简写
- **%G** %f 和 %E 的简写
- **%p** 用十六进制数格式化变量的地址


**格式化操作符辅助指令:**

- \* 定义宽度或者小数点精度
- \- 用做左对齐
- \+ 在正数前面显示加号( + )- <sp> 在正数前面显示空格- # 在八进制数前面显示零('0')，在十六进制前面显示'0x'或者'0X'(取决于用的是'x'还是'X')
- 0 显示的数字前面填充'0'而不是默认的空格 
- % '%%'输出一个单一的'%'
- (var) 映射变量(字典参数)
- m.n.m 是显示的最小总宽度,n 是小数点后的位数(如果可用的话)

**字符串内建函数**

|方法|描述|
|:-|:-|
|**string.capitalize():** |把字符串的第一个字符大写|
|**string.center(width):** |返回一个原字符串居中,并使用空格填充至长度 width 的新字符串|
|**string.count(str, beg=0, end=len(string)):** |返回 str 在 string 里面出现的次数，如果 beg 或者 end 指定则返回指定范围内 str 出现的次数|
|**string.decode(encoding='UTF-8', errors='strict'):** |以 encoding 指定的编码格式解码 string， 如果出错默认报一个 ValueError 的 异 常 ， 除非 errors 指 定 的 是 'ignore' 或 者'replace'|
|**string.encode(encoding='UTF-8', errors='strict'):** |以 encoding 指定的编码格式编码 string，如果出错默认报一个ValueError 的异常，除非 errors 指定的是'ignore'或者'replace'|
|**string.endswith(obj, beg=0, end=len(string)):** |检查字符串是否以 obj 结束，如果beg 或者 end 指定则检查指定的范围内是否以 obj 结束，如果是，返回 True,否则返回 False.|
|**string.expandtabs(tabsize=8):** |把字符串 string 中的 tab 符号转为空格，tab 符号默认的空格数是 8。|
|**string.find(str, beg=0, end=len(string)):** |检测 str 是否包含在 string 中，如果 beg 和 end 指定范围，则检查是否包含在指定范围内，如果是返回开始的索引值，否则返回-1|
|**string.format():** |格式化字符串|
|**string.index(str, beg=0, end=len(string)):** |跟find()方法一样，只不过如果str不在 string中会报一个异常.|
|**string.isalnum():** |如果 string 至少有一个字符并且所有字符都是字母或数字则返回 True,否则返回 False |
|**string.isalpha():** |如果 string 至少有一个字符并且所有字符都是字母则返回 True,否则返回 False|
|**string.isdecimal():** |如果 string 只包含十进制数字则返回 True 否则返回 False.|
|**string.isdigit():** |如果 string 只包含数字则返回 True 否则返回 False.|
|**string.islower():** |如果 string 中包含至少一个区分大小写的字符，并且所有这些(区分大小写的)字符都是小写，则返回 True，否则返回 False|
|**string.isnumeric():** |如果 string 中只包含数字字符，则返回 True，否则返回 False|
|**string.isspace():** |如果 string 中只包含空格，则返回 True，否则返回 False.|
|**string.istitle():** |如果 string 是标题化的(见 title())则返回 True，否则返回 False|
|**string.isupper():** |如果 string 中包含至少一个区分大小写的字符，并且所有这些(区分大小写的)字符都是大写，则返回 True，否则返回 False|
|**string.join(seq):** |以 string 作为分隔符，将 seq 中所有的元素(的字符串表示)合并为一个新的字符串|
|**string.ljust(width):** |返回一个原字符串左对齐,并使用空格填充至长度 width 的新字符串|
|**string.lower():** |转换 string 中所有大写字符为小写.|
|**string.lstrip():** |截掉 string 左边的空格|
|**string.maketrans(intab, outtab]):** |maketrans() 方法用于创建字符映射的转换表，对于接受两个参数的最简单的调用方式，第一个参数是字符串，表示需要转换的字符，第二个参数也是字符串表示转换的目标。|
|**max(str):** |返回字符串 str 中最大的字母。|
|**min(str):** |返回字符串 str 中最小的字母。|
|**string.partition(str):** |有点像 find()和 split()的结合体,从 str 出现的第一个位置起,把 字 符 串 string 分 成 一 个 3 元 素 的 元 组 (string_pre_str,str,string_post_str),如果 string 中不包含str 则 string_pre_str == string.|
|**string.replace(str1, str2,  num=string.count(str1)):** |把 string 中的 str1 替换成 str2,如果 num 指定，则替换不超过 num 次.|
|**string.rfind(str, beg=0,end=len(string) ):** |类似于 find()函数，不过是从右边开始查找.|
|**string.rindex( str, beg=0,end=len(string)):** |类似于 index()，不过是从右边开始.|
|**string.rjust(width):** |返回一个原字符串右对齐,并使用空格填充至长度 width 的新字符串|
|**string.rpartition(str):** |类似于 partition()函数,不过是从右边开始查找.|
|**string.rstrip():** |删除 string 字符串末尾的空格.|
|**string.split(str="", num=string.count(str)):** |以 str 为分隔符切片 string，如果 num有指定值，则仅分隔 num 个子字符串|
|**string.splitlines([keepends]):** |按照行('\r', '\r\n', \n')分隔，返回一个包含各行作为元素的列表，如果参数 keepends 为 False，不包含换行符，如果为 True，则保留换行符。|
|**string.startswith(obj, beg=0,end=len(string)):** |检查字符串是否是以 obj 开头，是则返回 True，否则返回 False。如果beg 和 end 指定值，则在指定范围内检查.|
|**string.strip([obj]):** |在 string 上执行 lstrip()和 rstrip()|
|**string.swapcase():** |翻转 string 中的大小写|
|**string.title():** |返回"标题化"的 string,就是说所有单词都是以大写开始，其余字母均为小写(见 istitle())|
|**string.translate(str, del=""):** |根据 str 给出的表(包含 256 个字符)转换 string 的字符, 要过滤掉的字符放到 del 参数中|
|**string.upper():** |转换 string 中的小写字母为大写|
|**string.zfill(width):** |返回长度为 width 的字符串，原字符串 string 右对齐，前面填充0|
|**string.isdecimal():** |isdecimal()方法检查字符串是否只包含十进制字符。这种方法只存在于unicode对象。|



### 日期和时间

时间间隔是以秒为单位的浮点小数。
每个时间戳都以自从1970年1月1日午夜（历元）经过了多长时间来表示。
```python
# 获取当前时间戳
In [3]: print time.time()
1542250660.2
```
时间戳单位最适于做日期运算。但是1970年之前的日期就无法以此表示了。太遥远的日期也不行，UNIX和Windows只支持到2038年。

#### struct_time元组

**struct_time元组**
|属性|值|
|:-:|:-:|
|tm_year|2008|
|tm_mon|1-12|
|tm_mday|1-31|
|tm_hour|0-23|
|tm_min|0-59|
|tm_sec|0-61(60/61闰秒)|
|tm_wday|0-6周一到周日|
|tm_yday|0-366(儒略历)|
|tm_isdst|-1, 0, 1, -1是决定是否为夏令时的旗帜|

#### 获取当前时间

**获取当前时间 struct_time格式**
```python
In [7]: print time.localtime(time.time())
time.struct_time(tm_year=2018, tm_mon=11, tm_mday=15, tm_hour=17, tm_min=52, tm_sec=23, tm_wday=3, tm_yday=319, tm_isdst=0)
```

**获取当前时间 asctime格式**
```python
In [8]: print  time.asctime( time.localtime(time.time()) )
Thu Nov 15 17:53:21 2018
```

#### 格式化日期

使用 **time.strftime()** 方法来格式化日期
```python
time.strftime(format[, t])
```
实例演示
```python
# 格式化成2016-03-20 11:45:39形式
In [9]: print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
2018-11-15 17:55:43
# 格式化成Sat Mar 28 22:24:24 2016形式
In [10]: print time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()) 
Thu Nov 15 17:55:54 2018
# 将格式字符串转换为时间戳
In [11]: a = "Sat Mar 28 22:24:24 2016"
In [12]: print time.mktime(time.strptime(a,"%a %b %d %H:%M:%S %Y"))
1459175064.0
```

**python中时间日期格式化符号：**

- %y 两位数的年份表示（00-99）
- %Y 四位数的年份表示（000-9999）
- %m 月份（01-12）
- %d 月内中的一天（0-31）
- %H 24小时制小时数（0-23）
- %I 12小时制小时数（01-12）
- %M 分钟数（00=59）
- %S 秒（00-59）
- %a 本地简化星期名称
- %A 本地完整星期名称
- %b 本地简化的月份名称
- %B 本地完整的月份名称
- %c 本地相应的日期表示和时间表示
- %j 年内的一天（001-366）
- %p 本地A.M.或P.M.的等价符
- %U 一年中的星期数（00-53）星期天为星期的开始
- %w 星期（0-6），星期天为星期的开始
- %W 一年中的星期数（00-53）星期一为星期的开始
- %x 本地相应的日期表示
- %X 本地相应的时间表示
- %Z 当前时区的名称
- %% %号本身

#### 日历模块 Calendar
Calendar模块有很广泛的方法用来处理年历和月历，例如打印某月的月历：
```python
cal = calendar.month(2016, 1)
print "以下输出2016年1月份的日历:"
print cal;

January 2016
Mo Tu We Th Fr Sa Su
1 2 3
4 5 6 7 8 9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30 31
```

#### Time模块函数

Time 模块包含了以下内置函数，既有时间处理的，也有转换时间格式的：

|模块函数|描述|
|:-|:-|
|time.altzone|返回格林威治西部的夏令时地区的偏移秒数。如果该地区在格林威治东部会返回负值（如西欧，包括英国）。对夏令时启用地区才能使用。|
|time.asctime([tupletime])|接受时间元组并返回一个可读的形式为"Tue Dec 11 18:07:14 2008"（2008年12月11日 周二18时07分14秒）的24个字符的字符串。|
|time.clock( )|用以浮点数计算的秒数返回当前的CPU时间。用来衡量不同程序的耗时，比time.time()更有用。|
|time.ctime([secs])|作用相当于asctime(localtime(secs))，未给参数相当于asctime()|
|time.gmtime([secs])|接收时间戳（1970纪元后经过的浮点秒数）并返回格林威治天文时间下的时间元组t。注：t.tm_isdst始终为0|
|time.localtime([secs])|接收时间戳（1970纪元后经过的浮点秒数）并返回当地时间下的时间元组t（t.tm_isdst可取0或1，取决于当地当时是不是夏令时）。|
|time.mktime(tupletime)|接受时间元组并返回时间戳（1970纪元后经过的浮点秒数）。|
|time.sleep(secs)|推迟调用线程的运行，secs指秒数。
|time.strftime(fmt[,tupletime])|接收以时间元组，并返回以可读字符串表示的当地时间，格式由fmt决定。|
|time.strptime(str,fmt='%a %b %d %H:%M:%S %Y')|根据fmt的格式把一个时间字符串解析为时间元组。|
|time.time( )|返回当前时间的时间戳（1970纪元后经过的浮点秒数）。|
|time.tzset()|根据环境变量TZ重新初始化时间相关设置。|

Time模块包含了以下2个非常重要的属性：
**time.timezone**
属性time.timezone是当地时区（未启动夏令时）距离格林威治的偏移秒数（>0，美洲;<=0大部分欧洲，亚洲，非洲）

**time.tzname**
属性time.tzname包含一对根据情况的不同而不同的字符串，分别是带夏令时的本地时区名称，和不带的。

#### Calendar函数
星期一是默认的每周第一天，星期天是默认的最后一天。更改设置需调用calendar.setfirstweekday()函数。模块包含了以下内置函数：



**calendar.calendar(year,w=2,l=1,c=6)**
返回一个多行字符串格式的year年年历，3个月一行，间隔距离为c。 每日宽度间隔为w字符。每行长度为21* W+18+2* C。l是每星期行数。

**calendar.firstweekday( )**
返回当前每周起始日期的设置。默认情况下，首次载入caendar模块时返回0，即星期一。

**calendar.isleap(year)**
是闰年返回 True，否则为 False。

**calendar.leapdays(y1,y2)**
返回在Y1，Y2两年之间的闰年总数。

**calendar.month(year,month,w=2,l=1)**
返回一个多行字符串格式的year年month月日历，两行标题，一周一行。每日宽度间隔为w字符。每行的长度为7* w+6。l是每星期的行数。

**calendar.monthcalendar(year,month)**
返回一个整数的单层嵌套列表。每个子列表装载代表一个星期的整数。Year年month月外的日期都设为0;范围内的日子都由该月第几日表示，从1开始。

**calendar.monthrange(year,month)**
返回两个整数。第一个是该月的星期几的日期码，第二个是该月的日期码。日从0（星期一）到6（星期日）;月从1到12。

**calendar.prcal(year,w=2,l=1,c=6)**
相当于 print calendar.calendar(year,w,l,c).

**calendar.prmonth(year,month,w=2,l=1)**
相当于 print calendar.calendar（year，w，l，c）。

**calendar.setfirstweekday(weekday)**
设置每周的起始日期码。0（星期一）到6（星期日）。

**calendar.timegm(tupletime)**
和time.gmtime相反：接受一个时间元组形式，返回该时刻的时间戳（1970纪元后经过的浮点秒数）。

**calendar.weekday(year,month,day)**
返回给定日期的日期码。0（星期一）到6（星期日）。月份为 1（一月） 到 12（12月）

#### datetime函数

pass



































































## Some Tips

### 循环控制语句

**break语句**： 语句块中终止循环，并跳出。
**continue语句**： 语句块中终止循环，继续下次循环。
**pass语句**： 空语句，用于保持程序完整性。

使用内置 **enumerate** 函数进行遍历
```python
In [24]: sequence = [1,2,3]
In [26]: for index, item in enumerate(sequence):
    ...:         print(index, item) 
(0, 1)
(1, 2)
(2, 3)

In [27]: sequence = {'a':1,'b':2,'c':3}
In [28]: for index, item in enumerate(sequence):
    ...:         print(index, item)
(0, 'a')
(1, 'c')
(2, 'b')
```
### return func和return func()区别

- **return func :** 返回函数func
- **return func():** 返回函数func()的返回值。
```python
In [27]: def funx(x):
    ...:     def funy(y=1):
    ...:         return x*y
    ...:     return funy

In [28]: funx(12)(2)
Out[28]: 24
```


### 函数参数类型
**函数参数的类型：**    

- 必备参数:  必备参数须以正确的顺序传入函数。调用时的数量必须和声明时的一样。
- 关键字参数： 使用关键字参数允许函数调用时参数的顺序与声明时不一致，因为 Python 解释器能够用参数名匹配参数值。
- 默认参数： 调用函数时，缺省参数的值如果没有传入，则被认为是默认值。下
- 不定长参数："* **" 你可能需要一个函数能处理比当初声明时更多的参数。这些参数叫做不定长参数，和上述2种参数不同，声明时不会命名



### 列表与字典函数
**Python列表 内置方法**
|序号|方法|
| ---- | ---- |
|list.append(obj)       |在列表末尾添加新的对象| 
|list.count(obj)        |统计某个元素在列表中出现的次数| 
|list.extend(seq)       |在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）| 
|list.index(obj)        |从列表中找出某个值第一个匹配项的索引位置| 
|list.insert(index, obj)|将对象插入列表| 
|list.pop(obj=list[-1]) |移除列表中的一个元素（默认最后一个元素），并且返回该元素的值| 
|list.remove(obj)       |移除列表中某个值的第一个匹配项| 
|list.reverse()         |反向列表中元素| 
|list.sort([func])      |对原列表进行排序| 

**Python字典 内置方法**

|序号                               |函数及描述| 
| ---- | ---- |
|dict.clear()                       |删除字典内所有元素| 
|dict.copy()                        |返回一个字典的浅复制| 
|dict.fromkeys(seq[, val])          |创建一个新字典，以序列 seq 中元素做字典的键，val 为字典所有键对应的初始值| 
|dict.get(key, default=None)        |返回指定键的值，如果值不在字典中返回default值| 
|dict.has_key(key)                  |如果键在字典dict里返回true，否则返回false| 
|dict.items()                       |以列表返回可遍历的(键, 值) 元组数组| 
|dict.keys()                        |以列表返回一个字典所有的键| 
|dict.setdefault(key, default=None) |和get()类似, 但如果键不存在于字典中，将会添加键并将值设为default| 
|dict.update(dict2)                 |把字典dict2的键/值对更新到dict里| 
|dict.values()                      |以列表返回字典中的所有值| 
|pop(key[,default])                 |删除字典给定键 key 所对应的值，返回值为被删除的值。key值必须给出。 否则，返回default值。| 
|popitem()                          |随机返回并删除字典中的一对键和值。| 


### 读取键盘输入

- **raw_input**: 读取行，并返回字符串。
- **input**： 读取行，可以读取表达式，并将运算结果返回。
```python
In [33]: input('输入内容为:')
输入内容为:test
NameError: name 'test' is not defined
In [32]: raw_input('输入内容为:')
输入内容为:test
Out[32]: 'test'

In [35]: input('输入内容为:')
输入内容为:[i for i in range(1,3)]
Out[35]: [1, 2]
In [36]: raw_input('输入内容为:')
输入内容为:[i for i in range(1,3)]
Out[36]: '[i for i in range(1,3)]'
```


