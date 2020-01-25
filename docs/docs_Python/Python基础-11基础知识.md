# Python 基础知识

tags: Python 基础 2019 年 10 月

**内容说明:**

- 变量
- 列表/元组
- 字典
- 数据转换

## 字符串

```python
a = 'string'
a = "string"
a = str()
a = """ string """
a = 'this is %s'%('string')
```

## 布尔类型

```python
True or False
```

## 整数

## 变量

### python 中检测某个变量是否有定义

参考链接：[http://www.cnblogs.com/starspace/archive/2008/12/03/1347007.html](http://www.cnblogs.com/starspace/archive/2008/12/03/1347007.html)

```python
第一种方法：
'var' in locals().keys()
第二种方法：
try:
    print var
except NameError:
    print 'var not defined'
第三种方法：
'var' in dir()
```

## 列表/元组 list/tuple

列表内置函数

1. list.append(obj) 在列表末尾添加新的对象
2. list.count(obj) 统计某个元素在列表中出现的次数
3. list.extend(seq) 在列表末尾一次性追加另一个序列中的多个值(用新列表扩展原来的列表)
4. list.index(obj) 从列表中找出某个值第一个匹配项的索引位置，索引从 0 开始
5. list.insert(index, obj) 将对象插入列表
6. list.pop(obj=list[-1]) 移除列表中的一个元素(默认最后一个元素)，并且返回该元素的值
7. list.remove(obj) 移除列表中某个值的第一个匹配项
8. list.reverse() 反向列表中元素，倒转
9. list.sort([func]) 对原列表进行排序

**列表特性:**

1. 列表使用方括号[]

**元组特性:**

1. 元组使用小括号()
2. 元组的元素不能修改
3. 元组中的元素值是不允许删除的，可以使用 del 语句来删除整个元组
4. 创建空元祖`tuple()`

### 判断 list 列表是否包含 Flase 布尔值 any/all

Python 内置函数 any(iterable)可以用来判断列表里是否存在元素可以使 bool(element)为 True

```python
>>> l= [None, 1, 0]
>>> any(l)
True
>>> all(l)
False
```

### 去除 list 重复值

myList = list(set(myList))

## 字典

字典(dictionary)是除列表之外 python 中最灵活的内置数据结构类型。列表是有序的对象结合，字典是无序的对象集合。两者之间的区别在于：字典当中的元素是通过键来存取的，而不是通过偏移存取。
字典由键和对应的值组成。字典也被称作关联数组或哈希表。

**字典的特性:**

1. 键必须不可变，键不能使用列表充当
2. 键出现两次，仅保留后面的键值。
3. 当访问不存在的键时报错 KeyError: 'Alice'[/code]

### 字典基础语法

**字典自带函数:**
Python 字典包含了以下内置函数：
1、cmp(dict1, dict2)：比较两个字典元素。
2、len(dict)：计算字典元素个数，即键的总数。
3、str(dict)：输出字典可打印的字符串表示。
4、type(variable)：返回输入的变量类型，如果变量是字典就返回字典类型。

Python 字典包含了以下内置方法：

1. radiansdict.clear()：删除字典内所有元素
2. radiansdict.copy()：返回一个字典的浅复制
3. radiansdict.fromkeys()：创建一个新字典，以序列 seq 中元素做字典的键，val 为字典所有键对应的初始值
4. radiansdict.get(key, default=None)：返回指定键的值，如果值不在字典中返回 default 值
5. radiansdict.has_key(key)：如果键在字典 dict 里返回 true，否则返回 false
6. radiansdict.items()：以列表返回可遍历的(键, 值) 元组数组
7. radiansdict.keys()：以列表返回一个字典所有的键
8. radiansdict.setdefault(key, default=None)：和 get()类似, 但如果键不已经存在于字典中，将会添加键并将值设为 default
9. radiansdict.update(dict2)：把字典 dict2 的键/值对更新到 dict 里
10. radiansdict.values()：以列表返回字典中的所有值
11. cmp(dict1, dict2) 比较两个字典元素
12. len(dict) 计算字典元素个数，即键的总数。
13. str(dict) 输出字典可打印的字符串表示。
14. type(variable) 返回输入的变量类型，如果变量是字典就返回字典类型。

### get

从字典中取值，当键不存在时不想处理异常

```python
dics.get('key', 'not found')
```

### setdefault

给字典添加一个条目。如果不存在，就指定特定的值；若存在，就算了。

```python
dic.setdefault(key, default)
```

### pop-删除字典值

从字典中取值，若找到则删除；当键不存在时不想处理异常

```python
dics.pop('key', '异常信息, not found')
```

### enumerate

用 enumerate 遍历下标

```python
In [17]: dic = {'a':'b'}
In [20]: for index,key in enumerate(dic):
    ...:     print index,key,dic[key]
0 a b
```

### sort 排序

利用 sort 函数对字典进行 key 排序和 value 排序

```python
字典实际上并不能排序，我们排的是items，即dict.items()，将字典转换成了一个列表
sorted函数的原型为：
sorted(iterable[, cmp[, key[, reverse]]])
iterable：是可迭代类型类型;
cmp：用于比较的函数，比较什么由key决定,有默认值，迭代集合中的一项;
key：用列表元素的某个属性和函数进行作为关键字，有默认值，迭代集合中的一项;
reverse：排序规则. reverse = True 或者 reverse = False，有默认值。
返回值：是一个经过排序的可迭代类型，与iterable一样。
一般来说，cmp和key可以使用lambda表达式。
常用的形式如下：
sorted(dict.items(), key=lambda e:e[1], reverse=True)
其中e表示dict.items()中的一个元素，e[1]则表示 按 值排序
如果把e[1]改成e[0]，那么则是按键排序，reverse=False可以省略
默认为升序排列
(1)字典按key排序
sorted(dict.items(), key=lambda e:e[0], reverse=True)#e[0]表示按key排序，e[1]表示按拍value排序。reverse=True表示倒序排列

sorted(dict.keys())#得到一个按大小排序的key列表
(2)字典按value排序
sorted(dict.items(), key=lambda e:e[1], reverse=True)#e[1]表示按value排序
```

### Python 由 Value 取 Key

说明：
_ 不同 key 同 value，转换中必然存在问题。
_ 不同方法不是完全可行的，仅仅做参考。

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

### Python 字典根据 Value 顺序排序

sort_sum = sorted(sum_dic.items(),key=lambda item:item[1],reverse=False)
[('北京', 714),
('上海', 660),]

### 有序字典

```python
from collections import OrderedDict
dic = OrderedDict({str(i):i for i in range(10)})
```

TODO 为什么字典按照插入顺序, 显示字典值?

### 对象随值变化

字典对象，随值变化

```python
In [55]: a;b
Out[55]: {1: 3}

In [56]: a={1:3};b=a

In [57]: print a;print b
{1: 3}
{1: 3}

In [58]: b.update({1:3222})

In [59]: print a;print b
{1: 3222}
{1: 3222}
```

嵌套对象，内部可变对象。随值变化

```python
In [60]: a=(1,2,[1,2]);b=a

In [61]: print a;print b
(1, 2, [1, 2])
(1, 2, [1, 2])

In [62]: b[2][1] = 23123

In [63]: print a;print b
(1, 2, [1, 23123])
(1, 2, [1, 23123])
```

## 日期和时间

```python
9.1、获取当前时间，例如：import time, datetime;

localtime = time.localtime(time.time())
#Local current time : time.struct_time(tm_year=2014, tm_mon=3, tm_mday=21, tm_hour=15, tm_min=13, tm_sec=56, tm_wday=4, tm_yday=80, tm_isdst=0)
print "Local current time :", localtime
说明：time.struct_time(tm_year=2014, tm_mon=3, tm_mday=21, tm_hour=15, tm_min=13, tm_sec=56, tm_wday=4, tm_yday=80, tm_isdst=0)属于struct_time元组，struct_time元组具有如下属性：


9.2、获取格式化的时间
可以根据需求选取各种格式，但是最简单的获取可读的时间模式的函数是asctime():
2.1、日期转换为字符串



首选：print time.strftime('%Y-%m-%d %H:%M:%S');
其次：print datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
最后：print str(datetime.datetime.now())[:19]
2.2、字符串转换为日期



expire_time = "2013-05-21 09:50:35"
d = datetime.datetime.strptime(expire_time,"%Y-%m-%d %H:%M:%S")
print d;
9.3、获取日期差




oneday = datetime.timedelta(days=1)
#今天，2014-03-21
today = datetime.date.today()
#昨天，2014-03-20
yesterday = datetime.date.today() - oneday
#明天，2014-03-22
tomorrow = datetime.date.today() + oneday
#获取今天零点的时间，2014-03-21 00:00:00
today_zero_time = datetime.datetime.strftime(today, '%Y-%m-%d %H:%M:%S')

#0:00:00.001000
print datetime.timedelta(milliseconds=1), #1毫秒
#0:00:01
print datetime.timedelta(seconds=1), #1秒
#0:01:00
print datetime.timedelta(minutes=1), #1分钟
#1:00:00
print datetime.timedelta(hours=1), #1小时
#1 day, 0:00:00
print datetime.timedelta(days=1), #1天
#7 days, 0:00:00
print datetime.timedelta(weeks=1)

9.4、获取时间差




#1 day, 0:00:00
oneday = datetime.timedelta(days=1)
#今天，2014-03-21 16:07:23.943000
today_time = datetime.datetime.now()
#昨天，2014-03-20 16:07:23.943000
yesterday_time = datetime.datetime.now() - oneday
#明天，2014-03-22 16:07:23.943000
tomorrow_time = datetime.datetime.now() + oneday
注意时间是浮点数，带毫秒。

那么要获取当前时间，需要格式化一下：
print datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')
print datetime.datetime.strftime(yesterday_time, '%Y-%m-%d %H:%M:%S')
print datetime.datetime.strftime(tomorrow_time, '%Y-%m-%d %H:%M:%S')

9.5、获取上个月最后一天



last_month_last_day = datetime.date(datetime.date.today().year,datetime.date.today().month,1)-datetime.timedelta(1)
9.6、字符串日期格式化为秒数，返回浮点类型：



expire_time = "2013-05-21 09:50:35"
d = datetime.datetime.strptime(expire_time,"%Y-%m-%d %H:%M:%S")
time_sec_float = time.mktime(d.timetuple())
print time_sec_float
9.7、日期格式化为秒数，返回浮点类型：



d = datetime.date.today()
time_sec_float = time.mktime(d.timetuple())
print time_sec_float
9.8、秒数转字符串



time_sec = time.time()
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_sec))
```

## 其他

### 内置函数

1. int(x [,base]) 将 x 转换为一个整数
2. float(x ) 将 x 转换到一个浮点数
3. complex(real [,imag]) 创建一个复数
4. str(x) 将对象 x 转换为字符串
5. repr(x) 将对象 x 转换为表达式字符串
6. eval(str) 用来计算在字符串中的有效 Python 表达式,并返回一个对象
7. tuple(s) 将序列 s 转换为一个元组
8. list(s) 将序列 s 转换为一个列表
9. chr(x) 将一个整数转换为一个字符
10. unichr(x) 将一个整数转换为 Unicode 字符
11. ord(x) 将一个字符转换为它的整数值
12. hex(x) 将一个整数转换为一个十六进制字符串
13. oct(x) 将一个整数转换为一个八进制字符串

### 数学函数

1. abs(x) 返回数字的绝对值，如 abs(-10) 返回 10
2. ceil(x) 返回数字的上入整数，如 math.ceil(4.1) 返回 5
3. cmp(x, y) 如果 x < y 返回 -1, 如果 x == y 返回 0, 如果 x > y 返回 1
4. exp(x) 返回 e 的 x 次幂(ex),如 math.exp(1) 返回 2.718281828459045
5. fabs(x) 返回数字的绝对值，如 math.fabs(-10) 返回 10.0
6. floor(x) 返回数字的下舍整数，如 math.floor(4.9)返回 4
7. log(x) 如 math.log(math.e)返回 1.0,math.log(100,10)返回 2.0
8. log10(x) 返回以 10 为基数的 x 的对数，如 math.log10(100)返回 2.0
9. max(x1, x2,...) 返回给定参数的最大值，参数可以为序列。
10. min(x1, x2,...) 返回给定参数的最小值，参数可以为序列。
11. modf(x) 返回 x 的整数部分与小数部分，两部分的数值符号与 x 相同，整数部分以浮点型表示。
12. pow(x, y) x\*\*y 运算后的值。
13. round(x [,n]) 返回浮点数 x 的四舍五入值，如给出 n 值，则代表舍入到小数点后的位数。
14. sqrt(x) 返回数字 x 的平方根，数字可以为负数，返回类型为实数，如 math.sqrt(4)返回 2+0j

### 类型转换

```python
 1 函数                      描述
 2 int(x [,base ])         将x转换为一个整数
 3 long(x [,base ])        将x转换为一个长整数
 4 float(x )               将x转换到一个浮点数
 5 complex(real [,imag ])  创建一个复数
 6 str(x )                 将对象 x 转换为字符串
 7 repr(x )                将对象 x 转换为表达式字符串
 8 eval(str )              用来计算在字符串中的有效Python表达式,并返回一个对象
 9 tuple(s )               将序列 s 转换为一个元组
10 list(s )                将序列 s 转换为一个列表
11 chr(x )                 将一个整数转换为一个字符
12 unichr(x )              将一个整数转换为Unicode字符
13 ord(x )                 将一个字符转换为它的整数值
14 hex(x )                 将一个整数转换为一个十六进制字符串
15 oct(x )                 将一个整数转换为一个八进制字符串
```

### 序列操作

```python
 1 操作                      描述
 2 s + r                   序列连接
 3 s * n , n * s           s的 n 次拷贝,n为整数
 4 s % d                   字符串格式化(仅字符串)
 5 s[i]                    索引
 6 s[i :j ]                切片
 7 x in s , x not in s     从属关系
 8 for x in s :            迭代
 9 len(s)                  长度
10 min(s)                  最小元素
11 max(s)                  最大元素
12 s[i ] = x               为s[i]重新赋值
13 s[i :j ] = r            将列表片段重新赋值
14 del s[i ]               删除列表中一个元素
15 del s[i :j ]            删除列表中一个片段
```

### 数值操作

```python
 1 x << y                  左移
 2 x >> y                  右移
 3 x & y                   按位与
 4 x | y                   按位或
 5 x ^ y                   按位异或 (exclusive or)
 6 ~x                      按位翻转
 7 x + y                   加
 8 x - y                   减
 9 x * y                   乘
10 x / y                   常规除
11 x // y                  地板除
12 x ** y                  乘方 (xy )
13 x % y                   取模 (x mod y )
14 -x                      改变操作数的符号位
15 +x                      什么也不做
16 ~x                      ~x=-(x+1)
17 abs(x )                 绝对值
18 divmod(x ,y )           返回 (int(x / y ), x % y )
19 pow(x ,y [,modulo ])    返回 (x ** y ) x % modulo
20 round(x ,[n])           四舍五入，n为小数点位数
21 x < y                   小于
22 x > y                   大于
23 x == y                  等于
24 x != y                  不等于(与<>相同)
25 x >= y                  大于等于
26 x <= y                  小于等于
```
