# Docker 功能模块

tags: `docker` `功能模块` `2020年` `04月`

`Docker功能模块`:

- Docker-Oracle 安装数据库
- Docker-network 配置网络
- Docker-Configs 参数配置

TODO Dockerfile

## Docker-Oracle

使用 Docker 安装 Oracle 11g/12g

### 方案 1: Oracle11g

说明:

- Docker 源: jaspeen/oracle-11g
- 需要自行安装 Oracle 数据库, 此 Docker 源只有环境

**安装 Oracle 数据库:**

```bash
# 步骤1: 拉取镜像
docker pull docker.io/jaspeen/oracle-11g
# 步骤2：准备安装包 PS: 由于  jaspeen/oracle-11g 仅有环境, 所以需要自行安装数据库
# 将其解压到/data_storage/oracle_install目录 得到 /data_storage/oracle_install/databases
unzip linux.x64_11gR2_database_1of2.zip
unzip linux.x64_11gR2_database_2of2.zip

# 步骤3: 运行镜像
docker run -d -p 2222:22 -p 9090:8080 -p 15210:1521 -v /data_storage/oracle:/u01/app/oracle/ -v /data_storage/oracle_install:/install --name fdm_oracle docker.io/jaspeen/oracle-11g:latest

# 步骤4：查看镜像日志
docker logs -f fdm_oracle
# 安装耗时很久... 可以通过查看日志或者ctop查看容器CPU消耗来判断是否安装完成
```

**配置 Oracle:**

```sql
# 连接到容器
docker exec -it oracle11g /bin/bash
切换到oracle用户，然后连接到sql控制台
[root@7f53f07c93e5 /]# su - oracle
Last login: Wed Apr 17 08:29:31 UTC 2019

[oracle@7f53f07c93e5 ~]$ sqlplus / as sysdba
SQL*Plus: Release 11.2.0.1.0 Production on Wed Apr 17 09:29:49 2019
Copyright (c) 1982, 2009, Oracle.  All rights reserved.

Connected to:
Oracle Database 11g Enterprise Edition Release 11.2.0.1.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
-- 解锁账户
SQL> alter user scott account unlock;
User altered.
SQL> commit;
Commit complete.
-- 连接到默认账户 scott 设置密码
SQL> conn scott/tiger
ERROR:
ORA-28001: the password has expired
Changing password for scott
New password:
Retype new password:
Password changed
Connected.
SQL>

-- 连接数据库
安装完成后，使用默认的sid为orcl，端口为1521，scott/tiger即可连接

用户名 scott
端口由于Docker run中做了映射 为15210
实例 orcl
```

参考链接: [Docker 安装 Oracle11g](https://blog.csdn.net/qq_39316391/article/details/100542751)

### 方案 2: 超简单安装 Oracle11g

```bash
前提最新版Docker安装好，配置阿里云镜像库
# 获取镜像
docker pull registry.cn-hangzhou.aliyuncs.com/qida/oracle-xe-11g

# 运行命令
docker run --name oracle11g -d -p 1521:1521 -v /docker/oracle/v/oradata/:/u01/app/oracle/oradata/oracle11g-data/ -e ORACLE_ALLOW_REMOTE=true --restart=always registry.cn-hangzhou.aliyuncs.com/qida/oracle-xe-11g

# 进入容器：
docker exec -it oracle11g bash

系统用户：root 密码：admin

切换用户：su oracle

进入SQL交互：sqlplus / as sysdba 到这里可以自己操作数据库了

数据库链接
hostname: localhost

port: 1521

sid: xe

username: system

password: oracle


# 创建数据库用户：
create user fdm identified by qwe123;

# 授权给用户：
GRANT CREATE USER,DROP USER,ALTER USER ,CREATE ANY VIEW ,DROP ANY VIEW,EXP_FULL_DATABASE,IMP_FULL_DATABASE,DBA,CONNECT,RESOURCE,CREATE SESSION TO 用户名fdm
```

## 附件

### 参考资源

- [Docker 安装 Oracle11g-超简单教程](https://www.jianshu.com/p/fc85bb7e2d90)
