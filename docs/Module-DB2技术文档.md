# DB2技术文档

tags: DB2 2017年 数据库

## 安装部署

参考链接： [Linux下DB2数据库安装过程详解](http://www.codeceo.com/article/linux-db2-setup.html)

```bash
数据库配置
创建数据库

db2 create database 数据库名develop PAGESIZE 32 K #建立数据库develop，32K,默认建立16k，32k空间大
关闭防火墙

systemctl stop firewalld.service # 关闭 firewall  centos7的防火墙
systemctl stop iptables.service  # 关闭 iptables  centos6的防火墙
systemctl disable firewalld.service # 禁止firewall开机启动
systemctl disable iptables.service  # 禁止iptables 开机启动
```

## 功能模块

### 安装Python-DB2驱动

若无DB2驱动，连接报错如下

```bash
>>> import ibm_db
>>> connStr = "DATABASE=XCDW;HOSTNAME=192.168.100.167;PORT=50000;PROTOCOL=TCPIP;UID=xcdw;PWD=qwe123;"
>>> conn = ibm_db.connect(connStr, "", "")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
SystemError: error return without exception set
```

解决方案

```bash
步骤1:
# 数据库用户
[db2inst1@localhost ~]$ ll
total 8
drwxrwxr-x.  3 db2inst1 db2iadm1 4096 Nov 13 19:10 db2inst1
drwxrwsr-t. 25 db2inst1 db2iadm1 4096 Nov 13 19:10 sqllib
[db2inst1@localhost ~]$ pwd
/home/db2inst1
[db2inst1@localhost ~]$


# 将如下加入到数据库用户 .bash_profile 中. db2inst1为用户名称
export PATH=$PATH:.$HOME/bin:/home/db2inst1/sqllib/bin
if [ -f /home/db2inst1/sqllib/db2profile ]
then
source /home/db2inst1/sqllib/db2profile
fi

步骤2
# 解压得到 clidriver
tar -zxvf linuxx64_odbc_cli.tar.gz
# 将 clidriver 复制到 ibm-db 下
cp -r clidriver/ xcdw1_env/lib/python2.7/site-packages/ibm_db-2.0.7.dist-info/.
```
