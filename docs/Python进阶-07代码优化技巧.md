# 代码优化技巧

  

## 优化原则



## 核心技巧



## 其他技巧


[Python 代码性能优化技巧](https://www.ibm.com/developerworks/cn/linux/l-cn-python-optim/)

常用代码优化技巧

- sort()优于sorted.
- 字符串拼接。join优于字符串相加
- 列表表达式优于列表循环。
- 减少不必要的临时对象
-  应避免在高频函数中使用import语句的开销。去除无用import语句，延迟import
- 尽量减少函数调用次数，减少时间复杂度。
- 元组内存优于列表。



### 检查值是否存在，set快于列表循环。
```python
from timeit import timeit
def in_test(iterable):
    for i in range(1000):
        if i in iterable:
            pass
print 'set:', timeit("in_test(iterable)", setup="from __main__ import in_test; iterable = set(range(1000))", number=10000)
print 'list:', timeit("in_test(iterable)", setup="from __main__ import in_test; iterable = list(range(1000))", number=10000)
print 'tuple:', timeit("in_test(iterable)", setup="from __main__ import in_test; iterable = tuple(range(1000))", number=10000)

[out]:
set: 0.558294298165
list: 52.8850349101
tuple: 58.9864508751
```
**结论：当生成可迭代对象后并且不再进行改变，应该使用tuple节省内存；当生成集合用来进行检查某个值是否存在时，应该使用set来提高效率。**


### 尽可能将if语句放在循环外面

这是在很多书本上看到的建议，然而这么做的原因，我并没有找到详尽的解释，我自己总结出来的原因有这么几个： 
1. 如果可以把if放在循环外面，却放在循环里，就增加了很多不必要的判断 
2. 在计算机体系结构层面，if放在循环里容易引起分支预测错误，而分支回退要耗很多指令周期 
3. 在计算机体系结构层面，if放在循环里面会造成控制相关，影响指令并行(隐约记得在计算机体系结构这门课程中学过，然而记不太清了，有时间还是得复习复习相关知识=_=(计算机体系结构：量化研究方法，第三章：指令级并行及其开发))

 

