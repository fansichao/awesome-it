# ScyllaDB 技术文档.md

## 简介说明

由于 scylladb 数据库本身就是基于 cassandra 的"优化版"。

> [ScyllaDB](https://www.scylladb.com/) 是用 C++ 重写的 Cassandra，每节点每秒处理 100 万 TPS。ScyllaDB 完全兼容 Apache Cassandra，拥有比 Cassandra 多 10x 倍的吞吐量，降低了延迟。 ScyllaDB 是性能优异的 NoSQL 列存储数据库。 ScyllaDB 在垃圾收集或者 Compaction 的时候不需要暂停；在常规生产负载的时候可以添加和删除节点。

**ScyllaDB_结构图**
![ScyllaDB_结构图](https://1bpezptkft73xxds029zrs59-wpengine.netdna-ssl.com/wp-content/uploads/network-diagram.png)

**Cassandra结构图**
![Cassandra结构图](https://img-blog.csdnimg.cn/20191016165735499.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzIxMTY1MDA3,size_16,color_FFFFFF,t_70)

### 功能支持

ScyllaDB官网号称

- 实时大数据数据库: 每个节点的向上扩展性能为1,000,000s OPS，可横向扩展到数百个节点，并且99％的延迟小于1毫秒
- 最快的NoSQL数据库
- 最快的分布式数据库
- 适用于最苛刻应用程序的真正NoSQL数据库

[ScyllaDB官网文档](https://docs.scylladb.com/)

### 优缺点

[ScyllDB优缺点](https://blog.csdn.net/nosqlnotes/article/details/79491256)

优点:

- **低而一致的延迟**: 无锁实现和独立的内存管理堆栈消除了对JVM或Linux页面缓存的低效率依赖，从而提供了一致的低延迟。
- **永远在线**: 跨多个节点和数据中心的自动故障转移和复制可实现可靠的容错能力。
- **吞吐量提高10倍**: 用C ++编写，可压缩硬件的每一性能，并允许每个节点最多进行1,000,000次读/写操作
- **高度可扩展**: 自动分片，同类服务器和本地多数据中心实施可实现无缝的线性扩展，而不会影响应用程序的停机时间或性能。
- **易于使用**: Apache Cassandra的有线协议，丰富的驱动程序以及与Spark，Presto和Graph工具的集成，可实现资源高效且性能高效的编码。
- **社区支持**: 从第一天开始，Scylla就成为一个开源数据库，得到了越来越多的贡献者社区的支持。
- **解决压实，流化和修复**: 工作负载调节提供了一系列动态调度算法，以最大程度地减少数据库操作延迟抖动并减少压缩流和修复时间。
- **最佳总拥有成本**: C ++框架提高了效率，可以捕获比现有基础结构高10倍的吞吐量，从而创建了强大而高效的NoSQL数据库。
- **自动调节**: 全自动和动态的数据库调整可有效管理内部资源，需要零配置，并立即提高性能。

缺点:

- 多副本之间数据不一致时经常需要手动修复来搞定
- 虽然ScyllaDB能够充分的利用底层硬件的IOPS，但长时间运行后的Compaction带来的冗余IOPS消耗.



### 术语说明

https://blog.csdn.net/mytobaby00/article/details/80375196



### 同类软件综合对比

## 安装部署

环境依赖

- CentOS7.3+ 64位机器
- Yum已经配置完毕
- 需要Root用户或者Sudo权限
- **确认所有端口已打开**

当前环境

- CentOS7.5
- 非Root用户
- 已关闭SeLinux、防火墙

[官网安装链接](https://docs.scylladb.com/getting-started/)

### 安装ScyllaDB

```bash
# >>>>>>>>> 安装 ScyllaDB
yum install -y sudo
# 卸载 abrt。 abrt 会和 ScyllaDB 冲突
sudo yum remove -y abrt
# 配置yum源
sudo yum install epel-release -y
sudo curl -o /etc/yum.repos.d/scylla.repo -L http://repositories.scylladb.com/scylla/repo/uuidValue/centos/scylladb-3.0.repo
# 安装最新版本
sudo yum install scylla -y
# sudo yum install scylla-3.0.6 -y # 安装指定版本
```

### 配置ScyllaDB

参考链接: [官网ScyllaDB群集配置](https://docs.scylladb.com/operating-scylla/procedures/cluster-management/create_cluster_multidc/)

配置文件

```bash
/etc/scylla/scylla.yaml
```

- cluster_name  集群的名称，集群中的所有节点必须具有相同的名称
- seeds     种子节点在启动过程中用于引导八卦过程并加入集群
- listen_address    Scylla用于连接到集群中其他Scylla节点的IP地址
- rpc_address   客户端连接接口的IP地址（Thrift，CQL）

修改指定IP

```conf
seed_provider:
    - class_name: org.apache.cassandra.locator.SimpleSeedProvider
      parameters:
          # seeds is actually a comma-delimited list of addresses.
          # Ex: "<ip1>,<ip2>,<ip3>"
          - seeds: "192.168.172.72"

listen_address: 192.168.172.72
rpc_address: 192.168.172.72
```

### Scylla设置 & 启动命令

```bash
# 前置依赖
pip install PyYAML
pip install cqlsh
```

- 运行scylla_setup脚本以调整系统设置 ```sudo scylla_setup```

scylla_setup详细内容

```bash
[root@c7c57188b482 software]# scylla_setup
Skip any of the following steps by answering 'no'
Do you want to run check your kernel version?
Yes - runs a  script to verify that the kernel for this instance qualifies to run Scylla. No - skips the kernel check.
[YES/no]YES
INFO  2019-10-15 01:35:59,324 [shard 0] iotune - /var/tmp/mnt passed sanity checks
This is a supported kernel version.
Do you want to verify the ScyllaDB packages are installed?
Yes - runs a script to confirm that ScyllaDB is installed. No - skips the installation check.
[YES/no]YES
Do you want the Scylla server service to automatically start when the Scylla node boots?
Yes - Scylla server service automatically starts on Scylla node boot. No - skips this step. Note you will have to start the Scylla Server service manually.
[YES/no]yes
Do you want to disable SELinux?
Yes - disables SELinux. Choosing Yes greatly improves performance. No - keeps SELinux activated.
[YES/no]yes
Traceback (most recent call last):
  File "/usr/lib/scylla/scylla_selinux_setup", line 36, in <module>
    res = out('sestatus')
  File "/usr/lib/scylla/scylla_util.py", line 280, in out
    return subprocess.check_output(cmd, shell=shell).strip().decode('utf-8')
  File "/usr/lib64/python3.6/subprocess.py", line 356, in check_output
    **kwargs).stdout
  File "/usr/lib64/python3.6/subprocess.py", line 423, in run
    with Popen(*popenargs, **kwargs) as process:
  File "/usr/lib64/python3.6/subprocess.py", line 729, in __init__
    restore_signals, start_new_session)
  File "/usr/lib64/python3.6/subprocess.py", line 1364, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'sestatus': 'sestatus'
SELinux setup failed. Press any key to continue...

Do you want to setup Network Time Protocol(NTP) to auto-synchronize the current time on the node?
Yes - enables time-synchronization. This keeps the correct time on the node. No - skips this step.
[YES/no]yes
Failed to set locale, defaulting to C
Loaded plugins: fastestmirror, ovl
Loading mirror speeds from cached hostfile
 * base: ap.stykers.moe
 * epel: hkg.mirror.rackspace.com
 * extras: mirrors.163.com
 * updates: ap.stykers.moe
Package ntp-4.2.6p5-29.el7.centos.x86_64 already installed and latest version
Package ntpdate-4.2.6p5-29.el7.centos.x86_64 already installed and latest version
Nothing to do
15 Oct 01:36:45 ntpdate[5717]: adjust time server 5.79.108.34 offset 0.015830 sec
Do you want to setup RAID0 and XFS?
It is recommended to use RAID0 and XFS for Scylla data. If you select yes, you will be prompted to choose the unmounted disks to use for Scylla data. Selected disks are formatted as part of the process.
Yes - choose a disk/disks to format and setup for RAID0 and XFS. No - skip this step.
[YES/no]no
Do you want to enable coredumps?
Yes - sets up coredump to allow a post-mortem analysis of the Scylla state just prior to a crash. No - skips this step.
[YES/no]yes
kernel.core_pattern = |/usr/lib/systemd/systemd-coredump %p %u %g %s %t %e"
Do you want to setup a system-wide customized configuration for Scylla?
Yes - setup the sysconfig file. No - skips this step.
[YES/no]yes
Do you want to enable Network Interface Card (NIC) and disk(s) optimization?
Yes - optimize the NIC queue and disks settings. Selecting Yes greatly improves performance. No - skip this step.
[YES/no]yes
ERROR: 'disks' tuning was requested but no disks were found. Your system can't be tuned until the issue is fixed.
Traceback (most recent call last):
  File "/usr/lib/scylla/scylla_sysconfig_setup", line 75, in <module>
    rps_cpus = out('{} --tune net --nic {} --get-cpu-mask'.format(perftune_base_command(), ifname))
  File "/usr/lib/scylla/scylla_util.py", line 280, in out
    return subprocess.check_output(cmd, shell=shell).strip().decode('utf-8')
  File "/usr/lib64/python3.6/subprocess.py", line 356, in check_output
    **kwargs).stdout
  File "/usr/lib64/python3.6/subprocess.py", line 438, in run
    output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['/usr/lib/scylla/perftune.py', '--tune', 'disks', '--dir', '/var/lib/scylla/data', '--dir', '/var/lib/scylla/commitlog', '--tune', 'net', '--nic', 'eth0', '--get-cpu-mask']' returned non-zero exit status 1.
NIC queue setup failed. Press any key to continue...

Do you want iotune to study your disks IO profile and adapt Scylla to it?
Yes - let iotune study my disk(s). Note that this action will take a few minutes. No - skip this step.
[YES/no]yes
Do you want to install node exporter to export Prometheus data from the node? Note that the Scylla monitoring stack uses this data
Yes - install node exporter. No - skip this  step.
[YES/no]yes
node_exporter already installed
node exporter setup failed. Press any key to continue...

Do you want to set the CPU scaling governor to Performance level on boot?
Yes - sets the CPU scaling governor to performance level. No - skip this step.
[YES/no]yes
Failed to set locale, defaulting to C
Loaded plugins: fastestmirror, ovl
Loading mirror speeds from cached hostfile
 * base: ap.stykers.moe
 * epel: hkg.mirror.rackspace.com
 * extras: mirrors.163.com
 * updates: ap.stykers.moe
Package kernel-tools-3.10.0-1062.1.2.el7.x86_64 already installed and latest version
Nothing to do
Do you want to enable fstrim service?
Yes - runs fstrim on your SSD. No - skip this step.
[YES/no]yes
ScyllaDB setup finished.
Please restart your machine before using ScyllaDB, as you have disabled
 SELinux.
```

- 启动服务 ```sudo systemctl start scylla-server```

- 运行nodetool ```nodetool status```

```bash
/usr/bin/filter_cassandra_attributes.py:10: YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated, as the default Loader is unsafe. Please read https://msg.pyyaml.org/load for full details.
  attributes.update(load(open(sys.argv[i], 'r')))
Datacenter: datacenter1
=======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address    Load       Tokens       Owns (effective)  Host ID                               Rack
UN  127.0.0.1  217.36 KiB  256          100.0%            d0d39d92-2974-4893-bd36-495391cac39b  rack1
```

- 运行cqlsh ```cqlsh --cqlversion=3.3.1 192.168.172.72```

```bash
(env) [scfan@scfan scyllaDB]$ cqlsh --cqlversion=3.3.1 192.168.172.72
Connected to  at 192.168.172.72:9042.
[cqlsh 5.0.1 | Cassandra 3.0.8 | CQL spec 3.3.1 | Native protocol v4]
Use HELP for help.
cqlsh>
cqlsh>
```

运行cassandra-stress

```bash
cassandra-stress write -mode cql3 native
```

### Scylla Monitoring(可选,建议安装)

![Scylla Monitoring可视化界面](https://docs.scylladb.com/_images/monitor3.png)

## 附件

### 问题记录

#### No module named yaml

pip install PyYAML

#### No module named cqlshlib

pip install cqlsh

#### cannot import name cqlshhandling

```bash
(env) [scfan@scfan scyllaDB]$ find /usr/lib/ -name cqlshlib
/usr/lib/python2.7/site-packages/cqlshlib
(env) [scfan@scfan scyllaDB]$ export PYTHONPATH=/usr/lib/python2.7/site-packages/

将如下加入到文件 /etc/profile 中
# Scylla
export PYTHONPATH=/usr/lib/python2.7/site-packages/
# 使其生效
source /etc/profile
```

#### Unable to connect to any servers

```bash
(env) [scfan@scfan scyllaDB]$ cqlsh
Connection error: ('Unable to connect to any servers', {'192.168.172.72:9042': ProtocolError("cql_version '3.0.10' is not supported by remote (w/ native protocol). Supported versions: [u'3.3.1']",)})
```

解决方法

```bash
# cqlsh --cqlversion=x.x.x host 指定版本和主机IP
cqlsh --cqlversion=3.3.1 192.168.172.72
```

#### No nodes present in the cluster

```bash
[root@c7c57188b482 software]# nodetool status
/usr/bin/filter_cassandra_attributes.py:10: YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated, as the default Loader is unsafe. Please read https://msg.pyyaml.org/load for full details.
  attributes.update(load(open(sys.argv[i], 'r')))
nodetool: Scylla API server HTTP GET to URL '/storage_service/ownership/' failed: runtime error: No nodes present in the cluster. Has this node finished starting up?
See 'nodetool help' or 'nodetool help <command>'.
```

#### setting up system keyspace

重启后经常报错如下:

TODO 原因未知..........

```bash
[root@d276413151a0 graph_data]# systemctl status scylla-server.service -l 
● scylla-server.service - Scylla Server
   Loaded: loaded (/usr/lib/systemd/system/scylla-server.service; enabled; vendor preset: disabled)
  Drop-In: /etc/systemd/system/scylla-server.service.d
           └─capabilities.conf
   Active: failed (Result: exit-code) since 二 2019-10-15 09:12:10 UTC; 6s ago
  Process: 7020 ExecStopPost=/usr/lib/scylla/scylla_stop (code=exited, status=0/SUCCESS)
  Process: 6942 ExecStart=/usr/bin/scylla $SCYLLA_ARGS $SEASTAR_IO $DEV_MODE $CPUSET (code=exited, status=1/FAILURE)
  Process: 6941 ExecStartPre=/usr/lib/scylla/scylla_prepare (code=exited, status=0/SUCCESS)
 Main PID: 6942 (code=exited, status=1/FAILURE)
   Status: "setting up system keyspace"

10月 15 09:12:10 d276413151a0 scylla[6942]:  [shard 22] compaction_manager - Asked to stop
10月 15 09:12:10 d276413151a0 scylla[6942]:  [shard 12] compaction_manager - Asked to stop
10月 15 09:12:10 d276413151a0 scylla[6942]:  [shard 4] compaction_manager - Asked to stop
10月 15 09:12:10 d276413151a0 scylla[6942]:  [shard 18] compaction_manager - Asked to stop
10月 15 09:12:10 d276413151a0 scylla[6942]:  [shard 19] compaction_manager - Asked to stop
10月 15 09:12:10 d276413151a0 scylla[6942]:  [shard 16] compaction_manager - Asked to stop
10月 15 09:12:10 d276413151a0 systemd[1]: scylla-server.service: main process exited, code=exited, status=1/FAILURE
10月 15 09:12:10 d276413151a0 systemd[1]: Failed to start Scylla Server.
10月 15 09:12:10 d276413151a0 systemd[1]: Unit scylla-server.service entered failed state.
10月 15 09:12:10 d276413151a0 systemd[1]: scylla-server.service failed.
```

### 安装日志

```bash
[root@15b1fad0dfef java_install]# scylla_setup
Skip any of the following steps by answering 'no'
Do you want to run check your kernel version?
Yes - runs a  script to verify that the kernel for this instance qualifies to run Scylla. No - skips the kernel check.
[YES/no]YES  
INFO  2019-10-12 01:33:43,496 [shard 0] iotune - /var/tmp/mnt passed sanity checks
This is a supported kernel version.
Do you want to verify the ScyllaDB packages are installed?
Yes - runs a script to confirm that ScyllaDB is installed. No - skips the installation check.
[YES/no]YES
Do you want the Scylla server service to automatically start when the Scylla node boots?
Yes - Scylla server service automatically starts on Scylla node boot. No - skips this step. Note you will have to start the Scylla Server service manually.
[YES/no]YES
Created symlink from /etc/systemd/system/multi-user.target.wants/scylla-server.service to /usr/lib/systemd/system/scylla-server.service.
/bin/sh: sudo: command not found
Do you want to disable SELinux?
Yes - disables SELinux. Choosing Yes greatly improves performance. No - keeps SELinux activated.
[YES/no]YES
Traceback (most recent call last):
  File "/usr/lib/scylla/scylla_selinux_setup", line 36, in <module>
    res = out('sestatus')
  File "/usr/lib/scylla/scylla_util.py", line 280, in out
    return subprocess.check_output(cmd, shell=shell).strip().decode('utf-8')
  File "/usr/lib64/python3.6/subprocess.py", line 356, in check_output
    **kwargs).stdout
  File "/usr/lib64/python3.6/subprocess.py", line 423, in run
    with Popen(*popenargs, **kwargs) as process:
  File "/usr/lib64/python3.6/subprocess.py", line 729, in __init__
    restore_signals, start_new_session)
  File "/usr/lib64/python3.6/subprocess.py", line 1364, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'sestatus': 'sestatus'
SELinux setup failed. Press any key to continue...

Do you want to setup Network Time Protocol(NTP) to auto-synchronize the current time on the node?
Yes - enables time-synchronization. This keeps the correct time on the node. No - skips this step.
[YES/no]YES
Failed to set locale, defaulting to C
Loaded plugins: fastestmirror, ovl
Loading mirror speeds from cached hostfile
 * base: mirrors.163.com
 * epel: hk.mirrors.thegigabit.com
 * extras: ap.stykers.moe
 * updates: ap.stykers.moe
Resolving Dependencies
--> Running transaction check
---> Package ntp.x86_64 0:4.2.6p5-29.el7.centos will be installed
--> Processing Dependency: libopts.so.25()(64bit) for package: ntp-4.2.6p5-29.el7.centos.x86_64
---> Package ntpdate.x86_64 0:4.2.6p5-29.el7.centos will be installed
--> Running transaction check
---> Package autogen-libopts.x86_64 0:5.18-5.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

==================================================================================================
 Package                   Arch             Version                          Repository      Size
==================================================================================================
Installing:
 ntp                       x86_64           4.2.6p5-29.el7.centos            base           548 k
 ntpdate                   x86_64           4.2.6p5-29.el7.centos            base            86 k
Installing for dependencies:
 autogen-libopts           x86_64           5.18-5.el7                       base            66 k

Transaction Summary
==================================================================================================
Install  2 Packages (+1 Dependent package)

Total download size: 701 k
Installed size: 1.6 M
Downloading packages:
(1/3): ntpdate-4.2.6p5-29.el7.centos.x86_64.rpm                            |  86 kB  00:00:00
(2/3): ntp-4.2.6p5-29.el7.centos.x86_64.rpm                                | 548 kB  00:00:00
(3/3): autogen-libopts-5.18-5.el7.x86_64.rpm                               |  66 kB  00:00:14
--------------------------------------------------------------------------------------------------
Total                                                              47 kB/s | 701 kB  00:00:14
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : autogen-libopts-5.18-5.el7.x86_64                                              1/3
  Installing : ntpdate-4.2.6p5-29.el7.centos.x86_64                                           2/3
  Installing : ntp-4.2.6p5-29.el7.centos.x86_64                                               3/3
  Verifying  : ntp-4.2.6p5-29.el7.centos.x86_64                                               1/3
  Verifying  : ntpdate-4.2.6p5-29.el7.centos.x86_64                                           2/3
  Verifying  : autogen-libopts-5.18-5.el7.x86_64                                              3/3

Installed:
  ntp.x86_64 0:4.2.6p5-29.el7.centos            ntpdate.x86_64 0:4.2.6p5-29.el7.centos

Dependency Installed:
  autogen-libopts.x86_64 0:5.18-5.el7

Complete!
12 Oct 01:38:44 ntpdate[13000]: adjust time server 116.203.151.74 offset -0.083053 sec
Created symlink from /etc/systemd/system/multi-user.target.wants/ntpd.service to /usr/lib/systemd/system/ntpd.service.
Do you want to setup RAID0 and XFS?
It is recommended to use RAID0 and XFS for Scylla data. If you select yes, you will be prompted to choose the unmounted disks to use for Scylla data. Selected disks are formatted as part of the process.
Yes - choose a disk/disks to format and setup for RAID0 and XFS. No - skip this step.
[YES/no]No
Do you want to enable coredumps?
Yes - sets up coredump to allow a post-mortem analysis of the Scylla state just prior to a crash. No - skips this step.
[YES/no]Yes
kernel.core_pattern = |/usr/lib/systemd/systemd-coredump %p %u %g %s %t %e"
Do you want to setup a system-wide customized configuration for Scylla?
Yes - setup the sysconfig file. No - skips this step.
[YES/no]Yes
Do you want to enable Network Interface Card (NIC) and disk(s) optimization?
Yes - optimize the NIC queue and disks settings. Selecting Yes greatly improves performance. No - skip this step.
[YES/no]Y
ERROR: 'disks' tuning was requested but no disks were found. Your system can't be tuned until the issue is fixed.
Traceback (most recent call last):
  File "/usr/lib/scylla/scylla_sysconfig_setup", line 75, in <module>
    rps_cpus = out('{} --tune net --nic {} --get-cpu-mask'.format(perftune_base_command(), ifname))
  File "/usr/lib/scylla/scylla_util.py", line 280, in out
    return subprocess.check_output(cmd, shell=shell).strip().decode('utf-8')
  File "/usr/lib64/python3.6/subprocess.py", line 356, in check_output
    **kwargs).stdout
  File "/usr/lib64/python3.6/subprocess.py", line 438, in run
    output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['/usr/lib/scylla/perftune.py', '--tune', 'disks', '--dir', '/var/lib/scylla/data', '--dir', '/var/lib/scylla/commitlog', '--tune', 'net', '--nic', 'eth0', '--get-cpu-mask']' returned non-zero exit status 1.
NIC queue setup failed. Press any key to continue...

Do you want iotune to study your disks IO profile and adapt Scylla to it?
Yes - let iotune study my disk(s). Note that this action will take a few minutes. No - skip this step.
[YES/no]Y
tuning /sys/dev/block/0:99
ERROR 2019-10-12 01:42:39,980 [shard 0] iotune - Exception when qualifying filesystem at /var/lib/scylla/data
ERROR:root:/var/lib/scylla/data did not pass validation tests, it may not be on XFS and/or has limited disk space.
This is a non-supported setup, and performance is expected to be very bad.
For better performance, placing your data on XFS-formatted directories is required.
To override this error, enable developer mode as follow:
sudo /usr/lib/scylla/scylla_dev_mode_setup --developer-mode 1
IO configuration setup failed. Press any key to continue...

Do you want to install node exporter to export Prometheus data from the node? Note that the Scylla monitoring stack uses this data
Yes - install node exporter. No - skip this  step.
[YES/no]Y


Created symlink from /etc/systemd/system/multi-user.target.wants/node-exporter.service to /usr/lib/systemd/system/node-exporter.service.
node_exporter successfully installed
Do you want to set the CPU scaling governor to Performance level on boot?
Yes - sets the CPU scaling governor to performance level. No - skip this step.
[YES/no]Failed to set locale, defaulting to C
Loaded plugins: fastestmirror, ovl
Loading mirror speeds from cached hostfile
 * base: mirrors.163.com
 * epel: mirror01.idc.hinet.net
 * extras: ap.stykers.moe
 * updates: ap.stykers.moe
Resolving Dependencies
--> Running transaction check
---> Package kernel-tools.x86_64 0:3.10.0-1062.1.2.el7 will be installed
--> Processing Dependency: kernel-tools-libs = 3.10.0-1062.1.2.el7 for package: kernel-tools-3.10.0-1062.1.2.el7.x86_64
--> Processing Dependency: libcpupower.so.0()(64bit) for package: kernel-tools-3.10.0-1062.1.2.el7.x86_64
--> Running transaction check
---> Package kernel-tools-libs.x86_64 0:3.10.0-1062.1.2.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

==================================================================================================
 Package                    Arch            Version                        Repository        Size
==================================================================================================
Installing:
 kernel-tools               x86_64          3.10.0-1062.1.2.el7            updates          7.8 M
Installing for dependencies:
 kernel-tools-libs          x86_64          3.10.0-1062.1.2.el7            updates          7.7 M

Transaction Summary
==================================================================================================
Install  1 Package (+1 Dependent package)

Total download size: 16 M
Installed size: 310 k
Downloading packages:
(1/2): kernel-tools-libs-3.10.0-1062.1.2.el7.x86_64.rpm                    | 7.7 MB  00:00:03
kernel-tools-3.10.0-1062.1.2.e FAILED
http://centos.ustc.edu.cn/centos/7.7.1908/updates/x86_64/Packages/kernel-tools-3.10.0-1062.1.2.el7.x86_64.rpm: [Errno 12] Timeout on http://centos.ustc.edu.cn/centos/7.7.1908/updates/x86_64/Packages/kernel-tools-3.10.0-1062.1.2.el7.x86_64.rpm: (28, 'Operation too slow. Less than 1000 bytes/sec transferred the last 30 seconds')
Trying other mirror.
(2/2): kernel-tools-3.10.0-1062.1.2.el7.x86_64.rpm                         | 7.8 MB  00:00:03
--------------------------------------------------------------------------------------------------
Total                                                             472 kB/s |  16 MB  00:00:33
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : kernel-tools-libs-3.10.0-1062.1.2.el7.x86_64                                   1/2
  Installing : kernel-tools-3.10.0-1062.1.2.el7.x86_64                                        2/2
  Verifying  : kernel-tools-3.10.0-1062.1.2.el7.x86_64                                        1/2
  Verifying  : kernel-tools-libs-3.10.0-1062.1.2.el7.x86_64                                   2/2

Installed:
  kernel-tools.x86_64 0:3.10.0-1062.1.2.el7

Dependency Installed:
  kernel-tools-libs.x86_64 0:3.10.0-1062.1.2.el7

Complete!
Created symlink from /etc/systemd/system/multi-user.target.wants/cpupower.service to /usr/lib/systemd/system/cpupower.service.
Do you want to enable fstrim service?
Yes - runs fstrim on your SSD. No - skip this step.
[YES/no]ScyllaDB setup finished.
Please restart your machine before using ScyllaDB, as you have disabled
 SELinux.
```
