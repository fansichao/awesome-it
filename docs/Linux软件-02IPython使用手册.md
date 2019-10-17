<!--
 * @Author: Scfan
 * @Date: 2019-07-07 00:53:00
 * @LastEditors: Scfan
 * @LastEditTime: 2019-08-10 20:37:04
 * @Description: 工作&学习&生活
 * @Email: 643566992@qq.com
 * @Company: 上海
 * @version: V1.0
 -->
# Linux-IPython使用手册

IPython是python的一个交互式shell，它比默认的“python shell”更方便，支持变量自动补全，自动缩进，支持 bash shell 命令，内置了许多强大的功能和函数。

IPython 是基于BSD 开源的，并且IPython为交互式计算提供了一个丰富的架构。

**IPython特色**
- 强大的交互式shell
- 供Jupyter notebooks使用的Jupyter内核
- 交互式的数据可视化工具
- 灵活、可嵌入的解释器
- 易于使用，高性能的并行计算工具
 


## IPython使用技巧

IPython中 ```%```调用IPython命令

### Tab键自动补全

在shell中输入表达式时，按下Tab键可将当前命名空间中任何与已输入的字符串相匹配的变量（对象、函数等）显示出来

### 中断正在执行的代码
当代码正在执行时，需要终止代码运行，则只需按下“Ctrl+C”，就会引发一个KeyboardInterrupt，除一些特殊的情况以外，绝大部分Python程序会立即停止执行。
键盘中的快捷键
使用IPython编码时还可使用键盘快捷键来快速完成所需操作，常用的键盘快捷键（IPython环境下）如下表所示。

### 内置命令-记录 (%logstart)

记录输入的命令

```python
In [2]: %logstart
Activating auto-logging. Current session state plus future input saved.
Filename       : ipython_log.py
Mode           : rotate
Output logging : False
Raw input log  : False
Timestamping   : False
State          : active
```

### 内置命令-执行系统命令 (!)

```python
In [6]: !hostname
neo4j.yinsho.com
```


### 内置命令-内省 (?)
当某对象的信息不是很明确时，可以在变量的前面或后面加上问号（？），有关该对象的一些通用信息就会显示出来，如下图所示。

```python
# 查看变量或函数
In [4]: ?a
Type:        int
String form: 1
Docstring:  
int(x=0) -> int or long
int(x, base=10) -> int or long


# 打印函数的源码
In [15]: func??            
Signature: func()
Source:   
def func():
	print("hello world")
File:      /<ipython-input-13-4475a92670e6>
Type:      function

    

```

### 内置命令-执行文件代码 (%run)
```python
In [29]: !vi test.py

In [30]: !cat test.py
def func1():
	print("hello world")

func1()

In [31]: %run "test.py"
hello world
```

 
### 目录书签系统 (%bookmark)

**目录书签**，类似于快捷方式

```python
# 定义 local 书签
In [37]: %bookmark local /usr/local
# 查看所有书签
In [38]: %bookmark -l
Current bookmarks:
local -> /usr/local
# 使用书签.
In [39]: cd local
(bookmark:local) -> /usr/local
/usr/local
# 覆盖之前书签
In [41]: %bookmark local /etc/sysconfig
```


### 其他命令

- %paste和%cpaste命令执行剪帖板代码
- 使用上箭头或下箭头可以查看上一条命令或下一条命令的历史
- _i48 执行第48条命令
- __ 执行前面倒数第一条命令
- 输入与输出主要是使用 _、__、_X、_iX，这里的X表示行号
- %dhist  ：打印目录访问的历史
- %env :以dict的形式返回系统的环境变量

## Ipython高级使用

日志处理、代码调试、性能分析、自定义主题

## IPython附件

### 快捷键

| 快捷键          | 作用               |
|--------------|------------------|
| Ctrl+P或向上箭头  | 后向搜索命令           |
| Ctrl+N或向下箭头  | 前向搜索命令           |
| Ctrl+R       | 按行读取反向历史搜索（部分匹配） |
| Ctrl+Shift+V | 从剪切板粘贴文本         |
| Ctrl+A       | 将光标移动到行首         |
| Ctrl+E       | 将光标移动到行尾         |
| Ctrl+K       | 删除从光标开始至行尾的文本    |
| Ctrl+U       | 清除从光标开始至行首的文本    |
| Ctrl+F       | 将光标向前移动一个字符      |
| Ctrl+B       | 将光标向后移动一个字符      |
| Ctrl+L       | 清屏               |
 
### 魔术命令

```python
%quickref                   显示ipython的快速参考
%magic                      显示所有的魔术命令的详细文档
%debug                      从最新的异常跟踪的底部进入交互式调试器
%hist                       打印命令的输入(可选输出)历史
%pdb                        在异常发生后自动进入调试器
%paste                      执行剪贴板中的python代码
%cpaste                     打开一个特殊提示符以便手工粘贴待执行的python代码
%reset                      删除interactive命名空间中的全部变量/名称
%page OBJECT                通过分页器打印输出object
%run script.py              在ipython中执行一个python脚本文件
%prun statement             通过cprofile执行statement,并打印分析器的输出结果
%time statement             报告statement的执行时间
%timeit statement           多次执行statement以计算系统平均执行时间.对那么执行时间非常小的代码很有用
%who,%who_id,%whos          显示interactive命名空间中定义的变量,信息级别/冗余度可变
%xdel variable              删除variable,并尝试清除其在ipython中的对象上的一切引用
```

### 调试器命令 (%debug)

**debug调试器样例**
```python
In [11]: %debug  
> <ipython-input-10-0ee88489e9f0>(1)<module>()
----> 1 func%debug
ipdb> 

设置断点单步调度 
%run -d script.py

s 进入脚本 ， 
b 13 # 在13行设置断点 
c # continue till touch the break point 
n # 执行下一行。 
如果有exception 报出：throws_an_exception , 
ipdb> s # 单步进入 exception 那行. 
ipdb> !a #在变量a 前加 ! 查看 变量内容
```

pdb 是 python 自带的一个包，为 python 程序提供了一种交互的源代码调试功能，
主要特性包括设置断点、单步调试、进入函数调试、查看当前代码、查看栈片段、动态改变变量的值等。pdb 提供了一些常用的调试命令 


**pdb 调试器命令列表**
```python
h(help)                 显示命令列表
help command            显示command的文档
c(continue)             恢复程序的执行
q(quit)                 退出调试器,不再执行任何代码
b(break) n              在当前文件的第n行设置一个断点
b path/to/file.py:n     在指定文件的第n行设置一个断点
s(step)                 单步进入函数调用
n(next)                 执行当前行,并前进到当前级别的下一行
u(up)/d(down)           在函数调用栈中向上或向下移动
a(args)                 显示当前函数的参数
debug statement         在新的递归调试器中调用语句statement
l(list) statement       显示当前行,以及当前栈级别上的上下文参考代码
w(where)                打印当前位置的完整栈跟踪(包括上下文参考代码)
```


## 资源

IPython用法详解: https://www.cnblogs.com/renpingsheng/p/7759797.html








