---
title: Linux-模块命令
tags: 2019年 08月 10号
notebook: 00技术笔记
---

# Linux-模块命令

## Linux 软件

### autopep8

autopep8 格式自动优化：代码规范
参考链接：http://hao.jobbole.com/autopep8/
命令：

```bash
autopep8 --in-place --aggressive --aggressive  test_model_logic_v2.py
```

### SVN

SVN 是 Subversion 的简称，是一个开放源代码的版本控制系统，相较于 RCS、CVS，它采用了分支管理系统，它的设计目标就是取代 CVS。互联网上很多版本控制服务已从 CVS 迁移到 Subversion。说得简单一点 SVN 就是用于多个人共同开发同一个项目，共用资源的目的。

#### SVN 常用命令

1. svn up
2. svn ci -m "update_msg" sss.py
3. svn log 展示给你主要信息：每个版本附加在版本上的作者与日期信息和所有路径修改。
4. svn diff 显示特定修改的行级详细信息。
5. svn cat 取得在特定版本的某一个文件显示在当前屏幕。
6. svn list 显示一个目录在某一版本存在的文件。
7. svn rename
8. svn merge

#### 删除目录下所有.svn

svn 删除版本库目录下所有中.svn 文件

```bash
# 方法1
find . -type d -name “.svn”|xargs rm -rf

# 方法2
find . -type d -iname ”.svn” -exec rm -rf {} \;
```

### Pylint

如何使用 Pylint 来规范 Python 代码风格
https://www.ibm.com/developerworks/cn/linux/l-cn-pylint/

pylint 的配置与使用
https://blog.csdn.net/jinguangliu/article/details/43674771

项目使用

```bash
Pylintp基础配置：
    见项目~/packages_py/1.sh  直接在项目虚拟环境中运行 sh 1.sh 即可安装pylint包
    见项目~/packages_py/pylint.conf 涉及pylint的相关参数
        Line65: disable=C,R,W,E,F # 表示忽略 pylint显示的错误级别
        Line113:ignored-calssed=optparse.Values,thread._local._thred._local # 表示忽略 项目代码中某些字符
    在项目目录中 server或者sqs层 运行命令 pylint --rcfile=~/packages_py/pylint.conf server/ 即可得到检查文档
        如在运行中报 server/__init__.py 文件存在 touch server/__init__.py 创建文件即可。
        如在运行中报 no function module ,说明命令中包含绝对路径，改为相对路径在指定位置运行即可。



项目使用：检查sqs或server的E F级别
    修改~/packages_py/pylint.conf
        Line65: disable=C,R,W,E,F 改为 disable=C,R,W
        由于scope_session报错过多 ，修改 Line113:ignored-calssed 后面加上 ,scope_session即可过滤.
    项目目录运行 pylint --rcfile=~/packages_py/pylint.conf server/ | tee check3.0.txt



项目使用：检查C注释中的 missing-docstring
    修改~/packages_py/pylint.conf
        Line65: disable=C,R,W,E,F 改为 disable=R,W,bad-whitespace,....... 等等 将 missing-docstring之外的Messages中的message id(检查文档中可得到)全部过滤即可
    项目目录运行  pylint --rcfile=~/packages_py/pylint.conf server/ | tee check3.0.txt

```

# Linux 技术笔记

## 查看 ipython 历史命令

由于 ipython 每次关闭后，没有日志文件，需要找回 ipython 的输入命令

两种办法：

1.  **用%hist**保存后把%开头的删掉再执行。
2.  **用%logstart 和%logstop**。它会把你所用的%命令对应的的 python 代码
    （如下面的 magic...）

```python
# %logstart 默认输出日志 ipython_log.py
In [7]: %logstart /tmp/test_log.py
In [8]: a = 10
In [9]: b = a*a
# 查看变量
In [10]: %who
a        b   
In [10]: %logstop
```

## 环境脚本头规范

每个 Script 头部信息

- Script 的功能
- Script 的版本信息
- script 的作者与联络方式
- script 的版权宣告方式
- script 的历史记录
- script 内特殊的指令，使用绝对路径的方式来下达
- script 运作时需要的环境变量预先宣告与设定

## 使用 vim 比对文件不同

```bash
 vim -d source.txt subject.txt
```

**效果如下所示**
![](https://blog-1254094716.cos.ap-chengdu.myqcloud.com/%E7%94%A8Vim%E6%9D%A5%E5%AF%B9%E6%AF%94%E4%B8%A4%E4%B8%AA%E6%96%87%E4%BB%B6%E7%9A%84%E4%B8%8D%E5%90%8C01.jpg)

## passwd 标准输入，设置用户密码

echo "PASSWORD" | passwd--stdin USERNAME

passwd[OPTIONS] UserName: 修改指定用户的密码，仅 root 用户权限

passwd: 修改自己的密码

常用选项：
-d：删除指定用户密码
-l:锁定指定用户
-u:解锁指定用户
-e:强制用户下次登录修改密码(密码马上过期:chage -d0 username)
-f：强制执行(配合其他选项使用)
-n mindays: 指定最短使用期限
-x maxdays：最大使用期限
-w warndays：提前多少天开始警告
-i inactivedays：非活动期限
--stdin：从标准输入接收用户密码
echo "PASSWORD" | passwd--stdin USERNAME

# Linux-模块命令

## Linux 软件

### autopep8

autopep8 格式自动优化：代码规范
参考链接：http://hao.jobbole.com/autopep8/
命令：

```bash
autopep8 --in-place --aggressive --aggressive  test_model_logic_v2.py
```

### SVN

SVN 是 Subversion 的简称，是一个开放源代码的版本控制系统，相较于 RCS、CVS，它采用了分支管理系统，它的设计目标就是取代 CVS。互联网上很多版本控制服务已从 CVS 迁移到 Subversion。说得简单一点 SVN 就是用于多个人共同开发同一个项目，共用资源的目的。

#### SVN 常用命令

1. svn up
2. svn ci -m "update_msg" sss.py
3. svn log 展示给你主要信息：每个版本附加在版本上的作者与日期信息和所有路径修改。
4. svn diff 显示特定修改的行级详细信息。
5. svn cat 取得在特定版本的某一个文件显示在当前屏幕。
6. svn list 显示一个目录在某一版本存在的文件。
7. svn rename
8. svn merge

#### 删除目录下所有.svn

svn 删除版本库目录下所有中.svn 文件

```bash
# 方法1
find . -type d -name “.svn”|xargs rm -rf

# 方法2
find . -type d -iname ”.svn” -exec rm -rf {} \;
```

### Pylint

如何使用 Pylint 来规范 Python 代码风格
https://www.ibm.com/developerworks/cn/linux/l-cn-pylint/

pylint 的配置与使用
https://blog.csdn.net/jinguangliu/article/details/43674771

项目使用

```bash
Pylintp基础配置：
    见项目~/packages_py/1.sh  直接在项目虚拟环境中运行 sh 1.sh 即可安装pylint包
    见项目~/packages_py/pylint.conf 涉及pylint的相关参数
        Line65: disable=C,R,W,E,F # 表示忽略 pylint显示的错误级别
        Line113:ignored-calssed=optparse.Values,thread._local._thred._local # 表示忽略 项目代码中某些字符
    在项目目录中 server或者sqs层 运行命令 pylint --rcfile=~/packages_py/pylint.conf server/ 即可得到检查文档
        如在运行中报 server/__init__.py 文件存在 touch server/__init__.py 创建文件即可。
        如在运行中报 no function module ,说明命令中包含绝对路径，改为相对路径在指定位置运行即可。



项目使用：检查sqs或server的E F级别
    修改~/packages_py/pylint.conf
        Line65: disable=C,R,W,E,F 改为 disable=C,R,W
        由于scope_session报错过多 ，修改 Line113:ignored-calssed 后面加上 ,scope_session即可过滤.
    项目目录运行 pylint --rcfile=~/packages_py/pylint.conf server/ | tee check3.0.txt



项目使用：检查C注释中的 missing-docstring
    修改~/packages_py/pylint.conf
        Line65: disable=C,R,W,E,F 改为 disable=R,W,bad-whitespace,....... 等等 将 missing-docstring之外的Messages中的message id(检查文档中可得到)全部过滤即可
    项目目录运行  pylint --rcfile=~/packages_py/pylint.conf server/ | tee check3.0.txt

```

# Linux 技术笔记

## 查看 ipython 历史命令

由于 ipython 每次关闭后，没有日志文件，需要找回 ipython 的输入命令

两种办法：

1.  **用%hist**保存后把%开头的删掉再执行。
2.  **用%logstart 和%logstop**。它会把你所用的%命令对应的的 python 代码
    （如下面的 magic...）

```python
# %logstart 默认输出日志 ipython_log.py
In [7]: %logstart /tmp/test_log.py
In [8]: a = 10
In [9]: b = a*a
# 查看变量
In [10]: %who
a        b   
In [10]: %logstop
```

## 环境脚本头规范

每个 Script 头部信息

- Script 的功能
- Script 的版本信息
- script 的作者与联络方式
- script 的版权宣告方式
- script 的历史记录
- script 内特殊的指令，使用绝对路径的方式来下达
- script 运作时需要的环境变量预先宣告与设定

## 使用 vim 比对文件不同

```bash
 vim -d source.txt subject.txt
```

**效果如下所示**
![](https://blog-1254094716.cos.ap-chengdu.myqcloud.com/%E7%94%A8Vim%E6%9D%A5%E5%AF%B9%E6%AF%94%E4%B8%A4%E4%B8%AA%E6%96%87%E4%BB%B6%E7%9A%84%E4%B8%8D%E5%90%8C01.jpg)

## passwd 标准输入，设置用户密码

echo "PASSWORD" | passwd--stdin USERNAME

passwd[OPTIONS] UserName: 修改指定用户的密码，仅 root 用户权限

passwd: 修改自己的密码

常用选项：
-d：删除指定用户密码
-l:锁定指定用户
-u:解锁指定用户
-e:强制用户下次登录修改密码(密码马上过期:chage -d0 username)
-f：强制执行(配合其他选项使用)
-n mindays: 指定最短使用期限
-x maxdays：最大使用期限
-w warndays：提前多少天开始警告
-i inactivedays：非活动期限
--stdin：从标准输入接收用户密码
echo "PASSWORD" | passwd--stdin USERNAME

# Linux 常见问题

### yum-database disk image is malformed

错误：database disk image is malformed  
解决方法：yum clean dbcache

```bash
[root@WOM ~]# yum install vim -y
已加载插件：fastestmirror, refresh-packagekit, security
设置安装进程
Loading mirror speeds from cached hostfile
* base: mirrors.shu.edu.cn
* epel: mirrors.tongji.edu.cn
* extras: mirrors.shu.edu.cn
* updates: mirrors.shu.edu.cn
错误：database disk image is malformed
[root@WOM ~]# yum clean dbcache
已加载插件：fastestmirror, refresh-packagekit, security
Cleaning repos: base bintray--sbt-rpm epel extras updates
8 sqlite 文件已删除
```

# Linux 编译基础知识

https://blog.csdn.net/qq_41035588/article/details/80296051

https://blog.csdn.net/Com_ma/article/details/79414952

https://www.cnblogs.com/stefan-liu/p/5172424.html

https://pandas.pydata.org/pandas-docs/stable/10min.html

https://blog.csdn.net/su_buju/article/details/77144582

# Linux 常用软件

[toc]

## virtualenv

虚拟环境

virtualenv 用于创建独立的 Python 环境，多个 Python 相互独立，互不影响，它能够：

1. 在没有权限的情况下安装新套件
2. 不同应用可以使用不同的套件版本
3. 套件升级不影响其他应用

```bash
# 安装
pip install virtualenv

# 创建虚拟环境
vitualenv XXX

# 创建独立，无root包依赖的环境
virtualenv --no-site-packages [虚拟环境名称]

# 启动环境
. ~/env/bin/activate     或
source ~/env/bin/activate
```

## virtualenvwrapper

virtualenv 管理软件

Virtaulenvwrapper 是 virtualenv 的扩展包，用于更方便管理虚拟环境，它可以做：

1. 将所有虚拟环境整合在一个目录下
2. 管理（新增，删除，复制）虚拟环境
3. 切换虚拟环境
4. ...

```bash
# 安装使用 virtualenvwrapper
pip install virtualenvwrapper
- mkdir $HOME/.virtualenvs
- 在~/.bashrc中添加行： export WORKON_HOME=$HOME/.virtualenvs
- 在~/.bashrc中添加行：source /usr/bin/virtualenvwrapper.sh
- 运行： source ~/.bashrc

# 常用命令
lsvirtualenv   列出虚拟环境列表
mkvirtualenv 新建虚拟环境
workon        启动/切换虚拟环境
rmvirtualenv  删除虚拟环境
deactivate     离开虚拟环境
```
