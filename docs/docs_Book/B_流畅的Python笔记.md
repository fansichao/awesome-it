---
title: 流畅的Python笔记
tags: MarkDown
notebook: 00.读书笔记
---

# 流畅的 Python

## 书籍说明

**适合有一定 Python 基础，官网推荐进阶书籍。**

## 序列

列表推导（list comprehension）简称为 listcomps，
生成式表达器（generator expression）则称为 genexps。

**列表表推导式**

```python
# 带条件的列表推导式
In [2]: symbols = '$¢£¥€¤'
In [3]: print [ord(s) for s in symbols if ord(s) > 127]
[194, 162, 194, 163, 194, 165, 226, 130, 172, 194, 164]
# 多个列表推导式
In [5]: colors = ['black', 'white']
In [6]: sizes = ['S', 'M', 'L']
In [7]: print [(color, size) for color in colors for size in sizes]
[('black', 'S'), ('black', 'M'), ('black', 'L'), ('white', 'S'), ('white', 'M'), ('white', 'L')]
```

**map/filter 组合**

```python
In [4]: print list(filter(lambda c: c > 127, map(ord, symbols)))
[194, 162, 194, 163, 194, 165, 226, 130, 172, 194, 164]
```

**生成器表达式**

a, b, \*rest = range(2)

> > > a, b, rest
> > > (0, 1, [])

### 具名元组

collections.namedtuple 是一个工厂函数，
它可以用来构建一个带字段名的元组和一个有名字的类

通过对象取元组值。

```python
from collections import namedtuple
# 创建City类 字段名称
City = namedtuple('City', 'name country population coordinates')
# 字段赋值
tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
# 取值
print tokyo.population
# 显示 类中所有字段
print City._fields
# 显示 字典信息
print City._asdict()
```

`s[a:b:c]` 对象切片: 在 a 和 b 之间，以间隔 c 取值。

### 双向队列 deque

支持对左侧或右侧处理

使用

- 可选参数 maxlen. 一旦设定无法修改。超出 maxlen 后，会删除另一侧元素
- rotate 参数： 反转元素，>0 时将右侧元素转移到左侧，<0 时左侧元素移到右侧
- appendleft 左侧添加元素
- extendleft 左侧添加列表

```python
In [15]: from collections import deque
In [16]: dq = deque(range(10), maxlen=10)
In [20]: dq
Out[20]: deque([7, 8, 9, 0, 1, 2, 3, 4, 5, 6])
In [21]: dq.rotate(-4)
In [22]: dq
Out[22]: deque([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
```

### 其他说明

- 常见序列分类
  - 可变序列
  - 不可变序列
- 其他分类：
  - 扁平序列：体积更小、速度更快而且用起来更简单，但是它只能保存一些原子性的数据
  - 容器序列：容器序列则比较灵活，但是当容器序列遇到可变对象时

列表推导和生成器表达式则提供了灵活构建和初始化序列的方式
