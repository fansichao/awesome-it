# Hadoop技术文档.md

环境依赖:

当前环境:

- CentOS7.5

## 安装部署

整体安装过程

- 前置依赖 Java/SSH无密钥配置
- 环境变量配置
- 修改配置文件
- 创建格式化HDFS目录

安装在目录 **/software/Spark/hadoop** ,安装在其他目录，**配置等对应修改**

### 安装Java

Java一键安装脚本

```bash
# 全程 root 用户安装
install_path=/usr/java/
file_bash=/etc/profile
file_name=jdk-8u171-linux-x64.tar.gz

mkdir -p $install_path
tar -zxf $file_name -C $install_path

echo """
# jdk java
export JAVA_HOME=/usr/java/jdk1.8.0_171
export JRE_HOME=\$JAVA_HOME/jre
export CLASSPATH=.:\$JAVA_HOME/lib:\$JRE_HOME/lib
export PATH=\$JAVA_HOME/bin:\$PATH
""" >> $file_bash
source $file_bash
```

[安装包jdk-8u171-linux-x64.tar.gz下载](https://pan.baidu.com/s/1FppDy891WtsbplDTVPt3dw)

### 配置SSH无密钥登录

《参考SSH密钥配置文档》

Hadoop密钥配置较为特殊。如果Hadoop安装在非root用户。
例如。
sudo cat /home/scfan/.ssh/id_rsa.pub >> /home/scfan/.ssh/authorized_keys
sudo cat /root/.ssh/id_rsa.pub >> /home/scfan/.ssh/authorized_keys
sudo cat /home/scfan/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
sudo cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
需要将密钥加在自己用户和其他用户。
chmod 700 /home/scfan/.ssh/
chmod 600 /home/scfan/.ssh/authorized_keys
chmod 700 /root/.ssh/
chmod 600 /root/.ssh/authorized_keys

### 下载安装Hadoop

```bash
# 步骤1：下载hadoop
wget http://mirror.bit.edu.cn/apache/hadoop/common/hadoop-2.7.7/hadoop-2.7.7.tar.gz -P /software/Spark/spark_packages/.

# 步骤2：解压hadoop
tar -zxvf /software/Spark/spark_packages/hadoop-2.7.7.tar.gz  -C /software/Spark/.
mv /software/Spark/hadoop-2.7.7 /software/Spark/hadoop

# 步骤3：设置环境变量
sudo vim /etc/profile
增加如下几行
## hadoop home
export HADOOP_HOME=/software/Spark/hadoop  
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

# 重新加载 /etc/profile
source /etc/profile
```

### 设置Hadoop配置文件

切换到配置文件目录
cd /software/Spark/hadoop/etc/hadoop

#### 修改 hadoop_env.sh  

```bash
修改原文件中
export JAVA_HOME=${JAVA_HOME}
为
export JAVA_HOME=/usr/java/jdk1.8.0_171
```

#### 修改HDFS默认名称core-site.xml

```xml
<configuration>
    <property>
        <name>fs.default.name</name>
        <value>hdfs://192.168.172.70:9000</value>
    </property>
</configuration>
```

#### 配置MapReduce  yarn-site.xml

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
    <property>
        <name>yarn.resourcemanager.address</name>
        <value>192.168.172.70:8032</value>
    </property>
    <property>
        <name>yarn.resourcemanager.scheduler.address</name>
        <value>192.168.172.70:8030</value>
    </property>
    <property>
        <name>yarn.resourcemanager.resource-tracker.address</name>
        <value>192.168.172.70:8031</value>
    </property>
    -->
</configuration>
```

#### 配置Job mapred-site.xml

拷贝文件
cp mapred-site.xml.template  mapred-site.xml

添加如下内容

```xml

<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <vaule>yarn</vaule>
    </property>
</configuration>
```

#### HDFS分布式文件系统 hdfs-site.xml

```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <vlaue>3</vlaue>
    </property>
    <property>
        <name>dfs.permissions</name>
        <value>false</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <vlaue>file:/software/Spark/data/hadoop_data/hdfs/namenode</vlaue>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <vlaue>file:/software/Spark/data/hadoop_data/hdfs/datanode</vlaue>
    </property>
</configuration>
```

### 创建并格式化HDFS目录

```bash
# 创建目录
mkdir -p /software/Spark/data/hadoop_data/hdfs/namenode
mkdir -p /software/Spark/data/hadoop_data/hdfs/datanode
# 格式化目录
# 进行格式化(如果报错，需要删除namenode下文件夹current)
hadoop namenode -format # 会删除HDFS数据
```

### 启动Hadoop

**启动HDFS** start-dfs.sh
**启动Yarn** start-yarn.sh
**启动所有(含 dfs和yarn)** start-all.sh

### 检查启动项

至少有如下启动项

```bash
[root@hbase hadoop]#  jps | grep -E 'ResourceManager|DataNode|NodeManager|SecondaryNameNode|NameNode'
26530 DataNode
26957 NodeManager
26862 ResourceManager
26429 NameNode
26717 SecondaryNameNode
```

问题
存在未启动情况，查看start-all.sh启动日志。或者在对应spark、hadoop日志目录下查看信息。

若存在datanode未启动（目录视情况而变动）(一般由于多次format导致的name和data的id不匹配)

```bash
(env) [scfan@WOM dfs]$ rm /tmp/hadoop-scfan/dfs/name/*
(env) [scfan@WOM dfs]$ rm /tmp/hadoop-scfan/dfs/data/*
(env) [scfan@WOM dfs]$ hadoop namenode -format
(env) [scfan@WOM dfs]$ stop-all.sh
(env) [scfan@WOM dfs]$ start-all.sh
```

### 查看页面

Hadoop界面： [http://192.168.172.70:8088](http://192.168.172.70:8088 )
HDFS界面： [http://192.168.172.70:50070](http://192.168.172.70:50070)


安装日志 仅供参考

```bash
[root@c7c57188b482 hadoop]# hadoop namenode -format
DEPRECATED: Use of this script to execute hdfs command is deprecated.
Instead use the hdfs command for it.

19/10/15 01:12:09 INFO namenode.NameNode: STARTUP_MSG: 
/************************************************************
STARTUP_MSG: Starting NameNode
STARTUP_MSG:   host = c7c57188b482/172.18.0.71
STARTUP_MSG:   args = [-format]
STARTUP_MSG:   version = 2.7.7
STARTUP_MSG:   classpath = /root/software/hadoop/etc/hadoop:/root/software/hadoop/share/hadoop/common/lib/jackson-xc-1.9.13.jar:/root/software/hadoop/share/hadoop/common/lib/api-asn1-api-1.0.0-M20.jar:/root/software/hadoop/share/hadoop/common/lib/hadoop-auth-2.7.7.jar:/root/software/hadoop/share/hadoop/common/lib/paranamer-2.3.jar:/root/software/hadoop/share/hadoop/common/lib/commons-configuration-1.6.jar:/root/software/hadoop/share/hadoop/common/lib/log4j-1.2.17.jar:/root/software/hadoop/share/hadoop/common/lib/jersey-core-1.9.jar:/root/software/hadoop/share/hadoop/common/lib/gson-2.2.4.jar:/root/software/hadoop/share/hadoop/common/lib/jackson-mapper-asl-1.9.13.jar:/root/software/hadoop/share/hadoop/common/lib/commons-httpclient-3.1.jar:/root/software/hadoop/share/hadoop/common/lib/apacheds-i18n-2.0.0-M15.jar:/root/software/hadoop/share/hadoop/common/lib/curator-client-2.7.1.jar:/root/software/hadoop/share/hadoop/common/lib/hadoop-annotations-2.7.7.jar:/root/software/hadoop/share/hadoop/common/lib/jets3t-0.9.0.jar:/root/software/hadoop/share/hadoop/common/lib/hamcrest-core-1.3.jar:/root/software/hadoop/share/hadoop/common/lib/curator-recipes-2.7.1.jar:/root/software/hadoop/share/hadoop/common/lib/junit-4.11.jar:/root/software/hadoop/share/hadoop/common/lib/jersey-server-1.9.jar:/root/software/hadoop/share/hadoop/common/lib/protobuf-java-2.5.0.jar:/root/software/hadoop/share/hadoop/common/lib/jackson-core-asl-1.9.13.jar:/root/software/hadoop/share/hadoop/common/lib/activation-1.1.jar:/root/software/hadoop/share/hadoop/common/lib/commons-collections-3.2.2.jar:/root/software/hadoop/share/hadoop/common/lib/commons-beanutils-core-1.8.0.jar:/root/software/hadoop/share/hadoop/common/lib/commons-digester-1.8.jar:/root/software/hadoop/share/hadoop/common/lib/httpcore-4.2.5.jar:/root/software/hadoop/share/hadoop/common/lib/xz-1.0.jar:/root/software/hadoop/share/hadoop/common/lib/asm-3.2.jar:/root/software/hadoop/share/hadoop/common/lib/guava-11.0.2.jar:/root/software/hadoop/share/hadoop/common/lib/commons-beanutils-1.7.0.jar:/root/software/hadoop/share/hadoop/common/lib/xmlenc-0.52.jar:/root/software/hadoop/share/hadoop/common/lib/jackson-jaxrs-1.9.13.jar:/root/software/hadoop/share/hadoop/common/lib/slf4j-log4j12-1.7.10.jar:/root/software/hadoop/share/hadoop/common/lib/commons-logging-1.1.3.jar:/root/software/hadoop/share/hadoop/common/lib/jetty-6.1.26.jar:/root/software/hadoop/share/hadoop/common/lib/mockito-all-1.8.5.jar:/root/software/hadoop/share/hadoop/common/lib/java-xmlbuilder-0.4.jar:/root/software/hadoop/share/hadoop/common/lib/commons-net-3.1.jar:/root/software/hadoop/share/hadoop/common/lib/servlet-api-2.5.jar:/root/software/hadoop/share/hadoop/common/lib/httpclient-4.2.5.jar:/root/software/hadoop/share/hadoop/common/lib/commons-lang-2.6.jar:/root/software/hadoop/share/hadoop/common/lib/zookeeper-3.4.6.jar:/root/software/hadoop/share/hadoop/common/lib/avro-1.7.4.jar:/root/software/hadoop/share/hadoop/common/lib/api-util-1.0.0-M20.jar:/root/software/hadoop/share/hadoop/common/lib/jettison-1.1.jar:/root/software/hadoop/share/hadoop/common/lib/commons-math3-3.1.1.jar:/root/software/hadoop/share/hadoop/common/lib/apacheds-kerberos-codec-2.0.0-M15.jar:/root/software/hadoop/share/hadoop/common/lib/commons-cli-1.2.jar:/root/software/hadoop/share/hadoop/common/lib/netty-3.6.2.Final.jar:/root/software/hadoop/share/hadoop/common/lib/commons-io-2.4.jar:/root/software/hadoop/share/hadoop/common/lib/jsr305-3.0.0.jar:/root/software/hadoop/share/hadoop/common/lib/jetty-sslengine-6.1.26.jar:/root/software/hadoop/share/hadoop/common/lib/stax-api-1.0-2.jar:/root/software/hadoop/share/hadoop/common/lib/jsp-api-2.1.jar:/root/software/hadoop/share/hadoop/common/lib/commons-codec-1.4.jar:/root/software/hadoop/share/hadoop/common/lib/snappy-java-1.0.4.1.jar:/root/software/hadoop/share/hadoop/common/lib/jaxb-api-2.2.2.jar:/root/software/hadoop/share/hadoop/common/lib/jetty-util-6.1.26.jar:/root/software/hadoop/share/hadoop/common/lib/commons-compress-1.4.1.jar:/root/software/hadoop/share/hadoop/common/lib/jsch-0.1.54.jar:/root/software/hadoop/share/hadoop/common/lib/curator-framework-2.7.1.jar:/root/software/hadoop/share/hadoop/common/lib/jersey-json-1.9.jar:/root/software/hadoop/share/hadoop/common/lib/htrace-core-3.1.0-incubating.jar:/root/software/hadoop/share/hadoop/common/lib/slf4j-api-1.7.10.jar:/root/software/hadoop/share/hadoop/common/lib/jaxb-impl-2.2.3-1.jar:/root/software/hadoop/share/hadoop/common/hadoop-nfs-2.7.7.jar:/root/software/hadoop/share/hadoop/common/hadoop-common-2.7.7.jar:/root/software/hadoop/share/hadoop/common/hadoop-common-2.7.7-tests.jar:/root/software/hadoop/share/hadoop/hdfs:/root/software/hadoop/share/hadoop/hdfs/lib/log4j-1.2.17.jar:/root/software/hadoop/share/hadoop/hdfs/lib/jersey-core-1.9.jar:/root/software/hadoop/share/hadoop/hdfs/lib/jackson-mapper-asl-1.9.13.jar:/root/software/hadoop/share/hadoop/hdfs/lib/xercesImpl-2.9.1.jar:/root/software/hadoop/share/hadoop/hdfs/lib/jersey-server-1.9.jar:/root/software/hadoop/share/hadoop/hdfs/lib/protobuf-java-2.5.0.jar:/root/software/hadoop/share/hadoop/hdfs/lib/jackson-core-asl-1.9.13.jar:/root/software/hadoop/share/hadoop/hdfs/lib/netty-all-4.0.23.Final.jar:/root/software/hadoop/share/hadoop/hdfs/lib/leveldbjni-all-1.8.jar:/root/software/hadoop/share/hadoop/hdfs/lib/asm-3.2.jar:/root/software/hadoop/share/hadoop/hdfs/lib/xml-apis-1.3.04.jar:/root/software/hadoop/share/hadoop/hdfs/lib/guava-11.0.2.jar:/root/software/hadoop/share/hadoop/hdfs/lib/xmlenc-0.52.jar:/root/software/hadoop/share/hadoop/hdfs/lib/commons-logging-1.1.3.jar:/root/software/hadoop/share/hadoop/hdfs/lib/jetty-6.1.26.jar:/root/software/hadoop/share/hadoop/hdfs/lib/servlet-api-2.5.jar:/root/software/hadoop/share/hadoop/hdfs/lib/commons-lang-2.6.jar:/root/software/hadoop/share/hadoop/hdfs/lib/commons-daemon-1.0.13.jar:/root/software/hadoop/share/hadoop/hdfs/lib/commons-cli-1.2.jar:/root/software/hadoop/share/hadoop/hdfs/lib/netty-3.6.2.Final.jar:/root/software/hadoop/share/hadoop/hdfs/lib/commons-io-2.4.jar:/root/software/hadoop/share/hadoop/hdfs/lib/jsr305-3.0.0.jar:/root/software/hadoop/share/hadoop/hdfs/lib/commons-codec-1.4.jar:/root/software/hadoop/share/hadoop/hdfs/lib/jetty-util-6.1.26.jar:/root/software/hadoop/share/hadoop/hdfs/lib/htrace-core-3.1.0-incubating.jar:/root/software/hadoop/share/hadoop/hdfs/hadoop-hdfs-2.7.7-tests.jar:/root/software/hadoop/share/hadoop/hdfs/hadoop-hdfs-2.7.7.jar:/root/software/hadoop/share/hadoop/hdfs/hadoop-hdfs-nfs-2.7.7.jar:/root/software/hadoop/share/hadoop/yarn/lib/jersey-client-1.9.jar:/root/software/hadoop/share/hadoop/yarn/lib/jackson-xc-1.9.13.jar:/root/software/hadoop/share/hadoop/yarn/lib/log4j-1.2.17.jar:/root/software/hadoop/share/hadoop/yarn/lib/jersey-core-1.9.jar:/root/software/hadoop/share/hadoop/yarn/lib/jackson-mapper-asl-1.9.13.jar:/root/software/hadoop/share/hadoop/yarn/lib/guice-3.0.jar:/root/software/hadoop/share/hadoop/yarn/lib/jersey-server-1.9.jar:/root/software/hadoop/share/hadoop/yarn/lib/protobuf-java-2.5.0.jar:/root/software/hadoop/share/hadoop/yarn/lib/jackson-core-asl-1.9.13.jar:/root/software/hadoop/share/hadoop/yarn/lib/activation-1.1.jar:/root/software/hadoop/share/hadoop/yarn/lib/commons-collections-3.2.2.jar:/root/software/hadoop/share/hadoop/yarn/lib/leveldbjni-all-1.8.jar:/root/software/hadoop/share/hadoop/yarn/lib/xz-1.0.jar:/root/software/hadoop/share/hadoop/yarn/lib/asm-3.2.jar:/root/software/hadoop/share/hadoop/yarn/lib/guava-11.0.2.jar:/root/software/hadoop/share/hadoop/yarn/lib/jackson-jaxrs-1.9.13.jar:/root/software/hadoop/share/hadoop/yarn/lib/commons-logging-1.1.3.jar:/root/software/hadoop/share/hadoop/yarn/lib/jetty-6.1.26.jar:/root/software/hadoop/share/hadoop/yarn/lib/servlet-api-2.5.jar:/root/software/hadoop/share/hadoop/yarn/lib/commons-lang-2.6.jar:/root/software/hadoop/share/hadoop/yarn/lib/zookeeper-3.4.6.jar:/root/software/hadoop/share/hadoop/yarn/lib/jettison-1.1.jar:/root/software/hadoop/share/hadoop/yarn/lib/aopalliance-1.0.jar:/root/software/hadoop/share/hadoop/yarn/lib/commons-cli-1.2.jar:/root/software/hadoop/share/hadoop/yarn/lib/netty-3.6.2.Final.jar:/root/software/hadoop/share/hadoop/yarn/lib/commons-io-2.4.jar:/root/software/hadoop/share/hadoop/yarn/lib/guice-servlet-3.0.jar:/root/software/hadoop/share/hadoop/yarn/lib/jsr305-3.0.0.jar:/root/software/hadoop/share/hadoop/yarn/lib/stax-api-1.0-2.jar:/root/software/hadoop/share/hadoop/yarn/lib/commons-codec-1.4.jar:/root/software/hadoop/share/hadoop/yarn/lib/zookeeper-3.4.6-tests.jar:/root/software/hadoop/share/hadoop/yarn/lib/javax.inject-1.jar:/root/software/hadoop/share/hadoop/yarn/lib/jaxb-api-2.2.2.jar:/root/software/hadoop/share/hadoop/yarn/lib/jetty-util-6.1.26.jar:/root/software/hadoop/share/hadoop/yarn/lib/commons-compress-1.4.1.jar:/root/software/hadoop/share/hadoop/yarn/lib/jersey-guice-1.9.jar:/root/software/hadoop/share/hadoop/yarn/lib/jersey-json-1.9.jar:/root/software/hadoop/share/hadoop/yarn/lib/jaxb-impl-2.2.3-1.jar:/root/software/hadoop/share/hadoop/yarn/hadoop-yarn-server-web-proxy-2.7.7.jar:/root/software/hadoop/share/hadoop/yarn/hadoop-yarn-registry-2.7.7.jar:/root/software/hadoop/share/hadoop/yarn/hadoop-yarn-api-2.7.7.jar:/root/software/hadoop/share/hadoop/yarn/hadoop-yarn-server-sharedcachemanager-2.7.7.jar:/root/software/hadoop/share/hadoop/yarn/hadoop-yarn-common-2.7.7.jar:/root/software/hadoop/share/hadoop/yarn/hadoop-yarn-applications-unmanaged-am-launcher-2.7.7.jar:/root/software/hadoop/share/hadoop/yarn/hadoop-yarn-server-tests-2.7.7.jar:/root/software/hadoop/share/hadoop/yarn/hadoop-yarn-client-2.7.7.jar:/root/software/hadoop/share/hadoop/yarn/hadoop-yarn-server-applicationhistoryservice-2.7.7.jar:/root/software/hadoop/share/hadoop/yarn/hadoop-yarn-server-resourcemanager-2.7.7.jar:/root/software/hadoop/share/hadoop/yarn/hadoop-yarn-applications-distributedshell-2.7.7.jar:/root/software/hadoop/share/hadoop/yarn/hadoop-yarn-server-common-2.7.7.jar:/root/software/hadoop/share/hadoop/yarn/hadoop-yarn-server-nodemanager-2.7.7.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/paranamer-2.3.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/log4j-1.2.17.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/jersey-core-1.9.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/jackson-mapper-asl-1.9.13.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/guice-3.0.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/hadoop-annotations-2.7.7.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/hamcrest-core-1.3.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/junit-4.11.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/jersey-server-1.9.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/protobuf-java-2.5.0.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/jackson-core-asl-1.9.13.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/leveldbjni-all-1.8.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/xz-1.0.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/asm-3.2.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/avro-1.7.4.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/aopalliance-1.0.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/netty-3.6.2.Final.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/commons-io-2.4.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/guice-servlet-3.0.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/snappy-java-1.0.4.1.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/javax.inject-1.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/commons-compress-1.4.1.jar:/root/software/hadoop/share/hadoop/mapreduce/lib/jersey-guice-1.9.jar:/root/software/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-hs-plugins-2.7.7.jar:/root/software/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-app-2.7.7.jar:/root/software/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-core-2.7.7.jar:/root/software/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-common-2.7.7.jar:/root/software/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-2.7.7-tests.jar:/root/software/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-2.7.7.jar:/root/software/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-hs-2.7.7.jar:/root/software/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.7.jar:/root/software/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-shuffle-2.7.7.jar:/root/software/hadoop/contrib/capacity-scheduler/*.jar:/root/software/hadoop/contrib/capacity-scheduler/*.jar
STARTUP_MSG:   build = Unknown -r c1aad84bd27cd79c3d1a7dd58202a8c3ee1ed3ac; compiled by 'stevel' on 2018-07-18T22:47Z
STARTUP_MSG:   java = 1.8.0_171
************************************************************/
19/10/15 01:12:09 INFO namenode.NameNode: registered UNIX signal handlers for [TERM, HUP, INT]
19/10/15 01:12:09 INFO namenode.NameNode: createNameNode [-format]
Formatting using clusterid: CID-9b2db537-6224-4ece-ba54-e2eb1da036f2
19/10/15 01:12:10 INFO namenode.FSNamesystem: No KeyProvider found.
19/10/15 01:12:10 INFO namenode.FSNamesystem: fsLock is fair: true
19/10/15 01:12:10 INFO namenode.FSNamesystem: Detailed lock hold time metrics enabled: false
19/10/15 01:12:10 INFO blockmanagement.DatanodeManager: dfs.block.invalidate.limit=1000
19/10/15 01:12:10 INFO blockmanagement.DatanodeManager: dfs.namenode.datanode.registration.ip-hostname-check=true
19/10/15 01:12:10 INFO blockmanagement.BlockManager: dfs.namenode.startup.delay.block.deletion.sec is set to 000:00:00:00.000
19/10/15 01:12:10 INFO blockmanagement.BlockManager: The block deletion will start around 2019 Oct 15 01:12:10
19/10/15 01:12:10 INFO util.GSet: Computing capacity for map BlocksMap
19/10/15 01:12:10 INFO util.GSet: VM type       = 64-bit
19/10/15 01:12:10 INFO util.GSet: 2.0% max memory 889 MB = 17.8 MB
19/10/15 01:12:10 INFO util.GSet: capacity      = 2^21 = 2097152 entries
19/10/15 01:12:10 INFO blockmanagement.BlockManager: dfs.block.access.token.enable=false
19/10/15 01:12:10 INFO blockmanagement.BlockManager: defaultReplication         = 3
19/10/15 01:12:10 INFO blockmanagement.BlockManager: maxReplication             = 512
19/10/15 01:12:10 INFO blockmanagement.BlockManager: minReplication             = 1
19/10/15 01:12:10 INFO blockmanagement.BlockManager: maxReplicationStreams      = 2
19/10/15 01:12:10 INFO blockmanagement.BlockManager: replicationRecheckInterval = 3000
19/10/15 01:12:10 INFO blockmanagement.BlockManager: encryptDataTransfer        = false
19/10/15 01:12:10 INFO blockmanagement.BlockManager: maxNumBlocksToLog          = 1000
19/10/15 01:12:10 INFO namenode.FSNamesystem: fsOwner             = root (auth:SIMPLE)
19/10/15 01:12:10 INFO namenode.FSNamesystem: supergroup          = supergroup
19/10/15 01:12:10 INFO namenode.FSNamesystem: isPermissionEnabled = false
19/10/15 01:12:10 INFO namenode.FSNamesystem: HA Enabled: false
19/10/15 01:12:10 INFO namenode.FSNamesystem: Append Enabled: true
19/10/15 01:12:10 INFO util.GSet: Computing capacity for map INodeMap
19/10/15 01:12:10 INFO util.GSet: VM type       = 64-bit
19/10/15 01:12:10 INFO util.GSet: 1.0% max memory 889 MB = 8.9 MB
19/10/15 01:12:10 INFO util.GSet: capacity      = 2^20 = 1048576 entries
19/10/15 01:12:10 INFO namenode.FSDirectory: ACLs enabled? false
19/10/15 01:12:10 INFO namenode.FSDirectory: XAttrs enabled? true
19/10/15 01:12:10 INFO namenode.FSDirectory: Maximum size of an xattr: 16384
19/10/15 01:12:10 INFO namenode.NameNode: Caching file names occuring more than 10 times
19/10/15 01:12:10 INFO util.GSet: Computing capacity for map cachedBlocks
19/10/15 01:12:10 INFO util.GSet: VM type       = 64-bit
19/10/15 01:12:10 INFO util.GSet: 0.25% max memory 889 MB = 2.2 MB
19/10/15 01:12:10 INFO util.GSet: capacity      = 2^18 = 262144 entries
19/10/15 01:12:10 INFO namenode.FSNamesystem: dfs.namenode.safemode.threshold-pct = 0.9990000128746033
19/10/15 01:12:10 INFO namenode.FSNamesystem: dfs.namenode.safemode.min.datanodes = 0
19/10/15 01:12:10 INFO namenode.FSNamesystem: dfs.namenode.safemode.extension     = 30000
19/10/15 01:12:10 INFO metrics.TopMetrics: NNTop conf: dfs.namenode.top.window.num.buckets = 10
19/10/15 01:12:10 INFO metrics.TopMetrics: NNTop conf: dfs.namenode.top.num.users = 10
19/10/15 01:12:10 INFO metrics.TopMetrics: NNTop conf: dfs.namenode.top.windows.minutes = 1,5,25
19/10/15 01:12:10 INFO namenode.FSNamesystem: Retry cache on namenode is enabled
19/10/15 01:12:10 INFO namenode.FSNamesystem: Retry cache will use 0.03 of total heap and retry cache entry expiry time is 600000 millis
19/10/15 01:12:10 INFO util.GSet: Computing capacity for map NameNodeRetryCache
19/10/15 01:12:10 INFO util.GSet: VM type       = 64-bit
19/10/15 01:12:10 INFO util.GSet: 0.029999999329447746% max memory 889 MB = 273.1 KB
19/10/15 01:12:10 INFO util.GSet: capacity      = 2^15 = 32768 entries
19/10/15 01:12:10 INFO namenode.FSImage: Allocated new BlockPoolId: BP-2097462600-172.18.0.71-1571101930518
19/10/15 01:12:10 INFO common.Storage: Storage directory /tmp/hadoop-root/dfs/name has been successfully formatted.
19/10/15 01:12:10 INFO namenode.FSImageFormatProtobuf: Saving image file /tmp/hadoop-root/dfs/name/current/fsimage.ckpt_0000000000000000000 using no compression
19/10/15 01:12:10 INFO namenode.FSImageFormatProtobuf: Image file /tmp/hadoop-root/dfs/name/current/fsimage.ckpt_0000000000000000000 of size 321 bytes saved in 0 seconds.
19/10/15 01:12:10 INFO namenode.NNStorageRetentionManager: Going to retain 1 images with txid >= 0
19/10/15 01:12:10 INFO util.ExitUtil: Exiting with status 0
19/10/15 01:12:10 INFO namenode.NameNode: SHUTDOWN_MSG: 
/************************************************************
SHUTDOWN_MSG: Shutting down NameNode at c7c57188b482/172.18.0.71
************************************************************/

[root@c7c57188b482 hadoop]# start-dfs.sh
Starting namenodes on [c7c57188b482]
The authenticity of host 'c7c57188b482 (172.18.0.71)' can't be established.
ECDSA key fingerprint is SHA256:wNaQZOYKNOWimeyHQIsFwCMyQcWanq3VgKjfmFrH4gw.
ECDSA key fingerprint is MD5:dc:f1:fc:16:f2:51:af:a3:cf:59:55:75:e2:0b:89:bd.
Are you sure you want to continue connecting (yes/no)? yes
c7c57188b482: Warning: Permanently added 'c7c57188b482,172.18.0.71' (ECDSA) to the list of known hosts.
c7c57188b482: starting namenode, logging to /root/packages/hugegraph/hadoop-2.7.7/logs/hadoop-root-namenode-c7c57188b482.out
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:wNaQZOYKNOWimeyHQIsFwCMyQcWanq3VgKjfmFrH4gw.
ECDSA key fingerprint is MD5:dc:f1:fc:16:f2:51:af:a3:cf:59:55:75:e2:0b:89:bd.
Are you sure you want to continue connecting (yes/no)? yes
localhost: Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
localhost: starting datanode, logging to /root/packages/hugegraph/hadoop-2.7.7/logs/hadoop-root-datanode-c7c57188b482.out
Starting secondary namenodes [0.0.0.0]
The authenticity of host '0.0.0.0 (0.0.0.0)' can't be established.
ECDSA key fingerprint is SHA256:wNaQZOYKNOWimeyHQIsFwCMyQcWanq3VgKjfmFrH4gw.
ECDSA key fingerprint is MD5:dc:f1:fc:16:f2:51:af:a3:cf:59:55:75:e2:0b:89:bd.
Are you sure you want to continue connecting (yes/no)? yes
0.0.0.0: Warning: Permanently added '0.0.0.0' (ECDSA) to the list of known hosts.
0.0.0.0: starting secondarynamenode, logging to /root/packages/hugegraph/hadoop-2.7.7/logs/hadoop-root-secondarynamenode-c7c57188b482.out

[root@c7c57188b482 hadoop]# start-yarn.sh
starting yarn daemons
starting resourcemanager, logging to /root/software/hadoop/logs/yarn-root-resourcemanager-c7c57188b482.out
localhost: starting nodemanager, logging to /root/packages/hugegraph/hadoop-2.7.7/logs/yarn-root-nodemanager-c7c57188b482.out

[root@c7c57188b482 hadoop]# jps | grep -E 'ResourceManager|DataNode|NodeManager|SecondaryNameNode|NameNode'
3121 SecondaryNameNode
2913 DataNode
3479 NodeManager
3352 ResourceManager
2766 NameNode
```
