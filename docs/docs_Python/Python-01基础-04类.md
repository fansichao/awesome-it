# Python基础-04类

类

## 类的定义（__init__方法，基类，self

类的定义：class ClassName(object):，object是父类名，object是一切类的基类。
__init__方法是函数写在类中就是方法，实例化对象的时候必须调用__init__方法。


## 类的属性


属性的本质就是变量。



## 私有化





```python
对于Python中的类属性，可以通过双下划线”__”来实现一定程度的私有化。
“ _”和“ __”的使用 更多的是一种规范/约定，没有真正达到限制的目的。
“_”：以单下划线开头只能允许其本身与子类进行访问，(起到一个保护的作用)。
“__”：双下划线的表示的是私有类型的变量。这类属性在运行时属性名会加上单下划线和类名。
“__foo__”：以双下划线开头和结尾的（__foo__）代表python里特殊方法专用的标识，如 __init__（）。
```





## 面向对象的三大特性：封装、继承、多态


# 参考链接:


- [Python类说明: https://blog.csdn.net/qq_35732147/article/details/83084774](https://blog.csdn.net/qq_35732147/article/details/83084774)
- [Python类术语: https://www.cnblogs.com/chengd/articles/7287528.html](https://www.cnblogs.com/chengd/articles/7287528.html)


- [Python类入门]( https://www.runoob.com/python3/python3-class.html)
- 























