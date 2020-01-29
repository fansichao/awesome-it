# 代码优化工具

Python作为高级编程语言，对于其性能要求也越来越注重。

**本文总结：**

性能优化的主要方法: 多进程处理，工具检测性能消耗完善代码，使用Cython扩展等。


## 说明


### 代码优化工具列表


**代码优化工具列表**
| 优化工具         | 工具说明            |
|-----------------|-------------------|
| PyLint          | 语法检查工具            |
| vprof           | 运行时间和内存分析器。图形化工具。 |
| cProfile        | 查询消耗时间最久的方法函数     |
| line_profile    | 查看耗时函数中的行耗时       |
| timeit          | 模块计算代码执行时间        |
| memory_profiler | 诊断内存的用量           |

### 代码常见性能优化指标


**机器性能指标**
- CPU
- IO
- MEM 内存
- NET 网络

**常见性能指标**
- 响应时间
- 错误率
- 吞吐率
- 执行时间
- 内存占用

### 优化方法小结

**方法小结:**
- 使用 cProfile, cStringIO 和 cPickle等用c实现相同功能
- 使用 c 扩展。目前主要有CPython(python最常见的实现的方式)原生API, ctypes,Cython，cffi三种方式
- 并行编程 multiprocessing
- 大杀器PyPy
- CUDA编程


## 相关资源



[Python应用与优化所必备的6个基本库](http://www.elecfans.com/emb/579616.html)


### 运行时间-vprof图表化

[vprof代码检测工具](https://blog.csdn.net/budong282712018/article/details/80281912)
[vprof官网](https://github.com/nvdv/vprof)


**vprof简单使用**
```python
pip3 install vprof
# 直接运行代码
vprof -c h test.py
# 带输入参数
vprof -c cmh "testscript.py --foo --bar"
```

### 运行时间-gprof2dot图表化（强烈推荐）

[gprof2dot官网](https://github.com/jrfonseca/gprof2dot)


**cProfile+gprof2dot简单使用**
```python
sudo pip3 install gprof2dot
# 先用cProfile生成分析报告
python3 -m cProfile -o output.pstats test.py
# 使用 gprof2dot 画图
gprof2dot -f pstats output.pstats | dot -Tpng -o output.png
```

### 编译优化-PyPy


**PyPy是用RPython(CPython的子集)实现的Python，使用了Just-in-Time(JIT)编译器，即动态编译器，**
与静态编译器(如gcc,javac等)不同，它是利用程序运行的过程的数据进行优化。
如果python程序中含有C扩展(非cffi的方式)，JIT的优化效果会大打折扣，甚至比CPython慢（比Numpy）。

所以在PyPy中最好用纯Python或使用cffi扩展。


> PyPy优势在于使用JIT动态编译，对于运行的函数会生成一个类C的函数。
编译成机器码，下次调用函数时，会直接调用机器码，速度得到质的飞跃。
但是由于本身编译机器码需要时间。

> 所以很多 JIT 实现都会先解释执行，然后确定了一段代码经常被执行之后，再进行编译。并且分多层 JIT，比较初级的对编译出来的机器码不做比较复杂的优化.

 

### 运行时间-上下文管理器

用上下文管理器测量部分代码运行时间
```python
from time import clock
class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
 
    def __enter__(self):
        self.start = clock()
        return self
 
    def __exit__(self, *args):
        self.end = clock()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs
 
if __name__ == "__main__":
 
    with Timer() as t:
        replace_str = ""
        for i, char in enumerate(orignal_str * 10000):
            c = char if char != " " else "-"
            replace_str += c
    print t.secs

```


### 内存-objgraph



objgraph是一个非常轻巧的工具，但在排查内存泄露的时候非常有用。
objgraph的代码很短，只有一个文件，其主要依靠标准库中的gc模块来获取对象之间的创建引用关系。objgraph使用起来十分简单，

```python
# 列出最多实例的类型
objgraph.show_most_common_types(shortnames=False)
# 显示两次调用之间的对象数量变化
objgraph.show_growth(limit=None)
# 获取指定类型的对象
objgraph.by_type('Foobar')
# 查找反向引用
objgraph.find_backref_chain(obj, objgraph.is_proper_module)
```

在遇到内存泄露问题时候首先考虑下用objgraph来进行查看，没有问题的时候也可以学习下它的代码，可以极大了解gc模块的应用。

### 内存-tracemalloc
 
tracemalloc是用来分析Python程序内存分配的工具，使用上也很简单，

```python
import tracemalloc
tracemalloc.start()

# ... run your application ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
```
snapshot结果中可以看到每个模块最终创建分配的内存大小，在追查内存问题上很有帮助。
Python 3.5.x之后将tracemalloc集成到了标准库当中 





### 编码规范-autopep8

Autopep8是一个将python代码自动编排的一个工具，它使用pep8工具来决定代码中的那部分需要被排。
，Autopep8可以修复大部分pep8工具中报告的排版问题。很多人都知道  Ctrl+Alt+L 也可以排版，快捷键只是可以简单的排版。
跟Autopep8是无法相比的。 


```python
# autopep8 使用命令
autopep8 --in-place --aggressive --aggressive file.py
```


































































