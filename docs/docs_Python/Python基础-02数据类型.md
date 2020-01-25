# Python 基础知识 02-数据类型

**变量** Python 中的变量是不需要声明数据类型的，每个变量在使用前都必须赋值，变量赋值以后该变量才会被创建，变量的"类型"是所指的内存中被赋值对象的类型

**Python 中数据类型：**

- 字符串 str
- 布尔类型 bool
- 整数 int
- 浮点数 float
- 数字 number
- 列表 list
- 元组 tuple
- 字典 dict
- 日期 date

## 数据类型说明

## 字符串 str

```python
# 单引号
a = 'string'
# 双引号
a = "string"
# 三引号
a = """
三引号支持换行
"""

# 字符串常用
name = "Bob"
print "name is %s"%Bob
print "name is {name}".format(**{'name':name})

```

## 布尔类型 bool

```python
bool_value = True
bool_value = False

In [1]: bool("sss")
Out[1]: True

In [2]: bool([])
Out[2]: False

In [3]: bool(True)
Out[3]: True
```

## 整数 int

```python
In [8]: a = 5;type(a)
Out[8]: int

```

## 浮点数 float

```python
In [9]: a = 0.5;type(a)
Out[9]: float
```

## 数字 number

包含整数、浮点数、复数等。

```python
# 数学函数包
import math

# 数字类型转换
int(x [,base]) 将x转换为一个整数
float(x ) 将x转换到一个浮点数
complex(real [,imag]) 创建一个复数
str(x) 将对象x转换为字符串
repr(x) 将对象x转换为表达式字符串
eval(str) 用来计算在字符串中的有效Python表达式,并返回一个对象
tuple(s) 将序列s转换为一个元组
list(s) 将序列s转换为一个列表
chr(x) 将一个整数转换为一个字符
unichr(x) 将一个整数转换为Unicode字符
ord(x) 将一个字符转换为它的整数值
hex(x) 将一个整数转换为一个十六进制字符串
oct(x) 将一个整数转换为一个八进制字符串

# 数学函数
abs(x)    返回数字的绝对值，如abs(-10) 返回 10
ceil(x)    返回数字的上入整数，如math.ceil(4.1) 返回 5
cmp(x, y) 如果 x < y 返回 -1, 如果 x == y 返回 0, 如果 x > y 返回 1
exp(x)    返回e的x次幂(ex),如math.exp(1) 返回2.718281828459045
fabs(x)    返回数字的绝对值，如math.fabs(-10) 返回10.0
floor(x) 返回数字的下舍整数，如math.floor(4.9)返回 4
log(x)    如math.log(math.e)返回1.0,math.log(100,10)返回2.0
log10(x) 返回以10为基数的x的对数，如math.log10(100)返回 2.0
max(x1, x2,...)    返回给定参数的最大值，参数可以为序列。
min(x1, x2,...)    返回给定参数的最小值，参数可以为序列。
modf(x)    返回x的整数部分与小数部分，两部分的数值符号与x相同，整数部分以浮点型表示。
pow(x, y) x**y 运算后的值。
round(x [,n]) 返回浮点数x的四舍五入值，如给出n值，则代表舍入到小数点后的位数。
sqrt(x)    返回数字x的平方根，数字可以为负数，返回类型为实数，如math.sqrt(4)返回 2+0j
```

## 列表 list

列表属于可变对象。

**列表使用**

```python
# 初始化列表
lis = list()
In [11]: lis = [1,2,3,4,5,"a","b","c"]
# 列表截取
In [12]: print lis[1:3]
[2, 3]
# 删除列表元素
In [13]: del lis[0] # 第 0 个位置
In [14]: lis
Out[14]: [2, 3, 4, 5, 'a', 'b', 'c']
# 列表新增
In [15]: lis.append("d")
In [16]: lis
Out[16]: [2, 3, 4, 5, 'a', 'b', 'c', 'd']
# 列表 + 列表
In [17]: lis + ["e","f"]
Out[17]: [2, 3, 4, 5, 'a', 'b', 'c', 'd', 'e', 'f']
lis.extend(["e","f"])


# 由于列表是可变对象，所有列表中元素变更，其内存地址不变。
In [19]: id(lis)
Out[19]: 140413028860776

In [20]: del lis[lis.index("a")]

In [21]: lis
Out[21]: [2, 3, 4, 5, 'b', 'c', 'd']

In [22]: id(lis)
Out[22]: 140413028860776
```

**列表函数**

```python
list.append(obj) 在列表末尾添加新的对象
list.count(obj) 统计某个元素在列表中出现的次数
list.extend(seq) 在列表末尾一次性追加另一个序列中的多个值(用新列表扩展原来的列表)
list.index(obj) 从列表中找出某个值第一个匹配项的索引位置，索引从0开始
list.insert(index, obj) 将对象插入列表
list.pop(obj=list[-1]) 移除列表中的一个元素(默认最后一个元素)，并且返回该元素的值
list.remove(obj) 移除列表中某个值的第一个匹配项
list.reverse() 反向列表中元素，倒转
list.sort([func]) 对原列表进行排序
```

## 元组 tuple

**元组特性:**

- 不可变列表
- 有序

元组时不可变的列表，类似列表，但是不可修改。

```python
a = tuple()
```

## 字典 dict

**字典特性:**

- 字典是 {Key:value} 格式
- 无序
- Key 唯一

字典(dictionary)是除列表之外 python 中最灵活的内置数据结构类型。
列表是有序的对象结合，字典是无序的对象集合。
两者之间的区别在于：字典当中的元素是通过键来存取的，而不是通过偏移存取。

字典由键和对应的值组成。字典也被称作关联数组或哈希表。

```python
# 初始化
dict = {'Alice': '2341', 'Beth': '9102', 'Cecil': '3258'};


# 字典内置函数
cmp(dict1, dict2) 比较两个字典元素。
len(dict) 计算字典元素个数，即键的总数。
str(dict) 输出字典可打印的字符串表示。
type(variable) 返回输入的变量类型，如果变量是字典就返回字典类型。
radiansdict.clear() 删除字典内所有元素
radiansdict.copy() 返回一个字典的浅复制
radiansdict.fromkeys() 创建一个新字典，以序列seq中元素做字典的键，val为字典所有键对应的初始值
radiansdict.get(key, default=None) 返回指定键的值，如果值不在字典中返回default值
radiansdict.has_key(key) 如果键在字典dict里返回true，否则返回false
radiansdict.items() 以列表返回可遍历的(键, 值) 元组数组
radiansdict.keys() 以列表返回一个字典所有的键
radiansdict.setdefault(key, default=None) 和get()类似, 但如果键不已经存在于字典中，将会添加键并将值设为default
radiansdict.update(dict2) 把字典dict2的键/值对更新到dict里
radiansdict.values() 以列表返回字典中的所有值
```

## 日期和时间 date

```python

# 日期时间常用模块
import time
import datetime
import calendar



```

# 参考资源

- [Python 数据类型详解: https://www.cnblogs.com/linjiqin/p/3608541.html](https://www.cnblogs.com/linjiqin/p/3608541.html)
