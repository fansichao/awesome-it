---
title: Linux-Spark使用文档.md
tags: 2019年 08月 11号
notebook: 00技术笔记
---

# 1. Spark简介

## 1.1. Spark说明

 Apache Spark是一个围绕速度、易用性和复杂分析构建的大数据处理框架，最初在2009年由加州大学伯克利分校的AMPLab开发，并于2010年成为Apache的开源项目之一，与Hadoop和Storm等其他大数据和MapReduce技术相比，Spark有如下优势：

- Spark提供了一个全面、统一的框架用于管理各种有着不同性质（文本数据、图表数据等）的数据集和数据源（批量数据或实时的流数据）的大数据处理的需求
- 官方资料介绍Spark可以将Hadoop集群中的应用在内存中的运行速度提升100倍，甚至能够将应用在磁盘上的运行速度提升10倍

[Spark官网](http://spark.apache.org/)

## 1.2. Spark框架

**spark运行流程图**

![Spark运行流程图](https://images2015.cnblogs.com/blog/1004194/201608/1004194-20160830094200918-1846127221.png)

**Spark架构**

![Spark架构](https://images2015.cnblogs.com/blog/1004194/201608/1004194-20160829161404996-1972748563.png)

**详见参考链接**：https://blog.csdn.net/swing2008/article/details/60869183


## 1.3. Hadoop说明

Hadoop是一个由Apache基金会所开发的**分布式系统基础架构**。

Hadoop实现了一个分布式文件系统（Hadoop Distributed File System），简称HDFS。

Hadoop的框架最核心的设计就是：HDFS和MapReduce。HDFS为海量的数据提供了存储，而MapReduce则为海量的数据提供了计算

[Hadoop百度百科](https://baike.baidu.com/item/Hadoop/3526507?fr=aladdin)

**Hadoop优点:**
- 高可靠性。Hadoop按位存储和处理数据的能力值得人们信赖。
- 高扩展性。Hadoop是在可用的计算机集簇间分配数据并完成计算任务的，这些集簇可以方便地扩展到数以千计的节点中。
- 高效性。Hadoop能够在节点之间动态地移动数据，并保证各个节点的动态平衡，因此处理速度非常快。
- 高容错性。Hadoop能够自动保存数据的多个副本，并且能够自动将失败的任务重新分配。
- 低成本。与一体机、商用数据仓库以及QlikView、Yonghong Z-Suite等数据集市相比，hadoop是开源的，项目的软件成本因此会大大降低。

**Hadoop框架**
Hadoop有两个核心模块，**分布式存储模块HDFS**和**分布式计算模块Mapreduce**.

## 1.4. Yarn框架说明

由于原有框架JobTracker/TaskTracker需要大规模的调整来修复它在可扩展性，内存消耗，线程模型，可靠性和性能上的缺陷,所以推出了Yarn框架。

- 参考链接：https://www.ibm.com/developerworks/cn/opensource/os-cn-hadoop-yarn/

Yarn框架核心在于将资源管理和任务调度/监控拆分。
- 资源管理器: 全局管理所有应用程序计算资源的分配
- 每一个应用的 ApplicationMaster 负责相应的调度和协调
- ResourceManager 和每一台机器的节点管理服务器能够管理用户在那台机器上的进程并能对计算进行组织

![Hadoop新MapReduce框架Yarn](https://www.ibm.com/developerworks/cn/opensource/os-cn-hadoop-yarn/images/image002.jpg)

- ResourceManager :中心服务，调度和启动Job中的ApplicationMaster,并监控ApplicationMaster存在情况
- NodeManager : 负责 Container 状态的维护，并向 ResourceManager 返回日志
- ApplicationMaster :负责一个 Job 生命周期内的所有工作

# 2. Spark环境部署

**不同部署模式**
- Standalone模式：独立部署模式
- Apache Mesos
- Hadoop YARN
- Kubernetes

版本说明:
- Spark 2.4.0
- Scala 2.12
- Spark和Hadoop版本必须相互配合

## 2.1. 安装Scala

Spark支持Scala、Java和Python等语言，不过Spark是采用Scala语言开发，所以必须先安装Scala.

**步骤1：下载**
Scala-2.12.7下载地址
```bash
wget https://downloads.lightbend.com/scala/2.12.7/scala-2.12.7.tgz
```

**步骤2：解压**

```bash
# 创建目录
tar -zxvf scala-2.12.7.tgz
sudo mv scala-2.12.7 /usr/local/scala
sudo chown scfan:scfan -R /usr/local/scala
```

**步骤3：配置环境变量**

```python
# 打开文件
sudo vim /etc/profile
# 添加内容如下
export SCALA_HOME=/usr/local/scala
export PATH=$SCALA_HOME/bin:$PATH
```

**步骤4：生效与验证**

```bash
(env) [scfan@WOM ~]$ source /etc/profile
(env) [scfan@WOM ~]$ scala
Welcome to Scala 2.12.7 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_171).
Type in expressions for evaluation. Or try :help.

scala>
```

## 2.2. 安装Spark

**步骤1：下载**

```bash
wget http://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz
```

**步骤2：解压**

```bash
tar -zxvf spark-2.4.0-bin-hadoop2.7.tgz
sudo mv spark-2.4.0-bin-hadoop2.7 /usr/local/spark
sudo chown -R scfan:scfan /usr/local/spark
```

**步骤3：配置环境变量**
```python
# 打开文件
sudo vim /etc/profile
# 添加内容如下
# Spark path
export SPARK_HOME=/usr/local/spark
export PATH=$SPARK_HOME/bin:$PATH
```

**步骤4：生效与验证**
```bash
(env) [scfan@WOM ~]$ source /etc/profile
(env) [scfan@WOM spark]$ source /etc/profile
(env) [scfan@WOM spark]$ pyspark
Python 2.7.11 (default, Apr 10 2018, 16:42:22) 
[GCC 4.4.7 20120313 (Red Hat 4.4.7-18)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
2018-12-06 15:37:54 WARN  NativeCodeLoader:62 - Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 2.4.0
      /_/

Using Python version 2.7.11 (default, Apr 10 2018 16:42:22)
SparkSession available as 'spark'.
>>> 
```

**步骤5：启动Spark**
```bash
(env) [scfan@WOM spark]$ ./bin/spark-shell --master local[2]
2018-12-06 15:49:10 WARN  NativeCodeLoader:62 - Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Spark context Web UI available at http://WOM:4040
Spark context available as 'sc' (master = local[2], app id = local-1544082590634).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 2.4.0
      /_/
         
Using Scala version 2.11.12 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_171)
Type in expressions to have them evaluated.
Type :help for more information.

scala> 
```
**页面UI:**  http://WOM:4040


## 2.3. 安装Hadoop(本地单节点)

**安装步骤**
- 安装JDK 1.8+
- 设置SSH无密钥登录
- 下载安装Hadoop
- 设置环境变量
- 设置Hadoop配置文件
- 创建并格式化HDFS目录
- 启动Hadoop
- 打开Web页面

### 2.3.1. 下载安装Hadoop

官网：https://hadoop.apache.org/releases.html
```bash
# 下载
wget http://mirror.bit.edu.cn/apache/hadoop/common/hadoop-2.7.7/hadoop-2.7.7.tar.gz
# 解压
tar -zxvf hadoop-2.7.7.tar.gz
# 迁移
sudo mv hadoop-2.7.7 /usr/local/hadoop
# 授权
sudo chown scfan:scfan -R usr/local/hadoop
```

### 2.3.2. 设置环境变量
文件  /etc/profile
```python
## hadoop home
export HADOOP_HOME=/usr/local/hadoop
# hadoop path
export PATH=$PATH:$HADOOP_HOME/bin
export PATH=$PATH:$HADOOP_HOME/sbin
# hadoop else env
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_PREFIX=$HADOOP_HOME
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
# hadoop lib 
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib"
export JAVA_LIBRARY_PATH=$HADOOP_HOME/lib/native:$JAVA_LIBRARY_PATH
```
### 2.3.3. 修改Hadoop配置文件

**配置文件：/usr/local/hadoop/etc/hadoop/hadoop-env.sh**
```python
export JAVA_HOME=/usr/java/jdk1.8.0_171
```
**HDFS默认名称 /usr/local/hadoop/etc/hadoop/core-site.xml**
```xml
<configuration>
    <property>
        <name>fs.default.name</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```
**MapReduce配置 /usr/local/hadoop/etc/hadoop/yarn-site.xml**
```xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
    </property>
    <!-- 后续如果 spark-yarn 部署报错，需要解开此处
    <property>
        <name>yarn.resourcemanager.address</name>
        <value>master:8032</value>
    </property>
    <property>
      <name>yarn.resourcemanager.scheduler.address</name>
      <value>master:8030</value>
    </property>
    <property>
      <name>yarn.resourcemanager.resource-tracker.address</name>
      <value>master:8031</value>
    </property>
    -->
</configuration>
```
**Job配置 /usr/local/hadoop/etc/hadoop/mapred-site.xml**
```xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <vaule>yarn</vaule>
    </property>
</configuration>
```
**HDFS分布式文件系统 /usr/local/hadoop/etc/hadoop/hdfs-site.xml**
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <vlaue>3</vlaue>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <vlaue>file:/usr/local/hadoop/hadoop_data/hdfs/namenode</vlaue>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <vlaue>file:/usr/local/hadoop/hadoop_data/hdfs/datanode</vlaue>
    </property>
</configuration>
```
### 2.3.4. 格式化目录
```bash
# 创建存储目录
mkdir -p /usr/local/hadoop/hadoop_data/hdfs/namenode/ 
mkdir -p /usr/local/hadoop/hadoop_data/hdfs/datanode/ 
# 进行格式化(如果报错，删除namenode下文件夹current)
hadoop namenode -format # 会删除HDFS数据
```
### 2.3.5. 查看页面
```bash
# 启动HDFS
start-dfs.sh
# 启动Yarn
start-yarn.sh
```
Hadoop界面： http://localhost:8088
HDFS界面： http://localhost:50070


## 2.4. 部署Spark Standalone Mode

参考链接：
- http://spark.apache.org/docs/latest/spark-standalone.html

本地单机模式
```bash
# 启动主节点 默认端口8080
./sbin/start-master.sh -h localhost --webui-port 8080
# 启动子节点
./sbin/start-slave.sh <master-spark-URL>
例如: <master-spark-URL> 可以在页面localhost:8080上面查看
./sbin/start-slave.sh spark://localhost:7077
```

## 2.5. 部署Spark Mesos模式

参考链接： http://spark.apache.org/docs/latest/running-on-mesos.html

**Mesos安装**
参考链接：https://open.mesosphere.com/downloads/mesos/
```bash
# 下载系统对应 rpm 包
wget http://repos.mesosphere.com/el/6/x86_64/RPMS/mesos-1.7.0-2.0.1.el6.x86_64.rpm
rpm -ivh mesos-1.7.0-2.0.1.el6.x86_64.rpm
```

**前端WebUI启动命令**
```bash
mesos master --ip=localhost  --work_dir=/var/lib/mesos
```

**前端WebUI地址:**
http://localhost:5050/#/

## 2.6. 部署Spark Yarn
参考链接： http://spark.apache.org/docs/latest/running-on-yarn.html
```bash
命令参数:
./bin/spark-submit --class path.to.your.Class --master yarn --deploy-mode cluster [options] <app jar> [app options]
命令样例:
$ ./bin/spark-submit --class org.apache.spark.examples.SparkPi \
    --master yarn \
    --deploy-mode cluster \
    --driver-memory 4g \
    --executor-memory 2g \
    --executor-cores 1 \
    --queue thequeue \
    examples/jars/spark-examples*.jar \
    10
```

### 2.6.1. 问题记录
**问题说明**
```
# 执行命令
$ ./bin/spark-submit --class org.apache.spark.examples.SparkPi \
    --master yarn \
    --deploy-mode cluster \
    --driver-memory 4g \
    --executor-memory 2g \
    --executor-cores 1 \
    --queue thequeue \
    examples/jars/spark-examples*.jar \
    10
# 报错如下
2018-12-07 16:19:07 INFO  Client:871 - Retrying connect to server: 0.0.0.0/0.0.0.0:8032. Already tried 0 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)
```
**问题解决**
yarn-site.xml增加如下内容
```
<property>
    <name>yarn.resourcemanager.address</name>
    <value>master:8032</value>
  </property>
  <property>
    <name>yarn.resourcemanager.scheduler.address</name>
    <value>master:8030</value>
  </property>
  <property>
    <name>yarn.resourcemanager.resource-tracker.address</name>
    <value>master:8031</value>
  </property>
```
## 2.7. 部署Spark Kubernetes

**Spark Kubernetes:** https//spark.apache.org/docs/latest/running-on-kubernetes.html 

**kubernetes官网：**https://kubernetes.io/

TODO 

# 3. Spark数据统计

## 3.1. SparkRDD使用

RDD - 弹性分布式数据集

RDD是可以并行操作的容错的容错集合。创建RDD有两种方法：并行化 驱动程序中的现有集合，或引用外部存储系统中的数据集

官网RDD参考链接： 
http://spark.apache.org/docs/latest/rdd-programming-guide.html#resilient-distributed-datasets-rdds

**Spark启动**
bin/pyspark

**Spark初始化**
- 创建SparkContext对象，告知Spark如何访问集群。
- appName参数是应用程序在群集UI上显示的名称
- master是URL
```python
>>> from pyspark import SparkContext, SparkConf
>>> appName="fdm"
>>> master="mesos://localhost:5050"
>>> conf = SparkConf().setAppName(appName).setMaster(master)
>>> sc = SparkContext(conf=conf)
>>> sc
<SparkContext master=local[*] appName=PySparkShell>
```
**并行化集合**
```python
>>> data = [1, 2, 3, 4, 5]
>>> distData = sc.parallelize(data)
>>> print distData
ParallelCollectionRDD[0] at parallelize at PythonRDD.scala:195
```
**外部数据集**
支持导入本地数据集、HDFS://xxxxxx等
```python
>>> distFile = sc.textFile("data.txt")
>>> distFile
data.txt MapPartitionsRDD[2] at textFile at NativeMethodAccessorImpl.java:0
```
可写类型：
- int 
- float
- double
- bool
- byte
- null
- dict 
**保存和加载SequenceFiles**
```python
>>> rdd = sc.parallelize(range(1, 4)).map(lambda x: (x, "a" * x))
>>> rdd.saveAsSequenceFile("path/to/file")
>>> sorted(sc.sequenceFile("path/to/file").collect())                          
[(1, u'a'), (2, u'aa'), (3, u'aaa')]
```



## 3.2. SparkDataFrame使用

官网DataFrame参考链接：
http://spark.apache.org/docs/latest/sql-programming-guide.html

**初始化Spark Session**
```python
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
```
**创建DataFrame**
```python
# spark is an existing SparkSession
df = spark.read.json("examples/src/main/resources/people.json")
# Displays the content of the DataFrame to stdout
df.show()
# +----+-------+
# | age|   name|
# +----+-------+
# |null|Michael|
# |  30|   Andy|
# |  19| Justin|
# +----+-------+
```

## 3.3. SparkSQL使用

官网参考链接：
http://spark.apache.org/docs/latest/sql-distributed-sql-engine.html#running-the-thrift-jdbcodbc-server

**启动Thrift JDBC / ODBC服务器**
```bash
./sbin/start-thriftserver.sh
```
**访问前端UI**
```
http://localhost:4042/SQL/
```
**使用beeline来测试Thrift JDBC / ODBC服务器：**
```bash
./bin/beeline
beeline> !connect jdbc:hive2://localhost:10000
# 输入用户名和空白密码
```
启动spark-sql
```
./bin/spark-sql
```


 
# Spark问题整理

## Service 'SparkUI' could not bind on port 4040. Attempting port 4041.

问题：运行Spark脚本报错

```python

self.spark = SparkSession.builder.master(self.MASTER).appName(self.APPNAME).getOrCreate()
```

原因：
由于启动一个Spark context 时，SparkUI 默认会使用 4040 端口，当 4040 端口被占用时，则尝试使用另外一个端口

解决步骤：
关闭 Spark-Shell 即可

错误日志:

```bash

2018-12-27 09:38:59 WARN  Utils:66 - Service 'SparkUI' could not bind on port 4040. Attempting port 4041.
I1227 09:39:02.612689 26652 sched.cpp:232] Version: 1.7.0
I1227 09:39:02.619974 26650 sched.cpp:336] New master detected at master@192.168.172.70:5050
I1227 09:39:02.620997 26650 sched.cpp:356] No credentials provided. Attempting to register without authentication
```



# Spark操作细节




# Mesos使用

## Messos安装&配置

[mesos官方部署文档](http://mesos.apache.org/documentation/latest/building/)

## Mesos启动 & 关闭

```bash
cd /usr/local/spark
./bin/spark-shell --master mesos://192.168.172.70:5050

/etc/mesos-master
/etc/mesos-slave

# 关闭 mesos-master
[root@WOM mesos-master]# netstat -lntp | grep 5050
[root@WOM mesos-master]# kill -9 XXXX
# 启动 mesoso-master
mesos-master --work_dir=/usr/local/mesos/master_data --log_dir=/usr/local/mesos/master_logs --no-hostname_lookup --ip=192.168.172.70 --cluster=wom
# 启动master-salve
mesos-slave --work_dir=/usr/local/mesos/salves_data --log_dir=/usr/local/mesos/salves_logs --master=192.168.172.70:5050 --no-hostname_lookup --ip=192.168.172.70 --port=5052
# 启动 Spark 
./sbin/start-master.sh -h localhost --webui-port 8080
(env) [scfan@WOM spark]$ bin/spark-shell --master mesos://192.168.172.70:5050 --total-executor-cores 1 --driver-memory 512M --executor-memory 512M
## 2.4. 部署Spark Standalone Mode
参考链接：
- http://spark.apache.org/docs/latest/spark-standalone.html

本地单机模式
# 启动主节点 默认端口8080
./sbin/start-master.sh -h localhost --webui-port 8080
# 启动子节点
./sbin/start-slave.sh <master-spark-URL>
例如: <master-spark-URL> 可以在页面localhost:8080上面查看
./sbin/start-slave.sh spark://localhost:7077

```
 





## 删除mesos工作目录

```bash

如果我需要一个新的mesos集群，我需要master的干净工作目录。但问题不在于10.142.55.202约瑟夫吴说。我清除了所有的word_dir，并摆脱了这个问题。

如何清理工作目录：

找到mesos-master工作目录

$ cat /etc/mesos-master/work_dir
/var/lib/mesos
去掉它

$ rm -rf /var/lib/mesos
```

## Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered and have sufficient resources

当前的集群的可用资源不能满足应用程序所请求的资源

资源分2类： cores 和 ram
Core代表对执行可用的executor slots
Ram代表每个Worker上被需要的空闲内存来运行你的Application。
解决方法：
应用不要请求多余空闲可用资源的
关闭掉已经执行结束的Application

解决方法：
1. 执行参数修改内存大小
2. 释放内存，增加内存大小

export SPARK_WORKER_MEMORY=512M
export SPARK_DAEMON_MEMORY=256M


这些--executor-memory、--driver-memory你是否能先指定得更小些（比如50M、100M）

1.因为提交任务的节点不能和worker节点交互，因为提交完任务后提交任务节点上会起一个进程，展示任务进度，大多端口为4044，工作节点需要反馈进度给该该端口，所以如果主机名或者IP在hosts中配置不正确。所以检查下主机名和ip是否配置正确。

2.也有可能是内存不足造成的。内存设置可以根据情况调整下。另外，也检查下web UI看看，确保worker节点处于alive状态。

