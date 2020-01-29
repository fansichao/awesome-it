# Python-00装饰器

装饰器

[toc]

**TODO**

## 总结

**装饰器的作用就是为已经存在的函数或对象添加额外的功能**

**装饰器使用种类：**
- 函数装饰器
- 类装饰器
- 函数装饰器装饰 类
- 类装饰器装饰 函数

**装饰器样例**
```python
@staticmethod
@logging
def a():
    return 1
    pass
等价于
a = staticmethod(logging(a)) 
```

**默认装饰器函数**

- **@property**
通过property装饰器控制类的属性的绑定与获取，一般就是给某个属性增加一个验证类型等功能。
- **@staticmethod**
将被装饰的函数从类中分离出来，该函数不能访问类的属性，简单说可以将该函数理解为一个独立的函数，不允许使用self。
staticmethod 就是将该被装饰的函数与该类没有关系，该函数不能用self传参，需要和普通函数一样传参。
- **@classmethod**
classmethod 可以用来为一个类创建一些预处理的实例.类方法只能找类变量，不能访问实例变量

**装饰器库 functools**
因为使用装饰器 functools 会导致函数或类信息缺失。
例如 func.\_\_name\_\_ 
所以需要使用 functools 装饰器库处理

使用方法:
每个装饰器前面加上下句话即可
**@functools.wraps(func)**
样例如下所示：
```python
def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print '%s %s():' % (text, func.__name__)
            return func(*args, **kw)
        return wrapper
    return decorator
```


## 装饰器&函数

### 函数简单说明

参考链接: [12步轻松搞定python装饰器](http://python.jobbole.com/81683/)

了解装饰器之前也需要了解**内部函数与函数闭包**。

参考链接: [内部函数&函数闭包](https://www.jb51.net/article/86383.htm)

**内部函数**

```python
def wai_hanshu(canshu_1):

  def nei_hanshu(canshu_2): # 我在函数内部有定义了一个函数
    return canshu_1*canshu_2

  return nei_hanshu  # 我将内部函数返回出去

a = wai_hanshu(123)   # 此时 canshu_1 = 123
print a
print a(321)  # canshu_2 = 321
```

**闭包说明**
参考链接： [函数闭包](https://www.cnblogs.com/JohnABC/p/4076855.html)
python中的闭包从表现形式上定义（解释）为：
如果在一个内部函数里，对在外部作用域（但不是在全局作用域）的变量进行引用，那么内部函数就被认为是闭包(closure)。

- 闭包=函数+引用环境
- 闭包中是不能修改外部作用域的局部变量的
- 当闭包执行完后，仍然能够保持住当前的运行环境
- 闭包可以根据外部作用域的局部变量来得到不同的结果

### 装饰器说明

装饰器本质上是一个Python函数，它可以**让其他函数在不需要做任何代码变动的前提下增加额外功能**。
装饰器的返回值也是一个函数对象。
它经常用于有切面需求的场景，比如：插入日志、性能测试、事务处理、缓存、权限校验等场景。
装饰器是解决这类问题的绝佳设计，有了装饰器，我们就可以抽离出大量与函数功能本身无关的雷同代码并继续重用。

**装饰器的作用就是为已经存在的函数或对象添加额外的功能**

装饰器/修饰符 - decorator



## 装饰器知识


### 函数装饰器

参考链接:
[https://www.cnblogs.com/cicaday/p/python-decorator.html](https://www.cnblogs.com/cicaday/p/python-decorator.html)

概括的讲，装饰器的作用就是为**已经存在的函数或对象添加额外的功能**

**简单装饰器样例**
```python
def debug(func):
    def wrapper(*args, **kwargs):  # 指定宇宙无敌参数
        print "[DEBUG]: enter {}()".format(func.__name__)
        print 'Prepare and say...',
        return func(*args, **kwargs)
    return wrapper  # 返回

@debug
def say(something):
    print "hello {}!".format(something)
   
等同于 
say = debug(say)
```

### 原理分析

```python
@decorator_a
def f():
    pass
等价于
f = decorator_a(f)
```

装饰器满足的条件
1. 装饰器函数运行在函数定义的时候 
2. 装饰器需要返回一个可执行的对象 
3. 装饰器返回的可执行对象要兼容函数f的参数

### 类装饰器
**类装饰器中必须使用 \_\_call__ 方法。将类实例转为可调用对象。**
```python
class Decorator(object):
    def __init__(self, f):
        self.f = f
    def __call__(self):
        print("decorator start")
        self.f()
        print("decorator end")

@Decorator
def func():
    print("func")

func()
```
这里有注意的是：__call__()是一个特殊方法，它可将一个类实例变成一个可调用对象:
```python
p = Decorator(func) # p是类Decorator的一个实例
p() # 实现了__call__()方法后，p可以被调用
```
要使用类装饰器必须实现类中的__call__()方法，就相当于将实例变成了一个方法。

### 装饰器链

所谓装饰器链，即多个装饰器的解析方式。

```python
@decorator_b
@decorator_a
def test():
    pass
等同于
test = decorator_b(decorator_a(test))
```

装饰器执行顺序 **是从近到远依次执行**。

### 内置装饰器

**内置装饰器**
- 特性（property）
- 静态方法（staticmethod）
- 类方法（classmethod） 



[内置装饰器参考链接](https://www.cnblogs.com/wangyongsong/p/6750454.html)

## 附录A-装饰器库参数表

[官方functools文档](https://docs.python.org/2/library/functools.html)
[functools参考博客](https://www.cnblogs.com/zhbzz2007/p/6001827.html)

functools，用于高阶函数：
指那些作用于函数或者返回其它函数的函数，通常只要是可以被当做函数调用的对象就是这个模块的目标。

**functools方法**
- cmp_to_key，将一个比较函数转换关键字函数；
- partial，针对函数起作用，并且是部分的；
- reduce，与python内置的reduce函数功能一样；
- total_ordering，在类装饰器中按照缺失顺序，填充方法；
- update_wrapper，更新一个包裹（wrapper）函数，使其看起来更像被包裹（wrapped）的函数；
- wraps，可用作一个装饰器，简化调用update_wrapper的过程；

**cmp_to_key**
将老式的比较函数（comparison function）转换为关键字函数（key function），与接受key function的工具一同使用（例如sorted，min，max，heapq.nlargest，itertools.groupby），该函数主要用于将程序转换成Python 3格式的，因为Python 3中不支持比较函数。比较函数是可调用的，接受两个参数，比较这两个参数并根据他们的大小关系返回负值、零或者正值中的一个。关键字函数也是可调用的，接受一个参数，同时返回一个可以用作排序关键字的值。
**partial**
functools.partial(func, \*args, \*\*keywords)，函数装饰器，返回一个新的partial对象。调用partial对象和调用被修饰的函数func相同，只不过调用partial对象时传入的参数个数通常要少于调用func时传入的参数个数。
**reduce**
与Python内置的reduce函数一样，为了向Python3过渡
**total_ordering**
这是一个类装饰器，给定一个类，这个类定义了一个或者多个比较排序方法，这个类装饰器将会补充其余的比较方法，减少了自己定义所有比较方法时的工作量.
被修饰的类必须至少定义 __lt__()， __le__()，__gt__()，__ge__()中的一个，同时，被修饰的类还应该提供 __eq__()方法。
**update_wrapper**
更新一个包裹（wrapper）函数，使其看起来更像被包裹（wrapped）的函数。
**wraps**
这个函数可用作一个装饰器，简化调用update_wrapper的过程，调用这个函数等价于调用partial(update_wrapper, wrapped = wrapped, assigned = assigned,updated = updated)。

## 附录B-测试代码样例

文件： /home/scfan/pro/server/pro/tools/base_decorator.py

```python
import time
import datetime
import functools

def decorator_func(text="all"):
    u""" 统计函数相关信息 All
    - 函数运行时间
    - 函数名称

    """
    def decorator(func,*args,**kwargs):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            start = datetime.datetime.now()
            data = func(*args, **kwargs)
            runtime = datetime.datetime.now() - start
            msg = "@函数运行信息: 函数类型[%s],函数名称[%s],运行时间[%s秒]"%(text,func.__name__,runtime.total_seconds())
            print(msg)
            return data
        return wrapper
    return decorator

class Decorator(object):
    u"""
        装饰器类
    """
    def __init__(self, func):
        self.func = func

    # __call__()是一个特殊方法，它可将一个类实例变成一个可调用对象
    def __call__(self, *args, **kwargs):
        print("decorator start")
        self.func()
        print("decorator end")
 
 if __name__ == '__main__':
    @Decorator
    @decorator_func("all")
    def a(b="cc"):
        for i in range(2):
            time.sleep(1)
        print "函数运行...."
        return b
    a()      
```
运行信息
```python
(env) [scfan@WOM tools]$ python base_decorator.py 
decorator start
函数运行....
@函数运行信息: 函数类型[all],函数名称[a],运行时间[2.004331秒]
decorator end
```

## 附录C-参考资源链接

- [廖雪峰-装饰器入门](https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386819879946007bbf6ad052463ab18034f0254bf355000)
- [装饰器参考A](https://www.cnblogs.com/lianyingteng/p/7743876.html)
- [装饰器参考B](http://baijiahao.baidu.com/s?id=1599946084778367809&wfr=spider&for=pc)


## 附录D-装饰器相关

- [智能装饰器](https://www.jb51.net/article/131397.htm)
- [python使用装饰器和线程限制函数执行时间的方法](https://www.jb51.net/article/64369.htm)








