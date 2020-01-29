---
title: Python进阶知识03-生成器.md
tags: 2019年 08月 11号
notebook: 00技术笔记
---

# Python生成器

## 列表/字典推导式

列表推导式 样例

```Python
# >> 实现列表自加一

info = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# 方法1 enumerate循环
for index,i in enumerate(info):
    info[index] +=1
# 方法2 map方法
a = map(lambda x:x+1,info)
# 方法3 列表推导式
a = [i+1 for i in range(10)]

In [3]: print a
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

字典推导式 样例

```python
In [5]: {k:k+1 for k in info}
Out[5]: {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10}
```

## 生成器

- 生成器是一个特殊的程序，可以被用作控制循环的迭代行为.
- python中生成器是迭代器的一种，使用yield返回值函数，每次调用yield会暂停，
- 而可以使用next()函数和send()函数恢复生成器。
- 生成器可以节省大量内存。

### 生成器表达式

把一个列表生成式的[]中括号改为（）小括号，就创建一个generator

```python
#列表生成式
lis = [x*x for x in range(10)]
print(lis)
#生成器
generator_ex = (x*x for x in range(10))
print(generator_ex)

结果：
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
<generator object <genexpr> at 0x000002A4CBF9EBA0>
```

**生成器表达式使用**
使用```next()获取生成器的下一个返回值```
```python
generator_ex = (x*x for x in range(4))
print(next(generator_ex))
print(next(generator_ex))
print(next(generator_ex))
print(next(generator_ex))
结果：
0
1
4
9
# 超出值时会抛出异常
Traceback (most recent call last):
  File "列表生成式.py", line 42, in <module>
    print(next(generator_ex))
StopIteration
```

创建生成器后,一般使用```for循环```实现。

### 生成器函数

使用```yield 构造生成器函数```
yield是一个类似return 的关键字，迭代一次遇到yield的时候就返回yield后面或者右面的值。
而且下一次迭代的时候，从上一次迭代遇到的yield后面的代码开始执行

**任何使用了yield的函数就是生成器，生成器就是一个返回迭代器的函数，或者说生成器就是一个迭代器。**

```python
def fib(max):
    n,a,b =0,0,1
    while n < max:
        yield b
        a,b =b,a+b
        n = n+1

a = fib(10)
print next(a)
for i in a:
    print i
```

### 小结

生成器的用法

- **next()** 返回生成器下个值
- **close()** 关闭生成器。生成器被关闭后，再次调用next()方法，不管能否遇到yield关键字，都会立即抛出StopIteration异常。
- **send()** 可以通过send()方法，向生成器内部传递参数.继续运行yield之后的代码。
- **throw()** 除了向生成器函数内部传递参数，还可以传递异常。

生成器用法样例

```python
#! -*- coding:utf-8 -*-
def iterator_func(val):
   for i in range(val):
       print("生成器值:%s"%i)
       tmp = yield i
       if tmp:
           print("send传递值:%s"%tmp)
num = 5
gen = iterator_func(num)
# 必须先next()调用,开始生成器
gen.next()
for i in range(10):
    print(">>>>>>>> ")
    gen.send(i + 10)
    if i >= num:
        # throw 方法自定义异常
        gen.throw(Exception,u"自定义异常:数值不够")
    if i >= 1:
        # close()后. 到下一个next或send直接抛出异常
        gen.close()

生成器值:0
>>>>>>>> 
send传递值:10
生成器值:1
>>>>>>>> 
send传递值:11
生成器值:2
>>>>>>>> 
Traceback (most recent call last):
  File "a", line 14, in <module>
    gen.send(i+10)
StopIteration
```

生成器的分类

- **生成器函数**: 也是用def定义的，利用关键字yield一次性返回一个结果，阻塞，重新开始
- **生成器表达式**: 返回一个对象，这个对象只有在需要的时候才产生结果

生成器的优点

- 节省内存。大量数据时尤为明显。
- 节省代码，减少代码量同时提高代码可读性。
- 模拟并发。

> 模拟并发。Python虽然支持多线程，但是由于GIL（全局解释锁，Global Interpreter Lock）的存在，同一个时间，只能有一个线程在运行，所以无法实现真正的并发。这时就出现了协程。复杂解释不说了，简单说协程就是你可以暂停执行的函数"。也就是yield。

> Python实现协程最简单的方法，就是使用yield。当一个函数在执行过程中被阻塞时，就用yield挂起，然后执行另一个函数。当阻塞结束后，可以用next()或者send()唤醒。相比多线程，协程的好处是它在一个线程内执行，避免线程之间切换带来的额外开销，而且协程不存在加锁的步骤。

## 迭代器

迭代器包含有next方法的实现，在正确的范围内返回期待的数据以及超出范围后能够抛出StopIteration的错误停止迭代。


### Iterable可迭代对象

使用isinstance()判断一个对象是否为可Iterable对象

```python
# Iterable 可迭代对象
In [1]: from collections import Iterable

In [2]: isinstance([], Iterable)
Out[2]: True

In [3]: isinstance((x for x in range(10)), Iterable)
Out[3]: True

In [4]: isinstance('test', Iterable)
Out[4]: True

In [5]: isinstance(123, Iterable)
Out[5]: False
```

### Iterator迭代器

一个实现了iter方法的对象是可迭代的，一个实现next方法并且是可迭代的对象是迭代器。

可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator。

所以一个实现了iter方法和next方法的对象就是迭代器。

```python
In [6]: from collections import Iterator

In [7]: isinstance((x for x in range(10)), Iterator)
Out[7]: True

In [8]: isinstance([], Iterator)
Out[8]: False
```

### 迭代器和可迭代对象之间的转换

**Iterable转为Iterator:** ```iter([1,2,3])```
**Iterator转为Iterable:** ```list((x+1 for x in range(10)))```

```python
In [11]: isinstance(iter([]), Iterator)
Out[11]: True

In [12]: isinstance(iter('abc'), Iterator)
Out[12]: True

In [13]: isinstance([], Iterator)
Out[13]: False

In [15]: isinstance(list((x for x in range(10))),Iterator)
Out[15]: False
```

## 总结

- 凡是可作用于for循环的对象都是Iterable类型；
- 凡是可作用于next()函数的对象都是Iterator类型，它们表示一个惰性计算的序列；
- 集合数据类型如list、dict、str等是Iterable但不是Iterator，不过可以通过iter()函数获得一个Iterator对象。

对yield的总结
　　（1）通常的for..in...循环中，in后面是一个数组，这个数组就是一个可迭代对象，类似的还有链表，字符串，文件。他可以是a = [1,2,3]，也可以是a = [x*x for x in range(3)]。

它的缺点也很明显，就是所有数据都在内存里面，如果有海量的数据，将会非常耗内存。

　　（2）生成器是可以迭代的，但是只可以读取它一次。因为用的时候才生成，比如a = (x*x for x in range(3))。!!!!注意这里是小括号而不是方括号。

　　（3）生成器（generator）能够迭代的关键是他有next()方法，工作原理就是通过重复调用next()方法，直到捕获一个异常。

　　（4）带有yield的函数不再是一个普通的函数，而是一个生成器generator，可用于迭代

　　（5）yield是一个类似return 的关键字，迭代一次遇到yield的时候就返回yield后面或者右面的值。而且下一次迭代的时候，从上一次迭代遇到的yield后面的代码开始执行

　　（6）yield就是return返回的一个值，并且记住这个返回的位置。下一次迭代就从这个位置开始。

　　（7）带有yield的函数不仅仅是只用于for循环，而且可用于某个函数的参数，只要这个函数的参数也允许迭代参数。

　　（8）send()和next()的区别就在于send可传递参数给yield表达式，这时候传递的参数就会作为yield表达式的值，而yield的参数是返回给调用者的值，也就是说send可以强行修改上一个yield表达式值。

　　（9）send()和next()都有返回值，他们的返回值是当前迭代遇到的yield的时候，yield后面表达式的值，其实就是当前迭代yield后面的参数。

　　（10）第一次调用时候必须先next（）或send（）,否则会报错，send后之所以为None是因为这时候没有上一个yield，所以也可以认为next（）等同于send(None)



## yield实现单线程并发

yield单线程并发样例

```python
#! -*- coding:utf-8 -*-
import time

def consumer(name):
    print('%s 准备学习了～' %(name))
    while True:
        lesson = yield
        print('开始[%s]了,[%s]老师来讲课了～' %(lesson,name))

def producer(name):
    c1 = consumer('A')
    c2 = consumer('B')
    c1.next() # 先调用c1使后面的send能够传值
    c2.next() # 先调用c2使后面的send能够传值
    print('同学们开始上课了～')
    for i in range(3):
        time.sleep(1)
        print('到了两个同学')
        c1.send(i)
        c2.send(i)

producer('westos')

# > 返回结果
A 准备学习了～
B 准备学习了～
同学们开始上课了～
到了两个同学
开始[0]了,[A]老师来讲课了～
开始[0]了,[B]老师来讲课了～
到了两个同学
开始[1]了,[A]老师来讲课了～
开始[1]了,[B]老师来讲课了～
到了两个同学
开始[2]了,[A]老师来讲课了～
开始[2]了,[B]老师来讲课了～

"""
利用了关键字yield一次性返回一个结果，阻塞，重新开始
send 唤醒
"""
```

## 第三方函数库-greenlet

```python
"""
使用greenlet完成多任务
为了更好的使用协程来完成多任务，python中的greeblet模块
对其进行的封装
"""
from greenlet import greenlet
import time

def test1():
    while True:
        print('---A----')
        gr2.switch()
        time.sleep(0.5)

def test2():
    while True:
        print('----B----')
        gr1.switch()
        time.sleep(0.5)

"""
greenlet这个类对yield进行的封装
"""
gr1= greenlet(test1)
gr2 = greenlet(test2)
# 相当于开关，开启后两个函数之间能够相互切换执行
gr1.switch()

```

## 参考资源

[生成器使用](https://www.cnblogs.com/wj-1314/p/8490822.html)
[python(生成式、生成器)](https://blog.csdn.net/qq_43194257/article/details/84833704)
