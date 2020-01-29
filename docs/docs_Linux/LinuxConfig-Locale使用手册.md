# Linux-Locale 介绍说明

<!-- TOC -->autoauto- [Linux-Locale 介绍说明](#linux-locale-介绍说明)auto    - [Locale 基本概念](#locale-基本概念)auto        - [locale 涉及到的配置](#locale-涉及到的配置)auto        - [locale 涉及到的环境变量](#locale-涉及到的环境变量)auto        - [Locale 常量含义](#locale-常量含义)auto    - [Locale 常用命令](#locale-常用命令)autoauto<!-- /TOC -->

Locale 是根据计算机用户所使用的语言，所在国家或者地区，以及当地的文化传统所定义的一个软件运行时的语言环境。

Locale 包括语言(Language), 地域 (Territory) 和字符集(Codeset)。
一个 locale 的书写格式为: **语言[\_地域[.字符集]]**。
完全的 locale 表达方式是 **[语言[\_地域][.字符集] [@修正值]**。
zh*CN.GB2312 ＝中文*中华人民共和国＋国标 2312 字符集。

## Locale 基本概念

```bash
1 名称：
    对外的接口，用来建立（语系+字符集）的映射关系
2 语系：
    决定了该语言包括哪些字符（unicode的字符序号来定义的，字符序号和字符编码不是一回事，字符序号是统一的），以及这些字符的表现格式等
3 字符集：
    用于该语系的字符编码
4 字体
    用于把字符集的编码转换成屏幕上的字体显示
```

### locale 涉及到的配置

```bash
1 /etc/sysconfig/i18n：
    设置默认的语系名称（缺省设置，每个登录用户可以自己设置来覆盖缺省值）
2 /usr/lib/locale/：
    语系名称文件（记录所有 语系+字符集 的映射关系）
3 /usr/share/i18n/locales/：
    所有的语系文件（记录语系中包含哪些字符序号，有哪些表现形式）
4 /usr/share/i18n/charmaps/：
    所有的字符编码文件
```

### locale 涉及到的环境变量

```bash
1 LC_ALL
2 LC_*
3 LANG（环境变量，通常用这个就行了）
4 LC_ALL > LC_* > LANG
```

### Locale 常量含义

```bash
LANG=语言
LC_CTYPE=语言符号及分类
LC_NUMERIC=数字
LC_TIME=时间
LC_COLLATE=比较和习惯
LC_MONETARY=货币
LC_MESSAGES=信息表达
LC_PAPER=默认纸张尺寸大小
LC_NAME=姓名书写方式
LC_ADDRESS=地址书写方式
LC_TELEPHONE=电话号码书写方式
LC_MEASUREMENT=度量衡表达方式
LC_IDENTIFICATION=对locale自身包含信息的概述
LC_ALL=
```

从优先级角度：LC*ALL > LC*\* > LANG

## Locale 常用命令

```bash
# 查看现有语言环境
locale
# 可用语言环境
locale -a
# 临时修改语言环境
export LANG=en_US.UTF-8
export LANG=zh_CN.UTF-8
```

**永久修改系统级字符集**

```bash

/etc/sysconfig/i18n
# 英文版系统：
LANG="en_US.UTF-8"
SYSFONT="latarcyrheb-sun16"

# 中文版系统：
LANG="zh_CN.UTF-8"或者LANG="zh_CN.gbk"
SYSFONT="latarcyrheb-sun16"

```
