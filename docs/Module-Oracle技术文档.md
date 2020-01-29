# Oracle技术文档.md

tags: Oracle

环境说明:

- Oracle11g
- CentOS6.10/CentOS7.5

## 功能(可选-建议操作)

### Oracel exp 导出空表数据

TODO 寻找更好导出空表的方法

问题原因:

由于Oracle11g新特性，当表无数据时，不分配segment，以节省空间。而导出时只会导出已分配segment的表

解决步骤:

**第一步:** 修改系统配置

设置deferred_segment_creation参数

```sql
SQL> show parameter deferred_segment_creation 
NAME                                 TYPE        VALUE 
------------------------------------ ----------- ------------------------------ 
deferred_segment_creation            boolean     TRUE 
SQL> alter system set deferred_segment_creation=false; 
系统已更改。
SQL> show parameter deferred_segment_creation 
NAME                                 TYPE        VALUE 
------------------------------------ ----------- ------------------------------ 
deferred_segment_creation            boolean     FALSE
```

**注意**: 该值设置后对以前导入的空表不产生作用，仍不能导出，只能对后面新增的表产生作用。如需导出之前的空表,只能使用后续方法。

**第二步: **处理空表

方法1: 批量处理空表

```sql
-- 首先使用下面的sql语句查询一下当前用户下的所有空表
select table_name from user_tables where NUM_ROWS=0 or num_rows is null;

然后用一下SQL语句执行查询
-- select 'alter table '||table_name||' allocate extent;' from user_tables where num_rows=0 or num_rows is null;

-- 查询结果如下所示..
alter table TBL_1 allocate extent;
alter table TBL_2 allocate extent;
alter table TBL_3 allocate extent;
alter table TBL_4 allocate extent;
-- 执行上面语句即可
```

**方法2:** insert一行，再rollback就产生segment了

该方法是在在空表中插入数据，再删除，则产生segment。导出时则可导出空表。

参考链接: [Oracle导出空表](https://www.cnblogs.com/ningvsban/p/3603678.html)

### Oracle数据导入导出

Oracle导入导出命令

```bash
# 导出数据
exp fdm/qwe1234@192.168.100.165:1521/newfdm file=20190514_newfdm.db owner=fdm
# 导入前需要删除原有数据库所有表+序列
imp fdm/qwe123 file=/home/oracle/20190514_newfdm.db fromuser=fdm touser=fdm DESTROY=Y
```

**导出日志查看**.配置 <导出空表数据> 后即可导出空表 xxx 0行

```bash
[oracle@WOM ~]$ exp fdm/qwe123@192.168.172.70:1521/fdm file=fdm.db owner=fdm
Export: Release 11.2.0.1.0 - Production on 星期三 10月 23 17:09:59 2019
Copyright (c) 1982, 2009, Oracle and/or its affiliates.  All rights reserved.
连接到: Oracle Database 11g Enterprise Edition Release 11.2.0.1.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
已导出 UTF8 字符集和 AL16UTF16 NCHAR 字符集
服务器使用 AL32UTF8 字符集 (可能的字符集转换)

即将导出指定的用户...
. 正在导出 pre-schema 过程对象和操作
. 正在导出用户 FDM 的外部函数库名
. 导出 PUBLIC 类型同义词
. 正在导出专用类型同义词
. 正在导出用户 FDM 的对象类型定义
即将导出 FDM 的对象...
. 正在导出数据库链接
. 正在导出序号
. 正在导出簇定义
. 即将导出 FDM 的表通过常规路径...
. . 正在导出表              ASSISTANT_ANALYSIS导出了           0 行
. . 正在导出表               BACK_MINING_MODEL导出了           5 行
. . 正在导出表        BACK_MINING_MODEL_ENTITY导出了          38 行
. . 正在导出表                         WEB_LOG导出了        1463 行
. 正在导出同义词
. 正在导出视图
. 正在导出存储过程
. 正在导出运算符
. 正在导出引用完整性约束条件
. 正在导出触发器
. 正在导出索引类型
. 正在导出位图, 功能性索引和可扩展索引
. 正在导出后期表活动
. 正在导出实体化视图
. 正在导出快照日志
. 正在导出作业队列
. 正在导出刷新组和子组
. 正在导出维
. 正在导出 post-schema 过程对象和操作
. 正在导出统计信息
导出成功终止, 但出现警告。
```
