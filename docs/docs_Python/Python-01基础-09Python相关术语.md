---
title: Python基础-09Python相关术语.md
tags: 2019年 08月 10号
notebook: 00技术笔记
---


# 术语大全

值(value)：就是在程序中，我们操作数据的基本单位，举例：”www.iplaypy.com” 
类型(type)：python type，值在Python中的类别，常见的类型我们在Python基础数据类型那篇文章中有详细介绍。 
整型(integer)：又叫做整数类型，用来表达整数的数据类型。 
浮点数(floating point)： 用来表示带小数部分的数。 
字符串(string)：用来表示一串字符的类型。 
变量(variable)：引用一个值，这个值的名称。 
语句(statement)：表示一个命令或行动的一段代码，我们见过赋值语句和print输出语句。 
赋值(assignment)：就是将一个值，赋值给一个变量。 
关键字(keyword)：这个关键词，这不是我们搜索引擎优化(SEO)中介绍的概念，它是Python内部保留的词，变量名一定不要使用系统关键字。 
操作符(operator)：用来表示简单的运算的特殊符号，像：加法、乘法和字符器拼接等。 
python 注释(comment)：代码中可以附加一些我们的注解信息，用来帮助我们调试程序时使用，也可以放入帮助文档信息，这是基础知识之中的基础。

生成器：在Python中，这种一边循环一边计算的机制，称为生成器：generator。
可迭代对象：可以直接作用于for循环的对象统称为可迭代对象：Iterable。
迭代器：可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator。
集合数据类型如list、dict、str等是Iterable但不是Iterator，不过可以通过iter()函数获得一个Iterator对象。
软件开发中的一个原则“开放-封闭”原则；
封闭：已实现的功能代码块不应该被修改
开放：对现有功能的扩展开放
高阶函数，就是把一个函数当做一个参数传给另外一个函数
匿名函数lambda与正常函数的区别是什么？ 最直接的区别是，正常函数定义时需要写名字，但lambda不需要。
模块，用一砣代码实现了某个功能的代码集合。 
json模块，用于字符串 和 python数据类型间进行转换；Json模块提供了四个功能：dumps、dump、loads、load
pickle模块，用于python特有的类型 和 python的数据类型间进行转换；pickle模块提供了四个功能：dumps、dump、loads、load
xml 是实现不同语言或程序之间进行数据交换的协议，跟json差不多，但json使用起来更简单，不过，古时候，在json还没诞生的黑暗年代，大家只能选择用xml呀
散列消息鉴别码，简称HMAC，是一种基于消息鉴别码MAC（Message Authentication Code）的鉴别机制。使用HMAC时,消息通讯的双方，通过验证消息中加入的鉴别密钥K来鉴别消息的真伪；



# 参考资源

**参考资源**
- [Python3术语对照表](https://docs.python.org/zh-cn/3.8/glossary.html)
- [IT行业术语大全](http://www.fly63.com/article/detial/1411)
- [Python术语中英文对照表](https://blog.csdn.net/qq_41420747/article/details/81534860)



函数式编程

