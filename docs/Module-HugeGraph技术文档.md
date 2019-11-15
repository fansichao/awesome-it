# HugeGraph技术文档

tags: 开源 HugeGragh 图库 使用手册 2019年

文档信息:

- HugeGraph说明
  - 简介
  - 优缺点
  - 同行对比
- 安装部署 配置说明
- 其他等

HugeGragh0.9.0环境依赖:

- JDK-1.8
- 后端数据库要求
  - ScyllaDB
    - CentOS 7.3+
  - RocksDB
    - GCC-4.3.0(GLIBCXX_3.4.10)+
  - Hbase
    - JDK1.8+

scylladb和hbase都支持容量横向扩展（容量上它们一般不会是瓶颈），scylladb的定位是低延迟（没有Java GC停顿、高效的网络库等），hbase生态更加完善及稳定性较好。

当前环境

- CentOS7
- GCC-4.4.7
- JDK-1.8
- HugeGragh==0.9.0

TODO 数据冗余，多服务区，异常重连，数据删除等问题,性能测试
后续测试重点:

- 1、实际数据的导入性能测试
- 2、现有业务逻辑查询语法实现（API或Gremlin，优先API）
- 3、查询效率测试
- 4、多图库数据同步使用测试
- 5、任务调度管理API使用测试
- 6、底层存储替换测试

## HugeGraph简介

[HugeGraph](https://hugegraph.github.io/hugegraph-doc)是百度在2018年中旬开源的一款图数据库（Graph Database）系统，可以存储海量的顶点（Vertex）和边（Edge）。
实现了Apache ThinkerPop 3[1]框架，支持Gremlin图查询语言。
HugeGraph支持多用户并行操作，用户可输入Gremlin查询语句，并及时得到图查询结果。也可以再用户程序中调用hugeGraph API进行图分析或查询。

本系统具备如下特点:

- **易用**: HugeGraph支持Gremlin图查询语言与Restful API，同时提供图检索常用接口，具备功能齐全的周边工具，轻松实现基于图的各种查询分析运算。
- **高效**: HugeGraph在图存储和图计算方面做了深度优化，提供多种批量导入工具，轻松完成百亿数据快速导入，通过优化过的查询达到图检索的毫秒级响应。支持数千用户并发的在线实时操作。
- **通用**: HugeGraph支持Apache Gremlin标准图查询语言和Property Graph标准图建模方法，支持基于图的OLTP和OLAP方案。集成Apache Hadoop及Apache Spark大数据平台。
- **可扩展**: 支持分布式存储、数据多副本及横向扩容，内置多种后端存储引擎，也可插件式轻松扩展后端存储引擎。
- **开放**: HugeGraph代码开源（Apache 2 License），客户可自主修改定制，选择性回馈开源社区。

本系统的功能包括但不限于:

- 支持从TXT、CSV、JSON等格式的文件中批量导入数据
- 具备可视化操作界面，降低用户使用门槛
- 优化的图接口: 最短路径(Shortest Path)、K步连通子图(K-neighbor)、K步到达邻接点(K-out)等
- 基于Apache TinkerPop3框架实现，支持Gremlin图查询语言
- 支持属性图，顶点和边均可添加属性，支持丰富的属性类型
- 具备独立的Schema元数据信息，方便第三方系统集成
- 支持多顶点ID策略: 支持主键ID、支持自动生成ID、支持用户自定义字符串ID、支持用户自定义数字ID
- 可以对边和顶点的属性建立索引，支持精确查询、范围查询、全文检索
- 存储系统采用插件方式，支持RocksDB、Cassandra、ScyllaDB、HBase、Palo、MySQL以及InMemory等
- 与Hadoop、Spark GraphX等大数据系统集成，支持Bulk Load操作
- 对图数据库的核心功能（例如批量写入、最短路径、N度关系等）做了重点优化，与常见图数据库Neo4j和TitanDB等相比较，HugeGraph拥有明显的性能优势.
- HugeGraph支持HBase和Cassandra等常见的**分布式系统作为其存储引擎**来实现水平扩展。
- 支持任务查看,任务撤销。

其他等

- 支持分布式存储: 支持底层使用HBase、Cassandra等分布式存储backend
- 支持多图配置: 能够支持配置多个图库空间（未明确上线），可用于支持临时或单次的数据分析。（但需配套编写调度功能，指定分析库）
- 导入速率较快: 提供HugeGraph-Loader，可在线或离线导入数据，服务无需重启，可指定导入图库位置
- API接口已实现部分业务逻辑: 多步邻居，两者最短路径，两者全部路径，
- 提供任务监控API接口: 能够支持任务的状态查询并允许终止任务。

## 软件使用

### 配置文件修改

hugegraph-0.9.2/conf/rest-server.properties ServerIP地址和端口.配置0.0.0.0使其他机器可以访问。

```conf
(fenv) [fdm@neo4j hugegraph]$ cat hugegraph-0.9.2/conf/rest-server.properties
# bind url
#restserver.url=http://127.0.0.1:8080
restserver.url=http://0.0.0.0:8080

# graphs list with pair NAME:CONF_PATH
graphs=[hugegraph:conf/hugegraph.properties]

# authentication
#auth.require_authentication=
#auth.admin_token=
#auth.user_tokens=[]
```

### 安装部署

HugeGragh共有如下工具

- **一键部署**: 通过部署工具简单轻松的一键部署所有组件。参考hugegraph-tools deploy。
- **可视化界面**: 基于Web的可视化环境，提供图操作界面、图数据展示与分析。参考hugegraph-studio。
- **导入工具**: 数据导入工具，支持从txt、csv、json等格式文件导入到HugeGraph。参考hugegraph-loader。
- **导出工具**: 数据导出工具，可将顶点及关联边导出到文件，支持用户实现formatter自定义格式。参考hugegraph-tools/dump。
- **备份恢复工具**: 数据备份与恢复工具，支持定时备份、手动备份、手动恢复等功能。参考hugegraph-tools/backup&restore。
- **Gremlin任务工具**: Gremlin任务执行工具，支持同步执行Gremlin查询与分析（OLTP），支持异步执行Gremlin任务（OLAP）。参考hugegraph-tools/gremlin。
- **集成Spark GraphX工具(Github已下架)**: 基于Spark GraphX的大数据环境下的图分析工具。参考hugegraph-spark。

HugeGragh框架模块

- **HugeGraph-Server**: HugeGraph-Server是HugeGraph项目的核心部分，包含Core、Backend、API等子模块；
  - Core: 图引擎实现，向下连接Backend模块，向上支持API模块；
  - Backend: 实现将图数据存储到后端，支持的后端包括: Memory、Cassandra、ScyllaDB、RocksDB、HBase以及Mysql，用户根据实际情况选择一种即可；
  - API: 内置REST Server，向用户提供RESTful API，同时兼容Gremlin查询。
- **HugeGraph-Client**: HugeGraph-Client提供了RESTful API的客户端，用于连接HugeGraph-Server，目前仅实现Java版，其他语言用户可自行实现；
- **HugeGraph-Studio**: HugeGraph-Studio是HugeGraph的Web可视化工具，可用于执行Gremlin语句及展示图；
- **HugeGraph-Loader**: HugeGraph-Loader是基于HugeGraph-Client的数据导入工具，将普通文本数据转化为图形的顶点和边并插入图形数据库中；
- **HugeGraph-Spark**: 基于Spark GraphX的图分析工具 ，HugeGraph-Spark能在图上做并行计算，例如PageRank算法等；
- **HugeGraph-Tools**: HugeGraph-Tools是HugeGraph的部署和管理工具，包括管理图、备份/恢复、Gremlin执行等功能。

总结: 部署HugeGraph需要HugeGraph-Server，在网页上操作图需要HugeGraph-Studio。

需要安装 HugeGraph-Server HugeGraph-Studio HugeGraph-Loader 下载解压即用，详情见[HugeGraph官网](https://hugegraph.github.io/hugegraph-doc)

如需安装Hbase,请参考《Hbase安装文档》

安装部署命令

```bash
# 默认CentOS会自带这些包,Docker中的镜像需要自行安装
yum -y install lsof crontabs
```

### 配置数据库-RocksDB

- RocksDB 默认数据库无需哦配置

### 配置数据库-ScyllaDB

参考文档《ScyllaDB》



### 配置数据库-HBase

参考文档《Hbase安装文档》

**特殊声明：**由于安装Hbase，需要先安装Hadoop，配置 ResourceManager|DataNode|NodeManager|SecondaryNameNode|NameNode。
其中ResourceManager的端口8080和HugeGraph端口冲突，需要先修改ResourceManager端口

```conf
# vim ./share/doc/hadoop/hadoop-yarn/hadoop-yarn-common/yarn-default.xml
 134   <property>
 135     <description>The http address of the RM web application.</description>
 136     <name>yarn.resourcemanager.webapp.address</name>
 137     <value>${yarn.resourcemanager.hostname}:8081</value>
 138   </property>
# 修改点，原 8080 修改为 8081。 重启Hadoop服务 stop-all.sh & start-all.sh
```

### 配置HugeGraph连接数据库

修改配置文件


初始化数据库

bin/init-store.sh

> 初始化数据库时，必须先 bin/stop-hugegraph.sh ,否则可能初始化失败。

启动服务

bin/start-hugegraph.sh
> 启动服务时,必须先关闭 hugegraph-studio 服务。否则会启动失败,报错端口已被使用。




### HugeGragh支持多图库模式

TODO (未发现多库查询方法)

参考链接: [HugeGraph 配置](https://hugegraph.github.io/hugegraph-doc/config/config-guide.html)

### 常用命令

一键重启脚本

```bash
restart_hugegraph(){
    hugegraph_pwd="/home/scfan/software/hugegraph"
    # 关闭服务
    ps anx | grep hugegraph-studio|awk '{print $1}' | xargs kill -9
    cd $hugegraph_pwd/hugegraph-0.9.2 && bin/stop-hugegraph.sh

    # 启动服务
    cd $hugegraph_pwd/hugegraph-studio-0.9.0 && nohup bin/hugegraph-studio.sh &
    # Server修改配置后,需要关闭 studio 才可以启动
    cd $hugegraph_pwd/hugegraph-0.9.2 && bin/start-hugegraph.sh
}
restart_hugegraph
```

其他命令

```bash

# 数据导入命令
cd /home/scfan/software/hugegraph/hugegraph/hugegraph-loader-0.9.0
time bin/hugegraph-loader -g hugegraph -f example/graph_struct.json -s example/graph_schema.groovy

# 删除整个图库数据
curl -XDELETE "http://192.168.100.162:8080/graphs/hugegraph/clear?confirm_message=I'm+sure+to+delete+all+data"
# 支持任务撤销
PUT http://localhost:8080/graphs/hugegraph/tasks/2?action=cancel
```

可视化界面Studio: [http://192.168.172.72:8088/](http://192.168.172.72:8088/)
后端端口Server: [http://192.168.172.72:8080/graphs](http://192.168.172.72:8080/graphs)

![hugegraph_可视化界面](pictures/hugegraph_可视化界面.png)

## HugeGraph数据导入

官方链接: [HugeGraph-Loader Quick Start](https://hugegraph.github.io/hugegraph-doc/quickstart/hugegraph-loader.html)

HugeGraph-Loader 是 HugeGragh 的数据导入组件，能够将多种数据源的数据转化为图的顶点和边并批量导入到图数据库中。

目前支持的数据源包括:

- 本地磁盘文件或目录，支持压缩文件
- HDFS 文件或目录，支持压缩文件
- 部分关系型数据库，如 MySQL

## 附件

### 问题

#### 未停止服务,修改配置文件后,服务无法重启

hugegraph服务启动失败
(env) [scfan@scfan hugegraph-0.9.2]$ bin/stop-hugegraph.sh
no crontab for scfan
The HugeGraphServer monitor has been closed
The pid file /home/scfan/software/hugegraph/hugegraph-0.9.2/bin/pid doesn't exist
(env) [scfan@scfan hugegraph-0.9.2]$ bin/start-hugegraph.sh
The port 8080 has already been used

解决方案:
    先关闭 hugegraph-studio-0.9.0] 即可重启 hugegraph服务

多库合并操作 查询等....

####  Failed to update/query TaskStore

问题场景: 使用 scylladb 初始化数据库时报错。


日志信息

```bash
(env) [scfan@scfan hugegraph-0.9.2]$ bin/init-store.sh
Initing HugeGraph Store...
2019-10-12 11:27:04 1478  [main] [INFO ] com.baidu.hugegraph.cmd.InitStore [] - Init graph with config file: conf/hugegraph.properties
2019-10-12 11:27:04 1683  [main] [INFO ] com.baidu.hugegraph.HugeGraph [] - Opening backend store 'rocksdb' for graph 'hugegraph'
2019-10-12 11:27:04 1789  [main] [INFO ] com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore [] - Opening RocksDB with data path: /home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/schema
2019-10-12 11:27:05 2126  [main] [ERROR] com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore [] - Failed to open RocksDB '/home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/schema'
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStdSessions.<init>(RocksDBStdSessions.java:122) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.openSessionPool(RocksDBStore.java:241) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:181) [hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:172) [hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:155) [hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.tx.AbstractTransaction.<init>(AbstractTransaction.java:72) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.tx.IndexableTransaction.<init>(IndexableTransaction.java:30) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.tx.SchemaTransaction.<init>(SchemaTransaction.java:68) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.cache.CachedSchemaTransaction.<init>(CachedSchemaTransaction.java:53) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph.openSchemaTransaction(HugeGraph.java:250) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph.access$300(HugeGraph.java:80) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph$TinkerpopTransaction.getOrNewTransaction(HugeGraph.java:730) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph$TinkerpopTransaction.schemaTransaction(HugeGraph.java:713) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph$TinkerpopTransaction.access$000(HugeGraph.java:588) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph.schemaTransaction(HugeGraph.java:301) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.store.BackendStoreSystemInfo.info(BackendStoreSystemInfo.java:66) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.store.BackendStoreSystemInfo.exist(BackendStoreSystemInfo.java:78) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.cmd.InitStore.initGraph(InitStore.java:99) [hugegraph-dist-0.9.2.jar:?]
	at com.baidu.hugegraph.cmd.InitStore.main(InitStore.java:87) [hugegraph-dist-0.9.2.jar:?]
2019-10-12 11:27:05 2131  [main] [ERROR] com.baidu.hugegraph.HugeGraph [] - Failed to open schema transaction
com.baidu.hugegraph.backend.BackendException: Failed to open RocksDB '/home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/schema'
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:219) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:172) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:155) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.tx.AbstractTransaction.<init>(AbstractTransaction.java:72) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.tx.IndexableTransaction.<init>(IndexableTransaction.java:30) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.tx.SchemaTransaction.<init>(SchemaTransaction.java:68) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.cache.CachedSchemaTransaction.<init>(CachedSchemaTransaction.java:53) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph.openSchemaTransaction(HugeGraph.java:250) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph.access$300(HugeGraph.java:80) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph$TinkerpopTransaction.getOrNewTransaction(HugeGraph.java:730) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph$TinkerpopTransaction.schemaTransaction(HugeGraph.java:713) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph$TinkerpopTransaction.access$000(HugeGraph.java:588) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph.schemaTransaction(HugeGraph.java:301) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.store.BackendStoreSystemInfo.info(BackendStoreSystemInfo.java:66) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.store.BackendStoreSystemInfo.exist(BackendStoreSystemInfo.java:78) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.cmd.InitStore.initGraph(InitStore.java:99) [hugegraph-dist-0.9.2.jar:?]
	at com.baidu.hugegraph.cmd.InitStore.main(InitStore.java:87) [hugegraph-dist-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStdSessions.<init>(RocksDBStdSessions.java:122) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.openSessionPool(RocksDBStore.java:241) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:181) ~[hugegraph-rocksdb-0.9.2.jar:?]
2019-10-12 11:27:05 2155  [task-db-worker-1] [INFO ] com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore [] - Opening RocksDB with data path: /home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/system
2019-10-12 11:27:05 2161  [task-db-worker-1] [ERROR] com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore [] - Failed to open RocksDB '/home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/system'
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStdSessions.<init>(RocksDBStdSessions.java:122) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.openSessionPool(RocksDBStore.java:241) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:181) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:172) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:155) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.tx.AbstractTransaction.<init>(AbstractTransaction.java:72) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.tx.IndexableTransaction.<init>(IndexableTransaction.java:30) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.tx.GraphTransaction.<init>(GraphTransaction.java:119) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.task.TaskScheduler$TaskTransaction.<init>(TaskScheduler.java:406) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.task.TaskScheduler.tx(TaskScheduler.java:111) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.task.TaskScheduler.lambda$close$3(TaskScheduler.java:206) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
Exception in thread "main" com.baidu.hugegraph.HugeException: Failed to update/query TaskStore
	at com.baidu.hugegraph.task.TaskScheduler.call(TaskScheduler.java:397)
	at com.baidu.hugegraph.task.TaskScheduler.call(TaskScheduler.java:389)
	at com.baidu.hugegraph.task.TaskScheduler.close(TaskScheduler.java:205)
	at com.baidu.hugegraph.task.TaskManager.closeScheduler(TaskManager.java:73)
	at com.baidu.hugegraph.HugeGraph.close(HugeGraph.java:460)
	at com.baidu.hugegraph.cmd.InitStore.initGraph(InitStore.java:107)
	at com.baidu.hugegraph.cmd.InitStore.main(InitStore.java:87)
Caused by: java.util.concurrent.ExecutionException: com.baidu.hugegraph.backend.BackendException: Failed to open RocksDB '/home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/system'
	at java.util.concurrent.FutureTask.report(FutureTask.java:122)
	at java.util.concurrent.FutureTask.get(FutureTask.java:192)
	at com.baidu.hugegraph.task.TaskScheduler.call(TaskScheduler.java:395)
	... 6 more
Caused by: com.baidu.hugegraph.backend.BackendException: Failed to open RocksDB '/home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/system'
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:219)
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:172)
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:155)
	at com.baidu.hugegraph.backend.tx.AbstractTransaction.<init>(AbstractTransaction.java:72)
	at com.baidu.hugegraph.backend.tx.IndexableTransaction.<init>(IndexableTransaction.java:30)
	at com.baidu.hugegraph.backend.tx.GraphTransaction.<init>(GraphTransaction.java:119)
	at com.baidu.hugegraph.task.TaskScheduler$TaskTransaction.<init>(TaskScheduler.java:406)
	at com.baidu.hugegraph.task.TaskScheduler.tx(TaskScheduler.java:111)
	at com.baidu.hugegraph.task.TaskScheduler.lambda$close$3(TaskScheduler.java:206)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: org.rocksdb.RocksDBException: While lock file: /home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/system/LOCK: Resource temporarily unavailable
	at org.rocksdb.RocksDB.open(Native Method)
	at org.rocksdb.RocksDB.open(RocksDB.java:286)
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStdSessions.<init>(RocksDBStdSessions.java:122)
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.openSessionPool(RocksDBStore.java:241)
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:181)
	... 13 more
```


#### HugeGraph_问题_使用scylladb数据库初始化报错.

![HugeGraph_问题_使用scylladb数据库初始化报错](https://img-blog.csdnimg.cn/20191012154029962.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzIxMTY1MDA3,size_16,color_FFFFFF,t_70)

问题原因：

- 初始化时，未关闭 hugegraph,导致报错, 关闭后正常执行。

### 参考资源

- [HugeGraph的Github链接](https://hugegraph.github.io/hugegraph-doc/)
- [HugeGraph初使用](https://www.imbajin.com/2019-01-08-%E5%9B%BE%E7%B3%BB%E7%BB%9F-HugeGraph%E5%88%9D%E8%AF%86/)
- [官方文档](https://hugegraph.github.io/hugegraph-doc/)
- [百度安全开源大规模图数据库HugeGraph](https://www.secrss.com/articles/4305)
- [十亿数据的快速导入](https://www.jianshu.com/p/7002ce359bfc)
- [图数据库功能说明](https://blog.csdn.net/u010260089/article/details/82844321)
- [图数据库对比](https://blog.csdn.net/wzwdcld/article/details/81384635)

### 图库热度排行榜

[hugegraph_DBengine图库排行榜](https://db-engines.com/en/ranking/graph+dbms)
![hugegraph_DBengine图库排行榜](pictures/hugegraph_DBengine图库排行榜.png)

### 图库综合对比

![hugegraph_图库综合对比](pictures/hugegraph_图库综合对比.png)
