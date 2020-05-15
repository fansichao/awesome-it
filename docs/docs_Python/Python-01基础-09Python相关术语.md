---
title: Python基础-09Python相关术语.md
tags: 2019年 08月 10号
notebook: 00技术笔记
---

# 术语大全

值(value)：就是在程序中，我们操作数据的基本单位，举例：”www.iplaypy.com”
类型(type)：python type，值在 Python 中的类别，常见的类型我们在 Python 基础数据类型那篇文章中有详细介绍。
整型(integer)：又叫做整数类型，用来表达整数的数据类型。
浮点数(floating point)： 用来表示带小数部分的数。
字符串(string)：用来表示一串字符的类型。
变量(variable)：引用一个值，这个值的名称。
语句(statement)：表示一个命令或行动的一段代码，我们见过赋值语句和 print 输出语句。
赋值(assignment)：就是将一个值，赋值给一个变量。
关键字(keyword)：这个关键词，这不是我们搜索引擎优化(SEO)中介绍的概念，它是 Python 内部保留的词，变量名一定不要使用系统关键字。
操作符(operator)：用来表示简单的运算的特殊符号，像：加法、乘法和字符器拼接等。
python 注释(comment)：代码中可以附加一些我们的注解信息，用来帮助我们调试程序时使用，也可以放入帮助文档信息，这是基础知识之中的基础。

生成器：在 Python 中，这种一边循环一边计算的机制，称为生成器：generator。
可迭代对象：可以直接作用于 for 循环的对象统称为可迭代对象：Iterable。
迭代器：可以被 next()函数调用并不断返回下一个值的对象称为迭代器：Iterator。
集合数据类型如 list、dict、str 等是 Iterable 但不是 Iterator，不过可以通过 iter()函数获得一个 Iterator 对象。
软件开发中的一个原则“开放-封闭”原则；
封闭：已实现的功能代码块不应该被修改
开放：对现有功能的扩展开放
高阶函数，就是把一个函数当做一个参数传给另外一个函数
匿名函数 lambda 与正常函数的区别是什么？ 最直接的区别是，正常函数定义时需要写名字，但 lambda 不需要。
模块，用一砣代码实现了某个功能的代码集合。
json 模块，用于字符串 和 python 数据类型间进行转换；Json 模块提供了四个功能：dumps、dump、loads、load
pickle 模块，用于 python 特有的类型 和 python 的数据类型间进行转换；pickle 模块提供了四个功能：dumps、dump、loads、load
xml 是实现不同语言或程序之间进行数据交换的协议，跟 json 差不多，但 json 使用起来更简单，不过，古时候，在 json 还没诞生的黑暗年代，大家只能选择用 xml 呀
散列消息鉴别码，简称 HMAC，是一种基于消息鉴别码 MAC（Message Authentication Code）的鉴别机制。使用 HMAC 时,消息通讯的双方，通过验证消息中加入的鉴别密钥 K 来鉴别消息的真伪；

# 参考资源

**参考资源**

- [Python3 术语对照表](https://docs.python.org/zh-cn/3.8/glossary.html)
- [IT 行业术语大全](http://www.fly63.com/article/detial/1411)
- [Python 术语中英文对照表](https://blog.csdn.net/qq_41420747/article/details/81534860)

函数式编程
