# Hbase技术文档.md

tags: 大数据 底层存储 分布式 Hbase 2019年

## 安装部署

环境依赖说明: TODO 未完全

- 依赖于Hadoop

环境说明：

- Hbase==2.2.1

### 安装Hbase

#### 下载解压

Hbase下载链接(版本更新太快,存在链接失效的可能性): [https://mirrors.cnnic.cn/apache/hbase/2.2.1/hbase-2.2.1-bin.tar.gz](https://mirrors.cnnic.cn/apache/hbase/2.2.1/hbase-2.2.1-bin.tar.gz)

```bash
wget https://mirrors.cnnic.cn/apache/hbase/hbase-1.2.9/hbase-1.2.9-bin.tar.gz -P /software/Spark/spark_packages/. 
(env) [scfan@WOM software]$ tar -zxvf /software/Spark/spark_packages/hbase-1.2.9-bin.tar.gz -C /software/Spark/.
(env) [scfan@WOM software]$ mv /software/Spark/hbase-1.2.9/ /software/Spark/hbase
```

#### 配置环境变量

修改文件```sudo vim /etc/profile```加入下面两行

```base
# Hbase
export HBASE_HOME=/software/Spark/hbase
export PATH=$PATH:$HBASE_HOME/bin
```

#### 修改配置文件

vi /software/Spark/hbase/conf/hbase-env.sh
修改hbase-env.sh，加入下面三行（注意java和hadhoop路径）

```conf
# java Home路径
export JAVA_HOME=/usr/java/jdk1.8.0_171
# Hadoop Home路径
export HBASE_CLASSPATH=/software/Spark/spark/conf
export HBASE_MANAGES_ZK=true
```

vi /software/Spark/hbase/conf/hbase-site.xml
修改hbase-site.xml(数据路径可自行修改)

```xml
<configuration>
  <property>
    <name>hbase.cluster.distributed</name>
    <value>true</value>
  </property>
  <property>
    <name>hbase.rootdir</name>
    <value>file:/software/Spark/data/hbase/hbase_data</value>
  </property>
  <property>
    <name>hbase.zookeeper.property.dataDir</name>
    <value>/software/Spark/data/hbase/zookeeper_data</value>
  </property>
</configuration>
```

创建目录
cd /software/Spark/data/ && mkdir hbase/hbase_data hbase/zookeeper_data

#### 启动和验证

启动服务

```bash
(env) [scfan@WOM hbase]$ source /etc/profile
start-hbase.sh
```

验证

```bash
# 输入 Hbase Shell
[root@c7c57188b482 software]# hbase shell
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/root/packages/hugegraph/hadoop-2.7.7/share/hadoop/common/lib/slf4j-log4j12-1.7.10.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/root/packages/hugegraph/hbase-2.2.1/lib/client-facing-thirdparty/slf4j-log4j12-1.7.25.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.slf4j.impl.Log4jLoggerFactory]
HBase Shell
Use "help" to get list of supported commands.
Use "exit" to quit this interactive shell.
For Reference, please visit: http://hbase.apache.org/2.0/book.html#shell
Version 2.2.1, rf93aaf770cce81caacbf22174dfee2860dbb4810, 2019年 09月 10日 星期二 14:28:27 CST
Took 0.0023 seconds
# 输入 List 查看表名称
hbase(main):001:0> list
TABLE
0 row(s)
Took 0.4448 seconds
=> []
```

## 附件

### 参考链接

- 推荐阅读
  - [hbase原理](https://blog.csdn.net/fanren224/article/details/84594842)
- 其他
