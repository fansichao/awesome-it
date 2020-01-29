# Python-05 知识-02Python23 对比分析.md

tags: Python2 Python3 差异对比 基础知识 2020 年 01 月

## Python2.7.11&Python3.6.0 差异

**环境说明**:

- Python2.7.11 -> Python3.6
- Centos7.5

**文档说明**:

1. 本文主要用于
   1. 项目 Python2 迁移升级到 Python3
   2. 学习了解 Python3
2. 本文主要来源于
   1. 知乎-Python23 差异
   2. 菜鸟教程-Python23 差异
   3. 官网-Python23 差异

### 主要区别

**Python23 主要区别**:

1. 统一了字符编码支持。
2. 增加了新的语法。print/exec 等成为了函数,格式化字符串变量,类型标注,添加了 nonlocal、yield from、async/await、yield for 关键词和**annotations**、**context**、**traceback**、**qualname**等 dunder 方法。
3. 修改了一些语法。metaclass,raise、map、filter 以及 dict 的 items/keys/values 方法返回迭代对象而不是列表,描述符协议,保存类属性定义顺序,保存关键字参数顺序
4. 去掉了一些语法。cmp、<>(也就是!=)、xrange（其实就是 range）、不再有经典类
5. 增加一些新的模块。concurrent.futures、venv、unittest.mock、asyncio、selectors、typing 等
6. 修改了一些模块。主要是对模块添加函数/类/方法（如 functools.lru_cache、threading.Barrier）或者参数。
7. 模块改名。把一些相关的模块放进同一个包里面（如 httplib, BaseHTTPServer, CGIHTTPServer, SimpleHTTPServer, Cookie, cookielib 放进了 http 里面,urllib, urllib2, urlparse, robotparse 放进了 urllib 里面）,个例如 SocketServer 改成了 socketserver,Queue 改成 queue 等 8. 去掉了一些模块或者函数。gopherlib、md5、contextlib.nested、inspect.getmoduleinfo 等。
8. 优化。重新实现了 dict 可以减少 20%-25%的内存使用；提升 pickle 序列化和反序列化的效率；collections.OrderedDict 改用 C 实现；通过 os.scandir 对 glob 模块中的 glob()及 iglob()进行优化,使得它们现在大概快了 3-6 倍等.. 这些都是喜大普奔的好消息,同样开发者不需要感知,默默的就会让结果变得更好。
9. 其他。构建过程、C 的 API、安全性等方面的修改,通常对于开发者不需要关心。

### 核心语法差异

Python23 主要变化项

- 字符串: 解决了编码问题
- 编码： 由默认 asscii, 变为 utf-8

#### 返回可迭代对象,而不是列表

```python
如果在 xrange 章节看到的,现在在 Python 3 中一些方法和函数返回迭代对象 -- 代替 Python 2 中的列表

因为我们通常那些遍历只有一次,我认为这个改变对节约内存很有意义。尽管如此,它也是可能的,相对于生成器 --- 如需要遍历多次。它是不那么高效的。

而对于那些情况下,我们真正需要的是列表对象,我们可以通过 list() 函数简单的把迭代对象转换成一个列表。

# py2
print range(3)
print type(range(3))

[0, 1, 2]
<type 'list'>

# py3
print(range(3))
print(type(range(3)))
print(list(range(3)))

range(0, 3)
<class 'range'>
[0, 1, 2]


```

在 Python 3 中一些经常使用到的不再返回列表的函数和方法：

- zip()
- map()
- filter()
- dictionary's .keys() method
- dictionary's .values() method
- dictionary's .items() method

#### 字符串 & 编码

字符串是最大的变化之一,

在 Python2 中,字符串有两个类型,一个是 unicode,一个是 str,前者表示文本字符串,后者表示字节序列

在 Python3 中两者做了严格区分,分别用 str 表示字符串,byte 表示字节序列,任何需要写入文本或者网络传输的数据都只接收字节序列

- Python2 的默认编码是 asscii
- Python3 默认采用了 UTF-8 作为默认编码,因此你不再需要在文件顶部写 `# coding=utf-8`

```python
# py2
>>> sys.getdefaultencoding()
'ascii'

# py3
>>> sys.getdefaultencoding()
'utf-8'
```

#### 格式化字符串

```python

在Python中格式化语法的方式大家通常都会偏向于【Format】或者 【%S】这两种方法,操作如下：
print("My name is %s" % ('phithon', ))
print("My name is %(name)s" % {'name':'phithon'})
print("My name is {}".format("bob"))
print("My name is {name}".format(name="bob"))


而到了Python3.6版本,推出了新的格式化字符串的灵活方法【f-string】,
使用【f-string】编写的与上面功能相同的代码是这样的
name="bob"
print(f"My name is {name}")
我们对比这几种格式化字符串的方法,可以发现相比于常见的字符串格式符【%S】 或 【Format】 方法,
【f-string】 直接在占位符中插入变量显得更加方便,也更好理解,
```

#### 路径管理库 Pathlib（最低 Python 版本为 3.4）

#### 枚举（最低 Python 版本为 3.4）

```python

# py3
from enum import Enum, auto
class Monster(Enum):
       ZOMBIE = auto()
       WARRIOR = auto()
       BEAR = auto()
print(Monster.ZOMBIE)
for i in Monster:
  print(i)
#Monster.ZOMBIE
#Monster.ZOMBIE
#Monster.WARRIOR
#Monster.BEAR
```

#### 原生 LRU 缓存（最低 Python 版本为 3.2）

TODO LRU 缓存
缓存是大家在开发中都会用到的一个特性,如果我们准确的使用好它,它会节省我们很多时间和成本。相信很多人初学 Python 装饰器的时候都会去实现一个缓存的装饰器来节省斐波那契函数的计算时间。而 Python 3 之后将 LRU（最近最少使用算法）缓存作为一个名为「lru_cache」的装饰器,使得对缓存的使用非常简单。

```python
from functools import lru_cache
@lru_cache(maxsize=512)
def fib_memoization(number: int) -> int:
  if number == 0:
    return 0
  if number == 1:
    return 1
  return fib_memoization(number-1) + fib_memoization(number-2)
start = time.time()
fib_memoization(40)
print(f'Duration: {time.time() - start}s')
# Duration: 6.866455078125e-05s
```

#### 扩展的可迭代对象解包（最低 Python 版本为 3.0）

```python
Python解包相信在我们初学Python的时候都有所了解,如果我们很多地掌握这个特性,相信是一件非常酷的事情。那什么是扩展的解包呢？我们可以从pep3132中了解更多,举个例子：# Python 3.4 中 print 函数 不允许多个 * 操作
>>> print(*[1,2,3], *[3,4])
  File "<stdin>", line 1
    print(*[1,2,3], *[3,4])
                    ^
SyntaxError: invalid syntax
>>>
# 再来看看 python3.5以上版本
# 可以使用任意多个解包操作
>>> print(*[1], *[2], 3)
1 2 3
>>> *range(4), 4
(0, 1, 2, 3, 4)
>>> [*range(4), 4]
[0, 1, 2, 3, 4]
>>> {*range(4), 4}
{0, 1, 2, 3, 4}
>>> {'x': 1, **{'y': 2}}
{'x': 1, 'y': 2}我们可以看到,解包这个操作也算的上Python中极其潮流的玩法了,耍的一手好解包,真的会秀翻全场啊！
```

#### Data class 装饰器（最低 Python 版本为 3.7）

```python
Python 3.7 引入了【data class】,新特性大大简化了定义类对象的代码量,代码简洁明晰。通过使用@dataclass装饰器来修饰类的设计,可以用来减少对样板代码的使用,因为装饰器会自动生成诸如「__init__（）」和「__repr（）__」这样的特殊方法。在官方的文档中,它们被描述为「带有缺省值的可变命名元组」。from dataclasses import dataclass

@dataclass
class DataClassCard:
    rank: str
    suit: str


#生成实例
queen_of_hearts = DataClassCard('Q', 'Hearts')
print(queen_of_hearts.rank)
print(queen_of_hearts)
print(queen_of_hearts == DataClassCard('Q', 'Hearts'))
#Q
#DataClassCard(rank='Q', suit='Hearts')
#True
```

#### 类型提示 Type hinting

```python
3. 类型提示 Type hinting（最低 Python 版本为 3.5）编程语言有很多类型,静态编译型语言和动态解释型语言的对比是软件工程中一个热门的话题,几乎每个人对此有自己的看法。在静态语言中类型标注无疑是让人又爱又恨,爱的是编译速度加快,团队合作中准确了解函数方法的入参类型,恨的是Coding时极其繁琐的标注。不过,标注这种极其符合团队文化的操作还是在Python3中被引入,并且很快得到了人们的喜爱。
def print_yes_or_no(codition: str) -> bool:
  pass

```

### 细节语法差异

#### next() and .next()

```python
# py2
next() 和 .next() 都可以使用

# py3
只能使用 next()
```

#### nonlocal

Python3 中新增 非局部变量 nonlocal,用于设置嵌套函数

#### unicode,字符串 u''

```python
# py2
u"根据orm模型重建表"

# py3
"根据orm模型重建表"
字符串、注释、unicode(xxx) 都需要去掉 u"" ,因为Python3默认为unicode,无需u前缀标识
unicode                  Python3加u''不会报错,但是无实际含义
```

#### 字典的 items 加 list

```python
# py2
savepath_dict.items()
list(savepath_dict.items())

# py3
>>> a = {'a':123}
>>> a.items()
dict_items([('a', 123)])
>>> list(a.items())
[('a', 123)]

字典的items加list     Python3不加list也不会报错
```

#### print 语法

```python
# py2
print "请输入正确的时间格式: yyyy-mm-dd"

# py3
print("请输入正确的时间格式: yyyy-mm-dd")

# 小结
1. Python2中print作为语句,Python3中print作为函数使用(接收字符串作为参数)
```

#### 除法运算

除法运算 Python3 保留小数部分

```python
# py2
In [11]: 1/2
Out[11]: 0

# py3
In [12]: 1/2
Out[12]: 0.5

In [13]: 1//2
Out[13]: 0
```

#### xrange 在 Python3 中被去除

#### 八进制字面量表示

Python3 中八进制不允许简写

```python
# py2
>>> 0o1000
512
>>> 01000
512

# py3
>>> 0o1000
512
```

#### 模块名称修改

Python3 中模块包名称符合 pep8 规范

```python
# py2
_winreg
ConfigParser
copy_reg
Queue
SocketServer
repr

# py3
winreg
configparser
copyreg
queue
socketserver
reprlib
```

#### 数据类型

```python
1）Py3.X去除了long类型,现在只有一种整型——int,但它的行为就像2.X版本的long

2）新增了bytes类型,对应于2.X版本的八位串,定义一个bytes字面量的方法如下：

>>> b = b'china'
>>> type(b)
<type 'bytes'>
str 对象和 bytes 对象可以使用 .encode() (str -> bytes) 或 .decode() (bytes -> str)方法相互转化。

>>> s = b.decode()
>>> s
'china'
>>> b1 = s.encode()
>>> b1
b'china'
3）dict的.keys()、.items 和.values()方法返回迭代器,而之前的iterkeys()等函数都被废弃。同时去掉的还有 dict.has_key(),用 in替代它吧
```

#### 从键盘录入一个字符串

```python
# py2
raw_input("提示信息")

# py3
input("提示信息")
```

#### 不等运算符

Python 2.x 中不等于有两种写法 != 和 <>

Python 3.x 中去掉了<>, 只有!=一种写法,还好,我从来没有使用<>的习惯

#### 隐式命名空间包（最低 Python 版本为 3.3）

在 Python 2 中,上面每个文件夹都必须包含将文件夹转化为 Python 程序包的`__init__.py`文件。

在 Python 3 中,随着隐式命名空间包的引入,这些文件不再是必须的了。

但建议有`__init__.py`文件

#### True and False

```python
# py2 中 True 和 False 可以赋值
True = 1

# py3 中 True 和 False 变更为关键字, 不允许更改
```

#### basestring

```python
# py2
isinstance(fields, basestring)

# py3
isinstance(fields, str)
```

#### has_key

```python
# py2
if not rst.has_key("aggregations"):

# py3
if "aggregations" not in rst:

Python3中可以使用 key not in dic 来识别key是否在字典中,
Python3中没有 dic.has_key('xxxx')
```

#### sys reload 语法

```python
# py2
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# py3
import sys
```

#### to_md5(x)

```python
# py2
        addr_df["peer_node_id"] = addr_df["peer_node_label"]. \
            apply(lambda x: to_md5(x))

# py3
to_md5(x.encode('utf-8'))

否则报错
TypeError: Unicode-objects must be encoded before hashing
```

#### min/max 函数

```python

Min/max函数在 Python 3 中,如果想对列表排序或找到最大/最小值,所有的元素必须可以比较。如果你原来的代码是 Python 2 写的,里面有包含 None 元素的列表,那么换到 Python 3 时就可能会出现一些问题。那么可以用 min/max 函数来解决这种冲突。def listmin(L):
 '''
 Returns min of an iterable L,
 Ignoring null (None) values.
 If all values are null, returns None
 '''
 values = [v for v in L if v is not None]
return min(values) if values else None也可以写一个相似的函数来确定最大元素。

```

#### cmp

```python
# py2
cmp(1,2)

# py3
python3移除了cmp()函数,但提供了六个丰富的比较运算符,详见此处
import operator       #首先要导入运算符模块
operator.gt(1,2)      #意思是greater than（大于）
operator.ge(1,2)      #意思是greater and equal（大于等于）
operator.eq(1,2)      #意思是equal（等于）
operator.le(1,2)      #意思是less and equal（小于等于）
operator.lt(1,2)      #意思是less than（小于）
```

#### except 语法

```python
# py2
except Exception, err:
    print(err.message)

# py3
except Exception as err:
    print(str(err))

```

#### 虚拟变量,For 循环变量和全局命名空间泄漏

```python
在使用由不同版本 Python 编写的代码时,还有一个很有意思的地方。
from __future__ import print_function
a = [i for i in range(10)]
print(i)如果我们在 Python 2 解释器上运行这段代码,我们会得到结果 9,

因为用于列表推导式的 i 变量留在了内存中。如果你在下部分代码中忘了这回事,再使用 i 变量的话,会导致不可见的错误。

在 Python 3 中一切更为简单,在这个例子中的变量只在列表的创建期间使用,之后不再保存。这样当我们运行代码时,就会看到如下结果：
NameError: name 'i' is not defined
```

#### func.func_name

```python
# py2
func.func_name

# py3
func.__name__
```

### 软件差异

```python
# Pandas
ModuleNotFoundError: No module named '_bz2'  Pandas==0.25.3 报此错误
更改安装 pandas==0.24.2

# uniout
import uniout
python3 中没有 uniout


# gunicorn
python2
gunicorn -c fdm/base/gun.conf fdm.views:app
python3
配置文件必须有 .py 扩展名
gunicorn -c fdm/base/gun.conf.py fdm.views:app 否则报错
!!!
!!! WARNING: configuration file should have a valid Python extension.
!!!

python2
workers = multiprocessing.cpu_count() / 4 + 1
python3  workers 只接受 int 参数
workers = int(multiprocessing.cpu_count() / 4 + 1)
```

#### `from module import *` 只能用于模块，不能用于函数

#### `from .[module] import name`

`from .[module] import name` 是相对导入的唯一正确语法，所有不以.开头的导入都被当成绝对导入

## Python2.7 升级到 Python3.6

Python3 自带 2to3 工具: `2to3 -w` 文件/文件夹路径

**项目代码修改:**

1. 2to3
   1. 去除 unicode
   2. print
   3. except,err
   4. has_key
   5. list(child_menus.get(menu_id, {}).items()) 字典加 list
   6. raw_input
   7. <>
   8. basestring
2. hashlib.md5(dataset_name.encode('utf-8') 增加 encode
3. sys reload 手动去除
4. cmp

**待修改项:**

1. 除法运算。 所有 `/` 项都需要检查

- [Python2 升级](https://blog.csdn.net/weixin_30326741/article/details/98936810)

## 参考链接

- [知乎 Python 2 和 Python 3 有哪些主要区别？](https://www.zhihu.com/question/19698598)
- [菜鸟教程-Python2.x 和 Python3.x 的区别](https://www.runoob.com/python/python-2x-3x.html)
- [Python 官网-Python3 新增差异](https://docs.python.org/3/whatsnew/3.0.html#)
