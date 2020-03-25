# Python 基础-13 功能模块

## Python2 和 Python3 并存

### Python3 安装配置

参考链接:
https://www.cnblogs.com/gaoyuechen/p/8006365.html

安装完成后自带 pip 等

```python
# 下载包
wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
# 解压
tar xf Python-3.6.0.tgz
# 配置安装信息
 ./configure --prefix=/usr/local/python3/
# 编译
make && make install
# 配置环境变量
新建文件
vim /etc/profile.d/python3.sh
export PATH=$PATH:/usr/local/python3/bin/
执行一下下面命令
export PATH=$PATH:/usr/local/python3/bin/
# 验证
python3
Python 3.6.0 (default, Feb  1 2017, 14:56:52)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-11)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

### pip3 安装配置

### env3 安装配置

### 判断数据类型

第一种：types
import types
type(x) is types.IntType # 判断是否 int 类型
type(x) is types.StringType # 判断是否 string 类型

第二种： 超级恶心的模式，不推荐
type(x) == type(1) # 判断是否 int 类型
type(x) == type("1") # 判断是否 string 类型

第三种： isinstance
isinstance(对象,类型名或类型列表或元祖) --> True/False
例如：isinstance("lst",(int,str,list)) # True
判断类型 "lst" 在 类型列表中

## Python 代码建议

```bash
from .. import
优先使用import a  使用a.B
有节制使用from a import B
避免使用 from a import *
```

Python -m xxx.py -m 使得一个模块像脚本一样运行
**name**
**package**

Python 的* \_\_ **xx**的区别
①*函数名 意味着，此函数用于类内部，不属于 api ，等同于私有函数
②**函数名 ，用来避免子类覆盖其内容，意味着此函数不能被重写，继承等。仅仅用于类的内部使用，
③**xx**函数，用于 Python 调用
使用\_one_underline 来表示该方法或属性是私有的，不属于 API；
当创建一个用于 python 调用或一些特殊情况时，使用**two_underline**；
使用**just_to_underlines，来避免子类的重写！

使用 join 连接字符 ,join 连接字符更高高效比+ ，尤其是大规模的字符串连接
join 使用：
'xx'.join([str1,str2]) = str1xxstr2
'xx'.join([str1,str2,str3]) = str1xxstr2xxstr3

时间测试，代码的性能分析
import timeit

# 生成测试所需的字符数组

格式化字符串优先使用.format，而不是%s 等

.format 的使用方法 1.位置符号
" select _ from {0} where 1=1 {2} ".format(xx,yy) 2.使用名称
" select _ from {xx} where 1=1 {yy} ".format(xx=1,yy=1) 3.同过属性
xx = 1
yy = 2
" select \* from {xx} where 1=1 {yy} ".format 4.格式化元组的具体项
point = (1,3)
'x:{0[0]}; y:{0[1]}'.format(point)
.format 的优势
使用灵活，可以作为参数传递，简便直观，%s 处理需要注意被格式化字符的格式而。format 不需要

## 通过字符串调用对象属性

python 通过字符串调用对象属性或方法的实例讲解
有时候需要将属性或方法作为参数传入，这个时候可以通过以下几种方式用字符串调用对象属性或方法

```python
1.eval
In [634]: def getmethod(x,char='just for test'):
  ...:  return eval('str.%s' % x)(char)
  ...:
In [635]: getmethod('upper')
Out[635]: 'JUST FOR TEST'
2、getattr
In [650]: def getmethod2(x, char='just for test'):
  ...:  return getattr(char, x)()
  ...:
In [651]: getmethod2('upper')
Out[651]: 'JUST FOR TEST'
```

## 获取目录下所有文件名称

```python
file_dir = "sss"
for root, dirs, files in os.walk(file_dir):
  print(root) #当前目录路径
  print(dirs) #当前路径下所有子目录
  print(files) #当前路径下所有非目录子文件
  for filename in files:
    file_path = os.path.join(file_dir,filename)
    print file_path
```

## uuid [唯一标识符]

UUID： 通用唯一标识符 ( Universally Unique Identifier )，对于所有的 UUID 它可以保证在空间和时间上的唯一性.

它是通过 MAC 地址、 时间戳、 命名空间、 随机数、 伪随机数来保证生成 ID 的唯一性,，有着固定的大小( 128 bit 位 )，通常由 32 字节的字符串（十六进制）表示。

它的唯一性和一致性特点，使得可以无需注册过程就能够产生一个新的 UUID；
UUID 可以被用作多种用途, 既可以用来短时间内标记一个对象，也可以可靠的辨别网络中的持久性对象。

```python
import uuid
# uuid.uuid1 基于时间戳
uuid.uuid1([node[, clock_seq]])
node - 默认主机的硬件地址
clock_seq 默认随机14位序列号
# uuid.uuid3  基于名字的MD5散列值
通过计算名字和命名空间的MD5散列值得到，保证了同一命名空间中不同名字的唯一性，
和不同命名空间的唯一性，但同一命名空间的同一名字生成相同的uuid。
uuid.uuid3(namespace, name)
# uuid.uuid4 基于随机数
由伪随机数得到，有一定重复概率，可以计算得到
# uuid.uuid5() 基于名称的SHA-1散列值
使用 Secure Hash Algorithm 1 算法
```

**总结：**

- 分布式环境: 建议 uuid1
- 名字唯一要求：建议 uuid3/uuid5

## 文字处理

### Levenshtein 文字距离

import Levenshtein
str1 = 'qwer1235'
str2 = 'qwe1235r'

计算汉明距离，要求 str1 和 str2 必须长度一致。是描述两个等长字串之间对应位置上不同字符的个数
Levenshtein.hamming(str1, str2) #

Levenshtein.distance(str1,str2)计算编辑距离。是描述一个字符串转化成另一个字串最少的操作次数，在其中的操作包括插入、删除、替换。
Levenshtein.distance(str1, str2)

### HTTP `url转义`

```python
         空格 用%20代替
         " 用%22代替
         # 用%23代替
        % 用%25代替
        &用%26代替
        ( 用%28代替
        ) 用%29代替
       + 用%2B代替
        , 用%2C代替
        / 用%2F代替
        : 用%3A代替
        ; 用%3B代替
       < 用%3C代替
       = 用%3D代替
       > 用%3E代替
       ? 用%3F代替
       @ 用%40代替
        \ 用%5C代替
        | 用%7C代替


%E6%B2%B3%E6%BA%90

python中关于url中特殊字符的编码和解码
原创瞌睡的猫猫 最后发布于2018-06-07 18:44:25 阅读数 5627  收藏
展开
编码

from urllib.parse import quote
text = quote(text, 'utf-8')
1
2
解码

from urllib.parse import unquote
text = unquote(text, 'utf-8')
1
2
假如url = “https://www.baidu.com"一个Ajax请求，url的字符”:”,”/”等需要转码才能传递
那么就需要编码，代码如下

from urllib.parse import quote
url = "https://www.baidu.com/"
url_encode = quote(url, 'utf-8')
print(url_encode)
1
2
3
4
反之，则为解码
我们在解析网页中可能需要把一些特定的url解码出来以便直观显示等
代码如下：

from urllib.parse import unquote
href= "https%3A%2F%2Fwww.baidu.com%2F"
url_encode = unquote(href, 'utf-8')
print(url_encode)
1
2
3
4
输出结果

https://www.baidu.com/
————————————————
版权声明：本文为CSDN博主「瞌睡的猫猫」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/sinat_35886587/article/details/80613618




Python2中,对url解码  可以这样做：
>>> print urllib.unquote("%E6%B5%8B%E8%AF%95abc")

 

 

python3取消unquote属性

可以这样做：

import urllib.parse

print(urllib.parse.unquote("%E6%B5%8B%E8%AF%95abc"))
 

 
```
