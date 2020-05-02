# Oracle 技术文档.md

tags: Oracle

环境说明:

- Oracle11g
- CentOS6.10/CentOS7.5

## 常用功能

### 创建用户&授权

Oracle 用户

```sql
$sqlplus / as sysdba
create user fdm identified by qwe123;
grant dba to fdm;
```

### 数据库自启动

```bash
数据库自启动
# vi /etc/oratab
# 找到 fdm:/u01/app/oracle/11g:N   # 实际名称和路径可能略有不同，和 $ORACLE_BASE有关
# 修改为 fdm:/u01/app/oracle/11g:Y

# vi /etc/rc.d/rc.local  删除中文
su oracle -lc " /u01/app/oracle/11g/bin/lsnrctl start"   # 路径是 $ORACLE_HOME+/bin/ lsnrctl start"
su oracle -lc /u01/app/oracle/11g/bin/dbstart
```

### 配置项目环境(`Oracle驱动`)

详见问题 `libclntsh.so: cannot open shared object file`

解决方法

```bash
yum install -y oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm
sudo sh -c "echo /usr/lib/oracle/12.2/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf"
sudo ldconfig
# 添加到/etc/profile
export LD_LIBRARY_PATH=/usr/lib/oracle/12.2/client64/lib:$LD_LIBRARY_PATH
# 执行命令
source /etc/profile
```

## 可选功能

### Oracel exp 导出空表数据

TODO 寻找更好导出空表的方法

问题原因:

由于 Oracle11g 新特性，当表无数据时，不分配 segment，以节省空间。而导出时只会导出已分配 segment 的表

解决步骤:

**第一步:** 修改系统配置

设置 deferred_segment_creation 参数

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

方法 1: 批量处理空表

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

**方法 2:** insert 一行，再 rollback 就产生 segment 了

该方法是在在空表中插入数据，再删除，则产生 segment。导出时则可导出空表。

参考链接: [Oracle 导出空表](https://www.cnblogs.com/ningvsban/p/3603678.html)

### Oracle 数据导入导出

Oracle 导入导出命令

```bash
# 导出数据
exp fdm/qwe1234@192.168.100.165:1521/newfdm file=20190514_newfdm.db owner=fdm
# 导入前需要删除原有数据库所有表+序列
imp fdm/qwe123 file=/home/oracle/20190514_newfdm.db fromuser=fdm touser=fdm DESTROY=Y
```

**导出日志查看**.配置 <导出空表数据> 后即可导出空表 xxx 0 行

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

### Oracle 密码到期修改

由于 Oracle 默认用户密码创建策略为 180 天，180 天用户密码失效，所以需要重新修改密码。
解决方法：
修改默认密码创建策略至无限期，重新设置用户密码

```sql
解决步骤:
-- 步骤1:查看当前open用户,即无限期用户 [非必需步骤]
select username,account_status,expiry_date,profile from dba_users;

-- 步骤2:查看目前的密码过期策略
SQL>  select * from dba_profiles s where s.profile='DEFAULT' and resource_name='PASSWORD_LIFE_TIME';
PROFILE                RESOURCE_NAME            RESOURCE
------------------------------ -------------------------------- --------
LIMIT
----------------------------------------
DEFAULT                PASSWORD_LIFE_TIME        PASSWORD
180

-- 步骤3:修改密码过期策略
alter profile default limit password_life_time unlimited;
# 重新查看策略，发现已经修改成功
SQL> select * from dba_profiles s where s.profile='DEFAULT' and resource_name='PASSWORD_LIFE_TIME';

PROFILE                RESOURCE_NAME            RESOURCE
------------------------------ -------------------------------- --------
LIMIT
----------------------------------------
DEFAULT                PASSWORD_LIFE_TIME        PASSWORD
UNLIMITED

-- 步骤4: 退出当前 sqlplus,重进sqlplus
$sqlplus / as sysdba

-- 步骤5: 重进后更新密码
过期的账户，重置密码后期不会再过期
alter user <用户名称> identified by <原来的密码>   ----不用换新密码
```

参考链接: [https://www.cnblogs.com/xiaochina/p/6892569.html](https://www.cnblogs.com/xiaochina/p/6892569.html)

### 修改数据库进程数为 500

项目需要，避免 oracle 数据库进程数不足，导致程序运行失败

```sql
su - oracle
$sqlplus / as sysdba
-- 更新系统参数
alter system set processes=500 scope=spfile;
-- 需要重启数据库
shutdown immediate;
startup;
-- 查看总进程数
show parameter processes;
--当前的连接数
select count(1) from v$process;
```

### Oracle 配置上下左右退格键

Linux 下 Oracle 的 sqlplus 中上下左右退格键无法使用

![20200409135421](https://raw.githubusercontent.com/fansichao/images/master/markdown/20200409135421.png)

```bash
# root用户
# 安装rlwrap
su - root
rpm -ivh /data/software/Oracle/rlwrap-0.42-1.el6.x86_64.rpm

# oracle用户
su – oracle
# 修改 .bash_profile
vi .bash_profile
# 添加2行
alias sqlplus='rlwrap sqlplus'
alias rman='rlwrap rman'
# 验证修改结果
sqlplus / as sysdba
其中上下左右退格键正常使用
```

### Oracle 显示乱码

```bash
主要方法1：(如果此方法无效，再尝试下一方法)
数据库显示正常，需要三者统一，客户端编码、数据库编码、系统编码。
oracle用户
#### 查看客户端编码、数据库编码、系统编码
# 查看系统编码
locale
# 进入数据库
sqlplus / as sysdba
startup;
# 查看oracle数据库的编码
select * from nls_database_parameters where parameter ='NLS_CHARACTERSET';
# 查看oracle客户端编码
select * from nls_instance_parameters where parameter='NLS_LANGUAGE';

#### 修改编码
# Linux系统默认 utf-8，将数据库和客户端也修改为utf-8的编码
1.首先以sysdba的身份登录上去 sqlplus / as sysdba
2.关闭数据库shutdown immediate;
3.以mount打来数据库，startup mount
4.设置session
SQL>ALTER SYSTEM ENABLE RESTRICTED SESSION;
SQL> ALTER SYSTEM SET JOB_QUEUE_PROCESSES=0;
SQL> ALTER SYSTEM SET AQ_TM_PROCESSES=0;
5.启动数据库
alter database open;

6.修改字符集
ALTER DATABASE CHARACTER SET AL32UTF8;
这会可能会报错，提示我们的字符集：新字符集必须为旧字符集的超集，这时我们可以跳过超集的检查做更改：
ALTER DATABASE character set INTERNAL_USE AL32UTF8;

这条语句就可以了，TERNAL_USE提供的帮助就会使oracle绕过了子集与超集的验证，这条语句和上面的语句内部操作时完全相同的。
7.关闭，重新启动
SQL>shutdown immediate;
SQL> startup
当上述修改无报错，但是依然乱码时，
	发现客户端编码、数据库编码、系统编码三者不一致，客户端编码为简体中文，其他为utf-8，故修改客户端编码(其他类同，也可以三者直接配置在.bash_profile)
# oracle用户
su - oracle
# 关闭数据库
sqlplus / as sysdba
shutdown immediate;
# 编辑文件
vi ~/.bash_profile
# 增加一行
export NLS_LANG=american_america.al32utf8
# 启动数据库
sqlplus / as sysdba
shartup;

```

## 常用 Oracle 命令

```sql
# 进入命令交互页面
sqlplus / as sysdba


# 启停监听服务
lsnrctl stop
lsnrctl start
# 数据库连接
fdm/qwe123@192.168.1.1:1521/fdm
数据库用户/数据库密码@IP地址:端口/SID
# 数据库启停
startup
shutdown immediate


```

## 附件
