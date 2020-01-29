# Linux基础知识

## 术语

 字符集就是字符，尤其是非英语字符在系统内的编码方式，也就是通常所说的内码，所有的字符集都放在/usr/share/i18n/charmaps，所有的字符集也都是用Unicode编号索引的。

## 操作系统

### 标准输入输出

Linux的大部分命令都具有标准的输入/输出设备端口，下图列出了标准设备信息:

| 名称     | 描述 | 含义     | 设备   | 说明                  |
|--------|------|--------|------|---------------------|
| STDIN  | 0    | 标准输入   | 键盘   | 命令在执行时所要的输入数据通过它来取得 |
| STDOUT | 1    | 标准输出   | 显示器  | 命令在执行后的输出结果从该端口送出   |
| STDERR | 2    | 标准错误   | 显示器  | 命令执行时的错误信息通过该端口送出   |

### .bash_profile 文件介绍

**/etc/profile**
此文件为系统的每个用户设置环境信息,当用户第一次登录时,该文件被执行.
并从/etc/profile.d目录的配置文件中搜集shell的设置.

**/etc/bashrc**
为每一个运行bash shell的用户执行此文件.当bash shell被打开时,该文件被读取.

**~/.bash_profile**
每个用户都可使用该文件输入专用于自己使用的shell信息,当用户登录时,该
文件仅仅执行一次!默认情况下,他设置一些环境变量,执行用户的.bashrc文件.

**~/.bashrc**
该文件包含专用于你的bash shell的bash信息,当登录时以及每次打开新的shell时,该
该文件被读取.

**~/.bash_logout**
当每次退出系统(退出bash shell)时,执行该文件.




### X86、X64和X86_64区别

参考链接：[https://blog.csdn.net/u010758410/article/details/76320530](https://blog.csdn.net/u010758410/article/details/76320530)

- **X86:** intel的开发的一种32位指令集.
- **X86_64:** x86 CPU开始迈向64位的时候
- **X64:** x86_64,x64,AMD64基本上是同一个东西.一种64位指令集

x86、x86_64主要的区别就是32位和64位的问题，x86中只有8个32位通用寄存器.
x86_64把这8个通用寄存器扩展成了64位的，并且比x86增加了若干个寄存器 



# 代码开发原则


## 代码**开发原则**

1. **SRP单一职责原则(Single Responsibility Principle)**：就一个类而言，应该仅有一个引起它变化的原因。
2. **OCP开放-封闭原则(Open Closure Principle)**：软件实体(类，模块，函数等)应该可以扩展的，但不可修改。
3. **LSPLiskov 替换原则(Liskov Substitution Principle)**：子类型必须能够替换它们的基类型
4. **DIP依赖倒置原则(Dependence Inversion Principle)**：抽象不应该依赖于细节，细节应该依赖于抽象。
5. **ISP接口隔离原则(Interface Segregation Principle)**：不应该强迫客户依赖与它们不用的方法。接口属于客户，不属于它所在的类层次结构。
6. **REP重用发布等价原则(Release Reuse Equivalency Principle**)：重用粒度就是发布粒度。
7. **CCP共同封闭原则(Common Closure Principle)**：包中 所有类应该对于同一类性质的变化应该是共同封闭的。一个变化若对包产生影响，则将对包中所有的类产生影响。而对其它的包不造成影响。
8. **CRP共同重用原则(Common Resue Principle)**：一个包中的所有类应该是共同重用的。如果重用了包中的一个类，那么就要重用包中的所有类。
9. **ADP无环依赖原则(Acyclic Dependencies Principle)**：在包的依赖关系图中不允许存在环。
10. **SDP稳定依赖原则(Stable Dependencies Principle)**：易变化包不应该依赖稳定包。
11. **SAP稳定抽象原则(Stable Abstract Principle)**：朝着抽象方向扩展。
12. 详细描述参考链接： https://blog.csdn.net/qq_16234613/article/details/54933742?utm_source=copy


## **ORM**说明
  
1. **对象关系映射**(英语：(Object Relational Mapping，简称ORM，或O/RM，或O/R mapping)，是一种程序技术，用于实现面向对象编程语言里不同类型系统的数据之间的转换
2. **对象关系映射**(Object-Relational Mapping)提供了概念性的、易于理解的模型化数据的方法。ORM方法论基于三个核心原则： 简单：以最基本的形式建模数据。 传达性：数据库结构被任何人都能理解的语言文档化。 精确性：基于数据模型创建正确标准化的结构。



### PIP安装和解压安装的区别

pip安装会检查依赖软件，依赖没有安转，则无法安装。安装成功即完全OK
解压安转，先安装成功，程序运行的时候，会缺失相关依赖，需要后续安装。

### 编码，gbk和utf-8的区别 

gbk-包含简体中文和繁体，空间较小，占用空间少，运行速度快。     ps:gb2312 只支持简体中文字符
utf-8支持所有国家的语言，占用空间大，运行速度较慢

