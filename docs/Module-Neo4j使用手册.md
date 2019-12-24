# Neo4j使用手册

<!-- TOC -->autoauto- [Neo4j使用手册](#neo4j使用手册)auto    - [Neo4j入门介绍](#neo4j入门介绍)auto    - [安装部署](#安装部署)auto    - [软件使用](#软件使用)auto        - [配置文件](#配置文件)auto    - [Neo4j语法](#neo4j语法)auto        - [Neo4j术语/概念](#neo4j术语概念)auto        - [Neo4j运算符](#neo4j运算符)auto        - [Cypher语法](#cypher语法)auto        - [Cpyher函数](#cpyher函数)auto        - [Cypher常用语句](#cypher常用语句)auto    - [数据导入](#数据导入)auto        - [Neo4j-import](#neo4j-import)auto            - [文件格式](#文件格式)auto            - [导入命令](#导入命令)auto        - [batch-import](#batch-import)auto            - [文件格式](#文件格式-1)auto            - [导入命令](#导入命令-1)auto        - [Load-csv](#load-csv)auto            - [文件格式](#文件格式-2)auto    - [问题记录](#问题记录)auto        - [Value 15979221751 is too big to be represented as int](#value-15979221751-is-too-big-to-be-represented-as-int)auto        - [already contains a database](#already-contains-a-database)auto        - [Max 1024 open files allowed, minimum of 40000 recommended.](#max-1024-open-files-allowed-minimum-of-40000-recommended)auto        - [其他情况](#其他情况)auto    - [其他说明](#其他说明)auto        - [参考资源](#参考资源)auto        - [No4j最大支持节点和关系数量](#no4j最大支持节点和关系数量)auto        - [Neo4j数据预热](#neo4j数据预热)auto        - [检查Neo4j是否启动](#检查neo4j是否启动)auto        - [性能测试](#性能测试)autoauto<!-- /TOC -->

## Neo4j入门介绍

http://dl2.iteye.com/upload/attachment/0120/3433/e84b4219-9e96-31fb-927f-241366d91c74.png

> Neo4j 是目前最流行的图形数据库，支持完整的事务，在属性图中，图是由顶点（Vertex），边（Edge）和属性（Property）组成的，
顶点和边都可以设置属性，顶点也称作节点，边也称作关系，每个节点和关系都可以由一个或多个属性。
Neo4j创建的图是用顶点和边构建一个有向图，其查询语言cypher已经成为事实上的标准。

它包括如下几个显著特点：

- 完整的ACID支持
- 高可用性
- 轻易扩展到上亿级别的节点和关系
- 通过遍历工具高速检索数据

其他的图形数据库还包括Oracle NoSQL数据库，OrientDB，HypherGraphDB，GraphBase，InfiniteGraph，AllegroGraph。

## 安装部署

环境说明

- 版本说明: neo4j-community-3.3.5
- 系统版本: CentOS6.10/CentOS7.5

部署说明

- 安装包获取: [Neo4j官网](https://neo4j.com/)下载
- [Neo4j安装包3.3.5](https://neo4j.com/artifact.php?name=neo4j-community-3.3.5-unix.tar.gz)
- 前置依赖:
  - Java1.8+
  - 系统文件数40000+
  
```bash
# vi /etc/security/limits.conf
fdm              soft    nofile          65535
fdm              hard    nofile          65535
# 修改后重新进入ssh
# fdm为用户名称
```

- 安装说明: 解压即用
- 配置文件: ```conf/neo4j.conf```
- 软件使用:
  - ```bin/neo4j restart``` 服务重启,启动在后台
  - ```bin/neo4j console``` 服务启动,启动在前台
  - Neo4j页面入口 [http://localhost:7474](http://localhost:7474)

## 软件使用

软件目录说明：

- bin目录：用于存储Neo4j的可执行程序；
- conf目录：用于控制Neo4j启动的配置文件；
- data目录：用于存储核心数据库文件；
- plugins目录：用于存储Neo4j的插件；
- import目录：用于存放load csv文件,作为根目录(配置文件中可修改)

### 配置文件

配置文件路径: ```conf/neo4j.conf```

配置文件说明

```bash
# For more details and a complete list of settings, please see https://neo4j.com/docs/operations-manual/current/reference/configuration-settings/

# 如果想自定义neo4j数据库数据的存储路径，要同时修改dbms.active_database 和 dbms.directories.data 两项配置，
# 修改配置后，数据会存放在${dbms.directories.data}/databases/${dbms.active_database} 目录下
# 安装的数据库的名称，默认使用${NEO4J_HOME}/data/databases/graph.db目录
# The name of the database to mount  
#dbms.active_database=graph.db

#安装Neo4j数据库的各个配置路径，默认使用$NEO4J_HOME下的路径
#Paths of directories in the installation.
# 数据路径
#dbms.directories.data=data  
# 插件路径
#dbms.directories.plugins=plugins  
#dbms.directories.certificates=certificates  证书路径
#dbms.directories.logs=logs 日志路径
#dbms.directories.lib=lib jar包路径
#dbms.directories.run=run 运行路径

#默认情况下想load csv文件，只能把csv文件放到${NEO4J_HOME}/import目录下，把下面的#删除后，可以在load csv时使用绝对路径，这样可能不安全
#This setting constrains all `LOAD CSV` import files to be under the `import` directory. Remove or comment it out to allow files to be loaded from anywhere in the filesystem; this introduces possible security problems. See the `LOAD CSV` section of the manual for details.  
#此设置将所有“LOAD CSV”导入文件限制在`import`目录下。删除注释允许从文件系统的任何地方加载文件;这引入了可能的安全问题。
dbms.directories.import=import

#把下面这行的#删掉后，连接neo4j数据库时就不用输密码了
#Whether requests to Neo4j are authenticated. 是否对Neo4j的请求进行了身份验证。
#To disable authentication, uncomment this line 要禁用身份验证，请取消注释此行。
#dbms.security.auth_enabled=false

#Enable this to be able to upgrade a store from an older version. 是否兼容以前版本的数据
dbms.allow_format_migration=true

#Java Heap Size: by default the Java heap size is dynamically calculated based on available system resources. Java堆大小：默认情况下，Java堆大小是动态地根据可用的系统资源计算。
#Uncomment these lines to set specific initial and maximum heap size. 取消注释这些行以设置特定的初始值和最大值
#dbms.memory.heap.initial_size=512m
#dbms.memory.heap.max_size=512m

#The amount of memory to use for mapping the store files, in bytes (or kilobytes with the 'k' suffix, megabytes with 'm' and gigabytes with 'g'). 
# 用于映射存储文件的内存量（以字节为单位）千字节带有'k'后缀，兆字节带有'm'，千兆字节带有'g'）。
#If Neo4j is running on a dedicated server, then it is generally recommended to leave about 2-4 gigabytes for the operating system, give the JVM enough heap to hold all your transaction state and query context, and then leave the rest for the page cache. 
# 如果Neo4j在专用服务器上运行，那么通常建议为操作系统保留大约2-4千兆字节，为JVM提供足够的堆来保存所有的事务状态和查询上下文，然后保留其余的页面缓存 。
#The default page cache memory assumes the machine is dedicated to running Neo4j, and is heuristically set to 50% of RAM minus the max Java heap size.  默认页面缓存存储器假定机器专用于运行Neo4j，并且试探性地设置为RAM的50％减去最大Java堆大小。
#dbms.memory.pagecache.size=10g


### Network connector configuration

#With default configuration Neo4j only accepts local connections. Neo4j默认只接受本地连接(localhost)
#To accept non-local connections, uncomment this line:  要接受非本地连接，请取消注释此行
# (这是删除#后的配置，可以通过ip访问)
dbms.connectors.default_listen_address=0.0.0.0

#You can also choose a specific network interface, and configure a non-default port for each connector, by setting their individual listen_address. 还可以选择特定的网络接口，并配置非默认值端口，设置它们各自的listen_address

#The address at which this server can be reached by its clients. This may be the server's IP address or DNS name, or it may be the address of a reverse proxy which sits in front of the server. This setting may be overridden for individual connectors below. 客户端可以访问此服务器的地址。这可以是服务器的IP地址或DNS名称，或者可以是位于服务器前面的反向代理的地址。此设置可能会覆盖以下各个连接器。
#dbms.connectors.default_advertised_address=localhost

#You can also choose a specific advertised hostname or IP address, and configure an advertised port for each connector, by setting their individual advertised_address. 您还可以选择特定广播主机名或IP地址，
# 为每个连接器配置通告的端口，通过设置它们独特的advertised_address。

#Bolt connector 使用Bolt协议
dbms.connector.bolt.enabled=true
dbms.connector.bolt.tls_level=OPTIONAL
dbms.connector.bolt.listen_address=:7687

#HTTP Connector. There must be exactly one HTTP connector. 使用http协议
dbms.connector.http.enabled=true
dbms.connector.http.listen_address=:7474

#HTTPS Connector. There can be zero or one HTTPS connectors. 使用https协议
dbms.connector.https.enabled=true
dbms.connector.https.listen_address=:7473

#Number of Neo4j worker threads. Neo4j线程数
#dbms.threads.worker_count=


#Logging configuration  日志配置

#To enable HTTP logging, uncomment this line  要启用HTTP日志记录，请取消注释此行
dbms.logs.http.enabled=true

#Number of HTTP logs to keep. 要保留的HTTP日志数
#dbms.logs.http.rotation.keep_number=5

#Size of each HTTP log that is kept. 每个HTTP日志文件的大小
dbms.logs.http.rotation.size=20m

#To enable GC Logging, uncomment this line 要启用GC日志记录，请取消注释此行
#dbms.logs.gc.enabled=true

#GC Logging Options see http://docs.oracle.com/cd/E19957-01/819-0084-10/pt_tuningjava.html#wp57013 for more information.  GC日志记录选项 有关详细信息，请参见http://docs.oracle.com/cd/E19957-01/819-0084-10/pt_tuningjava.html#wp57013
#dbms.logs.gc.options=-XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCApplicationStoppedTime -XX:+PrintPromotionFailure -XX:+PrintTenuringDistribution

#Number of GC logs to keep. 要保留的GC日志数
#dbms.logs.gc.rotation.keep_number=5

#Size of each GC log that is kept. 保留的每个GC日志文件的大小
#dbms.logs.gc.rotation.size=20m

#Size threshold for rotation of the debug log. If set to zero then no rotation will occur. Accepts a binary suffix "k", "m" or "g".  调试日志旋转的大小阈值。如果设置为零，则不会发生滚动(达到指定大小后切割日志文件)。接受二进制后缀“k”，“m”或“g”。
#dbms.logs.debug.rotation.size=20m

#Maximum number of history files for the internal log. 最多保存几个日志文件
#dbms.logs.debug.rotation.keep_number=7


### Miscellaneous configuration  其他配置


#Enable this to specify a parser other than the default one. 启用此选项可指定除默认解析器之外的解析器
#cypher.default_language_version=3.0

#Determines if Cypher will allow using file URLs when loading data using `LOAD CSV`. Setting this value to `false` will cause Neo4j to fail `LOAD CSV` clauses that load data from the file system.
# 确定当使用加载数据时，Cypher是否允许使用文件URL `LOAD CSV`。将此值设置为`false`将导致Neo4j不能通过互联网上的URL导入数据，`LOAD CSV` 会从文件系统加载数据。
dbms.security.allow_csv_import_from_file_urls=true

#Retention policy for transaction logs needed to perform recovery and backups.  执行恢复和备份所需的事务日志的保留策略
#dbms.tx_log.rotation.retention_policy=7 days

#Enable a remote shell server which Neo4j Shell clients can log in to.  启用Neo4j Shell客户端可以登录的远程shell服务器
dbms.shell.enabled=true
#The network interface IP the shell will listen on (use 0.0.0.0 for all interfaces).
dbms.shell.host=127.0.0.1
#The port the shell will listen on, default is 1337.
dbms.shell.port=1337

#Only allow read operations from this Neo4j instance. This mode still requires write access to the directory for lock purposes.  
# 只允许从Neo4j实例读取操作。此模式仍然需要对目录的写访问以用于锁定目的。
#dbms.read_only=false

#Comma separated list of JAX-RS packages containing JAX-RS resources, one package name for each mountpoint. The listed package names will be loaded under the mountpoints specified. Uncomment this line to mount the org.neo4j.examples.server.unmanaged.HelloWorldResource.java from neo4j-server-examples under /examples/unmanaged, resulting in a final URL of http://localhost:7474/examples/unmanaged/helloworld/{nodeId}      包含JAX-RS资源的JAX-RS软件包的逗号分隔列表，每个安装点一个软件包名称。所列出的软件包名称将在指定的安装点下加载。取消注释此行以装载org.neo4j.examples.server.unmanaged.HelloWorldResource.java neo4j-server-examples下/ examples / unmanaged，最终的URL为http//localhost7474/examples/unmanaged/helloworld/{nodeId}
#dbms.unmanaged_extension_classes=org.neo4j.examples.server.unmanaged=/examples/unmanaged


#JVM Parameters  JVM参数

#G1GC generally strikes a good balance between throughput and tail latency, without too much tuning. G1GC通常在吞吐量和尾部延迟之间达到很好的平衡，而没有太多的调整。
dbms.jvm.additional=-XX:+UseG1GC

#Have common exceptions keep producing stack traces, so they can be debugged regardless of how often logs are rotated. 有共同的异常保持生成堆栈跟踪，所以他们可以被调试，无论日志被旋转的频率
dbms.jvm.additional=-XX:-OmitStackTraceInFastThrow

#Make sure that `initmemory` is not only allocated, but committed to the process, before starting the database. This reduces memory fragmentation, increasing the effectiveness of transparent huge pages. It also reduces the possibility of seeing performance drop due to heap-growing GC events, where a decrease in available page cache leads to an increase in mean IO response time. Try reducing the heap memory, if this flag degrades performance.    确保在启动数据库之前，“initmemory”不仅被分配，而且被提交到进程。这减少了内存碎片，增加了透明大页面的有效性。它还减少了由于堆增长的GC事件而导致性能下降的可能性，其中可用页面缓存的减少导致平均IO响应时间的增加。如果此标志降低性能，请减少堆内存。    
dbms.jvm.additional=-XX:+AlwaysPreTouch

#Trust that non-static final fields are really final. This allows more optimizations and improves overall performance. NOTE: Disable this if you use embedded mode, or have extensions or dependencies that may use reflection or serialization to change the value of final fields!    信任非静态final字段真的是final。这允许更多的优化和提高整体性能。注意：如果使用嵌入模式，或者有可能使用反射或序列化更改最终字段的值的扩展或依赖关系，请禁用此选项！
dbms.jvm.additional=-XX:+UnlockExperimentalVMOptions
dbms.jvm.additional=-XX:+TrustFinalNonStaticFields

#Disable explicit garbage collection, which is occasionally invoked by the JDK itself.  禁用显式垃圾回收，这是偶尔由JDK本身调用。
dbms.jvm.additional=-XX:+DisableExplicitGC

#Remote JMX monitoring, uncomment and adjust the following lines as needed. Absolute paths to jmx.access and jmx.password files are required.  
# 远程JMX监视，取消注释并根据需要调整以下行。需要jmx.access和jmx.password文件的绝对路径。
#Also make sure to update the jmx.access and jmx.password files with appropriate permission roles and passwords, the shipped configuration contains only a read only role called 'monitor' with password 'Neo4j'. 
# 还要确保使用适当的权限角色和密码更新jmx.access和jmx.password文件，所配置的配置只包含名为“monitor”的只读角色，密码为“Neo4j”。
#For more details, see: http://download.oracle.com/javase/8/docs/technotes/guides/management/agent.html On Unix based systems the jmx.password file needs to be owned by the user that will run the server, and have permissions set to 0600. Unix系统，有关详情，请参阅：http：//download.oracle.com/javase/8/docs/technotes/guides/management/agent.html，jmx.password文件需要由运行服务器的用户拥有，并且权限设置为0600。
#For details on setting these file permissions on Windows see: http://docs.oracle.com/javase/8/docs/technotes/guides/management/security-windows.html   Windows系统  有关在设置这些文件权限的详细信息，请参阅：http://docs.oracle.com/javase/8/docs/technotes/guides/management/security-windows.html
#dbms.jvm.additional=-Dcom.sun.management.jmxremote.port=3637
#dbms.jvm.additional=-Dcom.sun.management.jmxremote.authenticate=true
#dbms.jvm.additional=-Dcom.sun.management.jmxremote.ssl=false
#dbms.jvm.additional=-Dcom.sun.management.jmxremote.password.file=/absolute/path/to/conf/jmx.password
#dbms.jvm.additional=-Dcom.sun.management.jmxremote.access.file=/absolute/path/to/conf/jmx.access

#Some systems cannot discover host name automatically, and need this line configured:  某些系统无法自动发现主机名，需要配置以下行：
#dbms.jvm.additional=-Djava.rmi.server.hostname=$THE_NEO4J_SERVER_HOSTNAME

#Expand Diffie Hellman (DH) key size from default 1024 to 2048 for DH-RSA cipher suites used in server TLS handshakes. 对于服务器TLS握手中使用的DH-RSA密码套件，将Diffie Hellman（DH）密钥大小从默认1024展开到2048。
#This is to protect the server from any potential passive eavesdropping. 这是为了保护服务器免受任何潜在的被动窃听。
dbms.jvm.additional=-Djdk.tls.ephemeralDHKeySize=2048


### Wrapper Windows NT/2000/XP Service Properties  包装器Windows NT / 2000 / XP服务属性包装器Windows NT / 2000 / XP服务属性

#WARNING - Do not modify any of these properties when an application using this configuration file has been installed as a service.  WARNING - 当使用此配置文件的应用程序已作为服务安装时，不要修改任何这些属性。
#Please uninstall the service before modifying this section.  The service can then be reinstalled. 请在修改此部分之前卸载服务。 然后可以重新安装该服务。

#Name of the service 服务的名称
dbms.windows_service_name=neo4j


### Other Neo4j system properties  其他Neo4j系统属性
dbms.jvm.additional=-Dunsupported.dbms.udc.source=zip
```

默认的Neo4j配置文件

```bash
#*****************************************************************
# Neo4j configuration
#
# For more details and a complete list of settings, please see
# https://neo4j.com/docs/operations-manual/current/reference/configuration-settings/
#*****************************************************************

# The name of the database to mount
dbms.active_database=graph.db

# Paths of directories in the installation.
#dbms.directories.data=data
#dbms.directories.plugins=plugins
#dbms.directories.certificates=certificates
#dbms.directories.logs=logs
#dbms.directories.lib=lib
#dbms.directories.run=run

# This setting constrains all `LOAD CSV` import files to be under the `import` directory. Remove or comment it out to
# allow files to be loaded from anywhere in the filesystem; this introduces possible security problems. See the
# `LOAD CSV` section of the manual for details.
dbms.directories.import=import

# Whether requests to Neo4j are authenticated.
# To disable authentication, uncomment this line
#dbms.security.auth_enabled=false

# Enable this to be able to upgrade a store from an older version.
#dbms.allow_upgrade=true

# Java Heap Size: by default the Java heap size is dynamically
# calculated based on available system resources.
# Uncomment these lines to set specific initial and maximum
# heap size.
#dbms.memory.heap.initial_size=512m
#dbms.memory.heap.max_size=512m
dbms.memory.heap.initial_size=1024m
dbms.memory.heap.max_size=1024m

# The amount of memory to use for mapping the store files, in bytes (or
# kilobytes with the 'k' suffix, megabytes with 'm' and gigabytes with 'g').
# If Neo4j is running on a dedicated server, then it is generally recommended
# to leave about 2-4 gigabytes for the operating system, give the JVM enough
# heap to hold all your transaction state and query context, and then leave the
# rest for the page cache.
# The default page cache memory assumes the machine is dedicated to running
# Neo4j, and is heuristically set to 50% of RAM minus the max Java heap size.
#dbms.memory.pagecache.size=10g
dbms.memory.pagecache.size=20g

#*****************************************************************
# Network connector configuration
#*****************************************************************

# With default configuration Neo4j only accepts local connections.
# To accept non-local connections, uncomment this line:
dbms.connectors.default_listen_address=localhost

# You can also choose a specific network interface, and configure a non-default
# port for each connector, by setting their individual listen_address.

# The address at which this server can be reached by its clients. This may be the server's IP address or DNS name, or
# it may be the address of a reverse proxy which sits in front of the server. This setting may be overridden for
# individual connectors below.
#dbms.connectors.default_advertised_address=localhost
dbms.connectors.default_advertised_address=localhost

# You can also choose a specific advertised hostname or IP address, and
# configure an advertised port for each connector, by setting their
# individual advertised_address.

# Bolt connector
dbms.connector.bolt.enabled=true
#dbms.connector.bolt.tls_level=OPTIONAL
#dbms.connector.bolt.listen_address=:7687

# HTTP Connector. There must be exactly one HTTP connector.
dbms.connector.http.enabled=true
#dbms.connector.http.listen_address=:7474

# HTTPS Connector. There can be zero or one HTTPS connectors.
dbms.connector.https.enabled=true
#dbms.connector.https.listen_address=:7473

# Number of Neo4j worker threads.
#dbms.threads.worker_count=

# apoc setting [scfan] [2018-06-19]
dbms.security.procedures.unrestricted=apoc.*
apoc.import.file.enabled=true

#*****************************************************************
# SSL system configuration
#*****************************************************************

# Names of the SSL policies to be used for the respective components.

# The legacy policy is a special policy which is not defined in
# the policy configuration section, but rather derives from
# dbms.directories.certificates and associated files
# (by default: neo4j.key and neo4j.cert). Its use will be deprecated.

# The policies to be used for connectors.
#
# N.B: Note that a connector must be configured to support/require
#      SSL/TLS for the policy to actually be utilized.
#
# see: dbms.connector.*.tls_level

#bolt.ssl_policy=legacy
#https.ssl_policy=legacy

#*****************************************************************
# SSL policy configuration
#*****************************************************************

# Each policy is configured under a separate namespace, e.g.
#    dbms.ssl.policy.<policyname>.*
#
# The example settings below are for a new policy named 'default'.

# The base directory for cryptographic objects. Each policy will by
# default look for its associated objects (keys, certificates, ...)
# under the base directory.
#
# Every such setting can be overriden using a full path to
# the respective object, but every policy will by default look
# for cryptographic objects in its base location.
#
# Mandatory setting

#dbms.ssl.policy.default.base_directory=certificates/default

# Allows the generation of a fresh private key and a self-signed
# certificate if none are found in the expected locations. It is
# recommended to turn this off again after keys have been generated.
#
# Keys should in general be generated and distributed offline
# by a trusted certificate authority (CA) and not by utilizing
# this mode.

#dbms.ssl.policy.default.allow_key_generation=false

# Enabling this makes it so that this policy ignores the contents
# of the trusted_dir and simply resorts to trusting everything.
#
# Use of this mode is discouraged. It would offer encryption but no security.

#dbms.ssl.policy.default.trust_all=false

# The private key for the default SSL policy. By default a file
# named private.key is expected under the base directory of the policy.
# It is mandatory that a key can be found or generated.

#dbms.ssl.policy.default.private_key=

# The private key for the default SSL policy. By default a file
# named public.crt is expected under the base directory of the policy.
# It is mandatory that a certificate can be found or generated.

#dbms.ssl.policy.default.public_certificate=

# The certificates of trusted parties. By default a directory named
# 'trusted' is expected under the base directory of the policy. It is
# mandatory to create the directory so that it exists, because it cannot
# be auto-created (for security purposes).
#
# To enforce client authentication client_auth must be set to 'require'!

#dbms.ssl.policy.default.trusted_dir=

# Client authentication setting. Values: none, optional, require
# The default is to require client authentication.
#
# Servers are always authenticated unless explicitly overridden
# using the trust_all setting. In a mutual authentication setup this
# should be kept at the default of require and trusted certificates
# must be installed in the trusted_dir.

#dbms.ssl.policy.default.client_auth=require

# A comma-separated list of allowed TLS versions.
# By default TLSv1, TLSv1.1 and TLSv1.2 are allowed.

#dbms.ssl.policy.default.tls_versions=

# A comma-separated list of allowed ciphers.
# The default ciphers are the defaults of the JVM platform.

#dbms.ssl.policy.default.ciphers=

#*****************************************************************
# Logging configuration
#*****************************************************************

# To enable HTTP logging, uncomment this line
#dbms.logs.http.enabled=true

# Number of HTTP logs to keep.
#dbms.logs.http.rotation.keep_number=5

# Size of each HTTP log that is kept.
#dbms.logs.http.rotation.size=20m

# To enable GC Logging, uncomment this line
#dbms.logs.gc.enabled=true

# GC Logging Options
# see http://docs.oracle.com/cd/E19957-01/819-0084-10/pt_tuningjava.html#wp57013 for more information.
#dbms.logs.gc.options=-XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCApplicationStoppedTime -XX:+PrintPromotionFailure -XX:+PrintTenuringDistribution

# Number of GC logs to keep.
#dbms.logs.gc.rotation.keep_number=5

# Size of each GC log that is kept.
#dbms.logs.gc.rotation.size=20m

# Size threshold for rotation of the debug log. If set to zero then no rotation will occur. Accepts a binary suffix "k",
# "m" or "g".
#dbms.logs.debug.rotation.size=20m

# Maximum number of history files for the internal log.
#dbms.logs.debug.rotation.keep_number=7

#*****************************************************************
# Miscellaneous configuration
#*****************************************************************

# Enable this to specify a parser other than the default one.
#cypher.default_language_version=3.0

# Determines if Cypher will allow using file URLs when loading data using
# `LOAD CSV`. Setting this value to `false` will cause Neo4j to fail `LOAD CSV`
# clauses that load data from the file system.
dbms.security.allow_csv_import_from_file_urls=true

# Retention policy for transaction logs needed to perform recovery and backups.
dbms.tx_log.rotation.retention_policy=1 days

# Enable a remote shell server which Neo4j Shell clients can log in to.
#dbms.shell.enabled=true
# The network interface IP the shell will listen on (use 0.0.0.0 for all interfaces).
#dbms.shell.host=127.0.0.1
# The port the shell will listen on, default is 1337.
#dbms.shell.port=1337

# Only allow read operations from this Neo4j instance. This mode still requires
# write access to the directory for lock purposes.
#dbms.read_only=false

# Comma separated list of JAX-RS packages containing JAX-RS resources, one
# package name for each mountpoint. The listed package names will be loaded
# under the mountpoints specified. Uncomment this line to mount the
# org.neo4j.examples.server.unmanaged.HelloWorldResource.java from
# neo4j-server-examples under /examples/unmanaged, resulting in a final URL of
# http://localhost:7474/examples/unmanaged/helloworld/{nodeId}
#dbms.unmanaged_extension_classes=org.neo4j.examples.server.unmanaged=/examples/unmanaged

#********************************************************************
# JVM Parameters
#********************************************************************

# G1GC generally strikes a good balance between throughput and tail
# latency, without too much tuning.
dbms.jvm.additional=-XX:+UseG1GC

# Have common exceptions keep producing stack traces, so they can be
# debugged regardless of how often logs are rotated.
dbms.jvm.additional=-XX:-OmitStackTraceInFastThrow

# Make sure that `initmemory` is not only allocated, but committed to
# the process, before starting the database. This reduces memory
# fragmentation, increasing the effectiveness of transparent huge
# pages. It also reduces the possibility of seeing performance drop
# due to heap-growing GC events, where a decrease in available page
# cache leads to an increase in mean IO response time.
# Try reducing the heap memory, if this flag degrades performance.
dbms.jvm.additional=-XX:+AlwaysPreTouch

# Trust that non-static final fields are really final.
# This allows more optimizations and improves overall performance.
# NOTE: Disable this if you use embedded mode, or have extensions or dependencies that may use reflection or
# serialization to change the value of final fields!
dbms.jvm.additional=-XX:+UnlockExperimentalVMOptions
dbms.jvm.additional=-XX:+TrustFinalNonStaticFields

# Disable explicit garbage collection, which is occasionally invoked by the JDK itself.
dbms.jvm.additional=-XX:+DisableExplicitGC

# Remote JMX monitoring, uncomment and adjust the following lines as needed. Absolute paths to jmx.access and
# jmx.password files are required.
# Also make sure to update the jmx.access and jmx.password files with appropriate permission roles and passwords,
# the shipped configuration contains only a read only role called 'monitor' with password 'Neo4j'.
# For more details, see: http://download.oracle.com/javase/8/docs/technotes/guides/management/agent.html
# On Unix based systems the jmx.password file needs to be owned by the user that will run the server,
# and have permissions set to 0600.
# For details on setting these file permissions on Windows see:
#     http://docs.oracle.com/javase/8/docs/technotes/guides/management/security-windows.html
#dbms.jvm.additional=-Dcom.sun.management.jmxremote.port=3637
#dbms.jvm.additional=-Dcom.sun.management.jmxremote.authenticate=true
#dbms.jvm.additional=-Dcom.sun.management.jmxremote.ssl=false
#dbms.jvm.additional=-Dcom.sun.management.jmxremote.password.file=/absolute/path/to/conf/jmx.password
#dbms.jvm.additional=-Dcom.sun.management.jmxremote.access.file=/absolute/path/to/conf/jmx.access

# Some systems cannot discover host name automatically, and need this line configured:
#dbms.jvm.additional=-Djava.rmi.server.hostname=$THE_NEO4J_SERVER_HOSTNAME

# Expand Diffie Hellman (DH) key size from default 1024 to 2048 for DH-RSA cipher suites used in server TLS handshakes.
# This is to protect the server from any potential passive eavesdropping.
dbms.jvm.additional=-Djdk.tls.ephemeralDHKeySize=2048

# This mitigates a DDoS vector.
dbms.jvm.additional=-Djdk.tls.rejectClientInitiatedRenegotiation=true

#********************************************************************
# Wrapper Windows NT/2000/XP Service Properties
#********************************************************************
# WARNING - Do not modify any of these properties when an application
#  using this configuration file has been installed as a service.
#  Please uninstall the service before modifying this section.  The
#  service can then be reinstalled.

# Name of the service
dbms.windows_service_name=neo4j

#********************************************************************
# Other Neo4j system properties
#********************************************************************
dbms.jvm.additional=-Dunsupported.dbms.udc.source=tarball
```

使用的配置文件

```bash
# 基本和默认配置文件相同，仅修改如下项。其他同原样
dbms.active_database=20190718095032289977.db
dbms.directories.import=import
dbms.memory.heap.initial_size=1024m
dbms.memory.heap.max_size=1024m
dbms.memory.pagecache.size=20g
dbms.connectors.default_listen_address=192.168.100.162
dbms.connectors.default_advertised_address=192.168.100.162
```

## Neo4j语法

Cypher是图形数据库Neo4j的声明式查询语言。

CQL代表Cypher查询语言。 像Oracle数据库具有查询语言SQL，Neo4j具有CQL作为查询语言。

[neo4j入门教程](https://www.w3cschool.cn/neo4j/neo4j_id_property.html)

### Neo4j术语/概念

基础术语/概念



下面介绍下neo4j的几个核心概念：

- Nodes（节点，类似地铁图里的一个地铁站）
图谱的基本单位主要是节点和关系，他们都可以包含属性，一个节点就是一行数据，一个关系也是一行数据，里面的属性就是数据库里面的row里面的字段。
除了属性之外，关系和节点还可以有零到多个标签，标签也可以认为是一个特殊分组方式。

- Relationships（关系，类似两个相邻地铁站之间路线）
关系的功能是组织和连接节点，一个关系连接2个节点，一个开始节点和一个结束节点。当所有的点被连接起来，就形成了一张图谱，通过关系可以组织节点形成任意的结构，比如list，tree，map，tuple，或者更复杂的结构。关系拥有方向进和出，代表一种指向。

- Properties（属性，类似地铁站的名字，位置，大小，进出口数量等）
属性非常类似数据库里面的字段，只有节点和关系可以拥有0到多个属性，属性类型基本和java的数据类型一致，分为 数值，字符串，布尔，以及其他的一些类型，字段名必须是字符串。

- Labels（标签，类似地铁站的属于哪个区）
标签通过形容一种角色或者给节点加上一种类型，一个节点可以有多个类型，通过类型区分一类节点，这样在查询时候可以更加方便和高效，除此之外标签在给属性建立索引或者约束时候也会用到。label名称必须是非空的unicode字符串，另外lables最大标记容量是int的最大值，近似21亿。

- Traversal（遍历，类似我们看地图找路径）
查询时候通常是遍历图谱然后找到路径，在遍历时通常会有一个开始节点，然后根据cpyher提供的查询语句，遍历相关路径上的节点和关系，从而得到最终的结果。

- Paths（路径，类似从一个地铁站到另一个地铁站的所有的到达路径）
路径是一个或多个节点通过关系连接起来的产物，例如得到图谱查询或者遍历的结果。

- Schema（模式，类似存储数据的结构）
neo4j是一个无模式或者less模式的图谱数据库，像mongodb，solr，lucene或者es一样，你可以使用它不需要定义任何schema，

- Indexes（索引）
遍历图通过需要大量的随机读写，如果没有索引，则可能意味着每次都是全图扫描，这样效率非常低下，为了获得更好的性能，我们可以在字段属性上构建索引，这样任何查询操作都会使用索引，从而大幅度提升seek性能，

构建索引是一个异步请求，并不会立刻生效，会再后台创建直至成功后，才能最终生效。如果创建失败，可以重建索引，先删除索引，在创建即可，然后从log里面找出创建失败的原因然后分析。

- Constraints（约束）
约束可以定义在某个字段上，限制字段值唯一，创建约束会自动创建索引。

参考链接:

[Neo4j术语与概念](https://blog.csdn.net/u010454030/article/details/52949031)

### Neo4j运算符

| 运算名称   | 运算符                           |
|--------|-------------------------------------------|
| 常规运算   | DISTINCT, ., []                           |
| 算数运算   | +, -, *, /, %, ^                          |
| 比较运算   | =, <>, <, >, <=, >=, IS NULL, IS NOT NULL |
| 逻辑运算   | AND, OR, XOR, NOT                         |
| 字符串操作  | +                                         |
| List操作 | +, IN, [x], [x .. y]                      |
| 正则操作   | =~                                        |
| 字符串匹配  | STARTS WITH, ENDS WITH, CONTAINS          |

### Cypher语法

```python
# Create 语句

# Create语法
CREATE (<node-name>:<label-name>{<Property1-name>...<Propertyn-name>})
- node-name 节点名称。Neo4j使用。不能使用它来访问节点详细信息
- label-name 标签名称 使用此标签名称来访问节点详细信息。
- Property1-name 属性

# Create 节点+标签 + 属性
CREATE (node_name:label1:label2{id:123,name:"Lokesh",sal:35000,deptno:10})

# Match - 查询指定节点
match (lab:label1)
where lab.name = 'Lokesh'
RETURN lab.name,lab.id
# label1 标签名称
# lab 标签名称重命名。类似 as

# Match - 查询指定节点,创建关系
MATCH (cust:Customer),(cc:CreditCard)
WHERE cust.id = "1001" AND cc.id= "5001"
CREATE (cust)-[r:DO_SHOPPING_WITH{shopdate:"12/12/2014",price:55000}]->(cc) 
RETURN r


# Sort排序 - 对 Match 结果升序或降序排序
MATCH (emp:Employee)
RETURN emp.empid,emp.name,emp.salary,emp.deptno
ORDER BY emp.name DESC

# UNION - 数据合并(字段名称类型必须一致) 不返回重复行

MATCH (cc:CreditCard)
RETURN cc.id as id,cc.number as number,cc.name as name,
   cc.valid_from as valid_from,cc.valid_to as valid_to
UNION
MATCH (dc:DebitCard)
RETURN dc.id as id,dc.number as number,dc.name as name,
   dc.valid_from as valid_from,dc.valid_to as valid_to

# UNION ALL - 数据合并(字段名称类型必须一致) 返回重复行
MATCH (cc:CreditCard)
RETURN cc.id as id,cc.number as number,cc.name as name,
   cc.valid_from as valid_from,cc.valid_to as valid_to
UNION ALL
MATCH (dc:DebitCard)
RETURN dc.id as id,dc.number as number,dc.name as name,
   dc.valid_from as valid_from,dc.valid_to as valid_to

# Limit 过滤或限制查询返回的行数. 去掉CQL查询结果集底部的结果
MATCH (emp:Employee)
RETURN emp
LIMIT 2

# skip 过滤或限制查询返回的行数. 去掉CQL查询结果集顶部的结果
MATCH (emp:Employee)
RETURN emp
SKIP 2

# Merge 合并

Neo4j使用CQL MERGE命令
- 创建节点，关系和属性
- 为从数据库检索数据
- 命令使用：Create+Match组合

MERGE (gp2:GoogleProfile2{ Id: 201402,Name:"Nokia"})


CREATE命令总是向数据库添加新的节点
Merge命令只有在不存在时创建节点。存在时更新


# NULL

Neo4j CQL将空值视为对节点或关系的属性的缺失值或未定义值。

当我们创建一个具有现有节点标签名称但未指定其属性值的节点时，它将创建一个具有NULL属性值的新节点。
# 查看存在 id 属性的节点
MATCH (e:Employee)
WHERE e.id IS NOT NULL
RETURN e.id,e.name,e.sal,e.deptno

# 移除属性
MATCH (n { name: 'Andres' })
SET n.name = NULL RETURN n.name, n.age

# IN 查询集合
MATCH (e:Employee) 
WHERE e.id IN [123,124]
RETURN e.id,e.name,e.sal,e.deptno

```




Cypher删除

- 两种删除方式。DELETE REMOVE
- Delete用于删除节点和关系。Remove用于删除标签和属性。
- Delete和Remove都需要和Match配合使用。

```bash
# 删除节点
MATCH (e: Employee) DELETE e

# 删除节点及关系
MATCH (cc: CreditCard)-[rel]-(c:Customer)
DELETE cc,c,rel

# 删除属性
MATCH (book { id:122 })
REMOVE book.price
RETURN book

# 删除匹配 label1 数据. 标签 label2.
MATCH (m:label1)
REMOVE m:label2
```

Cypher更新

- set方式更新数据。可以和match等配合使用

```bash
# 更新节点属性
MATCH (dc:DebitCard)
SET dc.atm_pin = 3456
RETURN dc

# 移除属性
MATCH (n { name: 'Andres' })
SET n.name = NULL RETURN n.name, n.age


```

ssh

```bash
一，创建节点
1，创建空的节点

CREATE (n)
CREATE (a),(b)
2，创建带标签的节点

CREATE (n:Person)
CREATE (n:Person:Swedish)
3，创建带标签和属性的节点

CREATE (n:Person { name: 'Andres', title: 'Developer' })
二，创建关系
创建节点之前的关系

1，在两个节点之间创建关系

在两个节点之间创建关系，并设置关系类型

MATCH (a:Person),(b:Person)
WHERE a.name = 'A' AND b.name = 'B'
CREATE (a)-[r:RELTYPE]->(b)
RETURN type(r)
2，创建关系，并设置关系的属性

MATCH (a:Person),(b:Person)
WHERE a.name = 'A' AND b.name = 'B'
CREATE (a)-[r:RELTYPE { name: a.name + '<->' + b.name }]->(b)
RETURN type(r), r.name
3，CREATE子句和模式

在CREATE子句和模式中，对于模式中的任意部分，如果它不存在于图中，那么CREATE子句创建它；如果存在于图中，那么就会引用它。

CREATE p =(andres { name:'Andres' })-[:WORKS_AT]->(neo)<-[:WORKS_AT]-(michael { name: 'Michael' })
RETURN p
三，删除节点和关系
使用delete子句删除节点、关系和路径，当删除节点时，该节点必须是孤立的节点，也就是说，必须首先删除跟节点相关的所有关系。

detach delete： 表示删除一个节点或多个节点，跟节点相关的所有关系也都被删除。

1，删除节点

MATCH (n:Person { name: 'UNKNOWN' })
DELETE n
2，删除所有节点和关系

MATCH (n)
DETACH DELETE n
3，删除一个节点和它的所有关系

MATCH (n { name: 'Andres' })
DETACH DELETE n
4，删除关系

MATCH (n { name: 'Andres' })-[r:KNOWS]->()
DELETE r
四，更新属性或标签
set子句用于更新节点的标签，向节点和关系中添加属性

1，向节点或关系中添加属性

MATCH (n { name: 'Andres' })
SET n.surname = 'Taylor'
RETURN n.name, n.surname
2，移除属性

如果设置属性的值是NULL，相当于把该属性从节点或关系中移除

MATCH (n { name: 'Andres' })
SET n.name = NULL RETURN n.name, n.age
3，复制属性

把一个节点的属性复制给另一个节点

MATCH (at { name: 'Andres' }),(pn { name: 'Peter' })
SET at = pn
RETURN at.name, at.age, at.hungry, pn.name, pn.age
4，从Map中添加属性

MATCH (p { name: 'Peter' })
SET p += { hungry: TRUE , position: 'Entrepreneur' }
5，在一条set子句中添加多个属性

MATCH (n { name: 'Andres' })
SET n.position = 'Developer', n.surname = 'Taylor'
6，向节点中添加标签

MATCH (n { name: 'Stefan' })
SET n:German
RETURN n.name, labels(n) AS labels
7，向节点中添加多个标签

MATCH (n { name: 'Emil' })
SET n:Swedish:Bossman
RETURN n.name, labels(n) AS labels
五，移除属性
使用remove子句从节点中移除标签和属性，从关系中移除属性。

1，移除属性

默认情况下，Neo4j不允许存在值为null的属性；如果属性不存在，那么返回该属性的值是null。

MATCH (a { name: 'Andres' })
REMOVE a.age
RETURN a.name, a.age
2，移除节点的标签

MATCH (n { name: 'Peter' })
REMOVE n:German
RETURN n.name, labels(n)
3，移除节点的多个标签

当节点的标签为空时，labels(n)函数返回空的list

MATCH (n { name: 'Peter' })
REMOVE n:German:Swedish
RETURN n.name, labels(n)
六，foreach子句
列表和路径是Cypher中的关键概念，foreach子句用于更新数据，例如，对路径中的元素或通过聚合创建的列表执行更新命令。

1，对路径中的元素执行更新命令

对路径中匹配的所有节点，添加marked属性，并设置属性值为TRUE

MATCH p =(begin)-[*]->(END )
WHERE begin.name = 'A' AND END .name = 'D'
FOREACH (n IN nodes(p)| SET n.marked = TRUE )
```

### Cpyher函数


### Cypher常用语句

查询指定节点

```bash
MATCH (n:cust) where n.id = '623026199412212548' RETURN n LIMIT 25
```

更新指定节点

```bash
MATCH (n:cust) where n.id = '623026199412212548' set n.name='set_name_test' RETURN n LIMIT 25
```

查询节点和边

```bash
match (ee:cust)-[:tran]-(tranx) where ee.address='吉林省东莞市新城哈尔滨街D座 690272' return ee,tranx
```

节点数据导入-loadcsv方式-merge(更新已存在数据)

```bash
USING PERIODIC COMMIT 10000 LOAD CSV WITH HEADERS
            FROM "file:///test.csv" AS line
            fieldterminator ','
            Merge (n:cust{id:line.id})
            set n.name = line.name
# PERIODIC COMMIT 10000 指定每10000条数据提交一次，减小内存压力
# WITH HEADERS 文件自带表头
# fieldterminator 指定文件分隔符
```

创建索引(加快查询，插入速度)

```bash
create index on :cust(id)
create index on :tran(id)
```


## 数据导入

数据导入的几种方式

- Cypher create 语句，为每一条数据写一个create
- Cypher load csv 语句，将数据转成CSV格式，通过LOAD CSV读取数据。
- 官方提供的neo4j-import工具，未来将被neo4j-admin import代替 
- 官方提供的Java API - BatchInserter
- 大牛编写的 batch-import 工具
- neo4j-apoc load.csv + apoc.load.relationship
- 针对实际业务场景，定制化开发

参考链接:

- [海量数据导入Neo4j的几种方式](https://blog.csdn.net/zhanaolu4821/article/details/80820434)
- [Neo4j批量导入数据的几种方式](http://weikeqin.cn/2017/04/14/neo4j-import-data/)
- [使用batch-import工具向neo4j中导入海量数据](https://my.oschina.net/u/2538940/blog/883829)
- [batch-import已经编译好的工具3.0，对应neo4j-3.0.4](https://github.com/mo9527/batch-import-tool)
- [batch-import的github](https://github.com/mo9527/batch-import)
- [batch-import的相关说明](https://github.com/jexp/batch-import/tree/20)

本节主要说明三种导入方式 loadcsv、neo4j-import、batch-import

本文数据导入使用唯一 ID(node)

数据导入的注意事项

- 如果设定唯一主键时，ID必须唯一
- 边中的ID必须存在于节点中，否则关系导入会跳过。

### Neo4j-import

注意事项

#### 文件格式

文件格式样例

```bash
# cust.csv
id:ID,certno,name,label,cust_certtype:string,cust_namespell:string,birthday:int,sex:string,address:string,mob_phone:string
# tran.csv
:START_ID,:END_ID,Type,tran_date:int,amount:int,count:int
```

文件格式说明

- 文件中ID必须唯一

#### 导入命令


```bash
neo4j-import适应场景
neo4j-import参数  (bin/neo4j-import help)
    - 指定最大进程数 --processors <max processor count>
    - 跳过重复节点 --skip-duplicate-nodes <true/false>
    - 跳过异常关系 --skip-bad-relationships <true/false>
    - 最大跳过数量 --bad-tolerance <max number of bad entries, or true for unlimited>
    - 跳过异常行(例如行列数异常) --ignore-extra-columns <true/false>


命令样例:

bin/neo4j-import --bad-tolerance=1000000 --skip-duplicate-nodes=true --skip-bad-relationships=true --into data/databases/graph.db --id-type string --nodes:cust import/c.csv  --relationships:tran import/t.csv

```


### batch-import

注意事项:

- batch-import 不支持多进程调用。
- batch-import版本必须和neo4j版本一致。
  - (否则导致数据库自动升级后虽然正常使用，但是batch-import已经无法读取升级后的数据库了)


#### 文件格式

```bash
# cust.csv
id:string:id_index,certno:string:id_index,name,Label:label,cust_certtype:string,cust_namespell:string,birthday:int,sex:string,address:string,mob_phone:string
874018718864465,874018718864465,鞠瑜,cust,其他证件,juyu,19801010,男,河北省岩市龙潭东莞街d座 188848,15767524738
# tran.csv
id:string:id_index,certno:string:id_index,Type,tran_date:int,amount:int,count:int
874018718864465,411224195908138440,tran,20180108,20,2
```

文件格式说明：

- id:string:id_index ID唯一,指定类型,设置索引


#### 导入命令

```bash
# batch-import命令
sh import.sh /home/fdm/neo4j_test/neo4j-community-3.0.4/data/databases/fdm.db /home/fdm/import_data/c.csv /home/fdm/import_data/t.csv

# batch-import3.0已经编译好的软件包
https://github.com/mo9527/batch-import-tool

# batch.properties配置文件
dump_configuration=false
cache_type=none
use_memory_mapped_buffers=true
neostore.propertystore.db.index.keys.mapped_memory=1000M
neostore.propertystore.db.index.mapped_memory=10M
neostore.nodestore.db.mapped_memory=10240M
neostore.relationshipstore.db.mapped_memory=10240M
neostore.propertystore.db.mapped_memory=5120M
neostore.propertystore.db.strings.mapped_memory=2000M
#batch_import.csv.quotes=true
#batch_import.csv.delim=,workInfoId
#contactRecordId deviceId workInfoId
#batch_array_separator=,

batch_import.csv.quotes=true
batch_import.csv.delim=,
batch_import.keep_db=true
batch_import.node_index.id_index=exact
batch_import.node_index.id_index2=exact
batch_import.node_index.id_index3=exact
```


### Load-csv

#### 文件格式

```bash
load csv 导入格式要求

# cust.csv
id,certno,name,label,cust_certtype,cust_namespell,birthday,sex,address,mob_phone
# tran.csv
start_id,end_id,type,tran_date,amount,count

# create 节点
LOAD CSV WITH HEADERS FROM "file:///cust.csv" AS line create
(p:cust{id:line.id,certno:line.certno,name:line.name,label:line.label,cust_certtype:line.cust_certtype,cust_namespell:line.cust_namespell,birthday:toInteger(line.birthday),sex:line.sex,address:line.address,mob_phone:line.mob_phone})

# 创建索引
CREATE INDEX ON :cust(id)

# create 边
LOAD CSV WITH HEADERS FROM "file:///tran.csv" AS line match
(from:cust{id:line.start_id}),(to:cust{id:line.end_id}) create (from)-[r:tran{ type:line. type,tran_date:line.tran_date,amount:line.amount,count:line.count}]->(to)
```











## 问题记录

### Value 15979221751 is too big to be represented as int

int不支持11位及其以上

### already contains a database

使用neo4j-import时,指定的数据库名称必须不存在,否则会报此错。

### Max 1024 open files allowed, minimum of 40000 recommended.

文件打开数太小。 修改文件 ```/etc/security/limits.conf```

```bash
# 添加如下两行。重新登录 ssh 即可
fdm              soft    nofile          65535
fdm              hard    nofile          65535
```

### 其他情况
  
  csv数据导入失败：可能性有多种

		* 
文件head头不对。  存在节点和交易关系头不对的情况
		* 
节点或交易边数据，ID存在重复。   csv文件中ID必须唯一。且所有实体表中的:ID是必须写的，并且ID 全局唯一，也就是三个表格中的ID都是唯一的，不可以有重复，在关系表中，不可以存在没有ID指向的实体。


## 其他说明

### 参考资源

- [Neo4j语句入门](https://www.w3cschool.cn/neo4j/neo4j_cql_set.html)
- [Neo4j数据导入参考博客](http://weikeqin.com/2017/04/11/neo4j-load-csv/)
- [Python-Neo4j语法](https://neo4j.com/developer/python/)
- [官网Neo4j语法简图](https://neo4j.com/docs/pdf/cypher-refcard-3.3.pdf)

### No4j最大支持节点和关系数量

目前累积统计它有34.4亿个节点，344亿的关系，和6870亿条属性。

### Neo4j数据预热

使用bin/neo4j-shell 进入neo4j命令行界面，执行以下语句预热：

```bash
MATCH (n)
OPTIONAL MATCH (n)-[r]->()
RETURN count(n.prop) + count(r.prop);
```

建立index可以使得查询性能得到巨大提升。如果不建立index，则需要对每个node的每一个属性进行遍历，所以比较慢。 并且index建立之后，新加入的数据都会自动编入到index中。 注意index是建立在label上的，不是在node上，所以一个node有多个label，需要对每一个label都建立index.

### 检查Neo4j是否启动

检查neo4j是否启动,通常10s左右可以启动成功。
[https://neo4j.com/docs/operations-manual/current/configuration/wait-for-start/](https://neo4j.com/docs/operations-manual/current/configuration/wait-for-start/)

### 性能测试

neo4j-import方式

IMPORT DONE in 1m 17s 799ms. Imported:
  7295460 nodes
  10000000 relationships
  112954600 properties

real    1m19.456s
user    5m51.375s
sys    0m15.706s

耗时 79.73S 速度  216,916.30条/s
