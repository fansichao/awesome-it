# Win-Virtualbox 技术文档.md

tags: 虚拟机 Virtualbox 2019 年 11 月

## 简介说明

[VirtualBox](https://www.virtualbox.org/) 号称是最强的免费虚拟机软件，它不仅具有丰富的特色，而且性能也很优异！它简单易用，可虚拟的系统包括 Windows（从 Windows 3.1 到 Windows10、Windows Server 2012，所有的 Windows 系统都支持）、Mac OS X、Linux、OpenBSD、Solaris、IBM OS2 甚至 Android 等操作系统！使用者可以在 VirtualBox 上安装并且运行上述的这些操作系统！ 与同性质的 VMware 及 Virtual PC 比较下，VirtualBox 独到之处包括远端桌面协定（RDP）、iSCSI 及 USB 的支持，VirtualBox 在客户端操作系统上已可以支持 USB 2.0 的硬件装置，不过要安装 VirtualBox Extension Pack。

**注意事项:**

- Win 命令,路径加双引号.(避免特殊字符的影响)

## Virtualbox 常用命令

参考链接:

- [VirtualBox 简用命令汇总](https://blog.csdn.net/achang21/article/details/18413811)
- [VBoxManage 常用命令用法](http://xcx1024.com/ArtInfo/143262.html)

```bash
# >>>>>>>>>>>>>> 格式转换 <<<<<<<<<<<<<<<<
# 格式转换 VDI转VMDK
VBoxManage clonehd "source.vdi" "target.vmdk" --format VMDK
# 格式转换 VMDK转VDI
VBoxManage clonehd "source.vmdk" "target.vdi" --format VDI

# >>>>>>>>>>>>>> 查看信息 <<<<<<<<<<<<<<<<
# 查看有哪些虚拟机
VBoxManage list vms
# 查看虚拟的详细信息
VBoxManage list vms --long
# 查看运行着的虚拟机
VBoxManage list runningvms
# 列出VirtualBox当前正在使用的虚拟磁盘的信息
VBoxManage list hdds
# 列出虚拟机配置文件中加载的虚拟磁盘镜像的信息
VBoxManage list dvds

# 列出VirtualBox所能识别的所有客户机操作系统
VBoxManage list ostypes
# 显示主机的Hardware time、CPU、内存、操作系统及系统版本信息
VBoxManage list hostinfo # (输出中的"Processor count"指的是CPU的线程数)
# 列出所有VirtualBox支持的虚拟磁盘后端
VBoxManage list hddbackends
# 显示VirtualBox的一些全局设置信息，包括Guest Additions文件的路径
VBoxManage list systemproperties
# 显示虚拟机的配置信息
VBoxManage showvminfo <uuid>|<name>
# 详细显示虚拟机的配置信息
VBoxManage showvminfo <uuid>|<name> [--details]




# >>>>>>>>>>>>>> 开启 <<<<<<<<<<<<<<<<
# 开启虚拟机在后台运行
VBoxManage startvm backup -type headless
# 开启虚拟机并开启远程桌面连接的支持
VBoxManage startvm <vm_name> -type vrdp

# 改变虚拟机的远程连接端口,用于多个vbox虚拟机同时运行
VBoxManage controlvm <vm_name> vrdpprot <ports>

# >>>>>>>>>>>>>> 关闭 <<<<<<<<<<<<<<<<
# 关闭虚拟机
VBoxManage controlvm <vm_name> acpipowerbutton
# 强制关闭虚拟机
VBoxManage controlvm <vm_name> poweroff

# >>>>>>>>>>>>>> 快照 <<<<<<<<<<<<<<<<
# 为名为centos7创建一张叫base的快照
VBoxManage snapshot "centos7" take base
# 为虚拟机centos7删除名为base的快照
VBoxManage snapshot "centos7" delete base

# >>>>>>>>>>>>>> 扩展包 <<<<<<<<<<<<<<<<
# 增加一个新的扩展包
VBoxManage extpack install <.vbox-extpack>
# 卸载指定扩展包
VBoxManage extpack uninstall <name>
# 显示已安装的扩展包
VBoxManage list extpacks
# 移除安装扩展包失败或卸载扩展包失败时可能遗留下来的文件和目录
VBoxManage extpack cleanup
```

## 功能配置

### 配置非 root 用户可以访问主机文件

参考链接: [virtualbox+centos 下非 root 用户访问不了共享目录](https://blog.csdn.net/longlongago7777/article/details/100808849)

**问题原因:** 共享目录用户组为 vboxsf,和非 root 用户属于不同用户组,所以无法访问。

**解决方法**:

```bash
# 1. root用户下
usermod -a -G wheel userName
# 2.当前用户下
sudo usermod -aG vboxsf $(whoami)
# 3. 重启或注销用户
su - $(whoami)
# 即可正常查看主机文件
```

### 动态磁盘和固定磁盘互相转换

参考链接: [Virtualbox 固定磁盘和动态磁盘之间进行转换](https://www.helplib.com/Linux/article_13912)

前置说明:

- 虚拟机已关机且备份(导出 OVA 格式等)

**将动态磁盘转为固定磁盘**实际操作步骤

```bash
# 切换目录
[C:\~]$ cd C:\Program Files\Oracle\VirtualBox
[C:\Program Files\Oracle\VirtualBox]$
# 列出当前硬盘信息
[C:\Program Files\Oracle\VirtualBox]$  VBoxManage.exe list hdds
UUID:           782ec60c-da8e-4308-994c-fff7e8e3594d
Parent UUID:    base
State:          locked write
Type:           normal (base)
Location:       D:\10-软件数据\Virtualbox\CentOS7.5_My HugeGraph\CentOS7.5_My HugeGraph-disk001.vmdk
Storage format: VMDK
Capacity:       204800 MBytes
Encryption:     disabled
# 将固定磁盘转换为动态磁盘
[C:\Program Files\Oracle\VirtualBox]$ VBoxManage.exe clonemedium disk "D:\10-软件数据\Virtualbox\CentOS7.5_My HugeGraph\CentOS7.5_My HugeGraph-disk001.vmdk" "D:\10-软件数据\Virtualbox\CentOS7.5_My HugeGraph\Centos75.vdi" -variant Standard
0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
Clone medium created in format 'VMDK'. UUID: 38a0c1d3-cc6f-427c-8dc4-fb33a50a0b24
# 将动态磁盘转为固定磁盘
# [C:\Program Files\Oracle\VirtualBox]$ VBoxManage.exe clonemedium disk "D:\10-软件数据\Virtualbox\CentOS7.5_My HugeGraph\CentOS7.5_My HugeGraph-disk001.vmdk" "D:\10-软件数据\Virtualbox\CentOS7.5_My HugeGraph\Centos75_fixed.vdi" -variant Fixed
# 0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
# Clone medium created in format 'VMDK'. UUID: 4f4952d3-6754-4267-8ffa-0e06f12d1449
# 列出当前硬盘信息
[C:\Program Files\Oracle\VirtualBox]$ VBoxManage.exe list hdds
UUID:           782ec60c-da8e-4308-994c-fff7e8e3594d
Parent UUID:    base
State:          created
Type:           normal (base)
Location:       D:\10-软件数据\Virtualbox\CentOS7.5_My HugeGraph\CentOS7.5_My HugeGraph-disk001.vmdk
Storage format: VMDK
Capacity:       204800 MBytes
Encryption:     disabled

UUID:           4f4952d3-6754-4267-8ffa-0e06f12d1449
Parent UUID:    base
State:          created
Type:           normal (base)
Location:       D:\10-软件数据\Virtualbox\CentOS7.5_My HugeGraph\Centos75_fixed.vdi
Storage format: VMDK
Capacity:       204800 MBytes
Encryption:     disabled
```

断开虚拟机和原有硬盘的关联,然后 添加新硬盘
![20191220_Virtualbox_删除硬盘01.png](https://raw.githubusercontent.com/fansichao/images/master/markdown/20191220_Virtualbox_%E5%88%A0%E9%99%A4%E7%A1%AC%E7%9B%9801.png)

删除原有硬盘(可以点击查看硬盘,会显示硬盘是否分配,未分配的硬盘根据需要可以对应删除掉)
![20191220_Virtualbox_删除硬盘02.png](https://raw.githubusercontent.com/fansichao/images/master/markdown/20191220_Virtualbox_%E5%88%A0%E9%99%A4%E7%A1%AC%E7%9B%9802.png)()

### Virtualbox 硬盘扩容

### Virtualbox 硬盘压缩

[虚拟机硬盘 vmdk 压缩瘦身并挂载到 VirtualBox](https://www.jianshu.com/p/3ed6e8ad5d05)

## 附件

### 参考链接

### 问题

### Virtualbox 虚拟机网络缓慢-解决方法

背景说明:

- 问题原因: 服务器项目运行缓慢，服务器网络缓慢。
- 网络配置: 三网卡配置 仅主机 host+nat 网络+桥接网卡

步骤 1：查看网络延迟

```bash
# 正常应该是0.1s内
(env) [scfan@fdm ~]$ time curl -s http://www.baidu.com > /dev/null
real 0m5.608s
user 0m0.004s
sys 0m0.004s
```

步骤 2: 参阅文档

参考资源: [VirtualBox 虚拟机里网络很慢的解决方法](https://pylist.com/t/1555072754)

发现可能是由于 DNS 问题导致的。

步骤 3：修改 Virtualbox 参数

```bash
# 先关闭虚拟机

# 修改 natdnshostresolver & natdnsproxy 参数
C:\Windows\system32>cd C:\Program Files\Oracle\VirtualBox
C:\Program Files\Oracle\VirtualBox>  VBoxManage modifyvm "CentOS7.5_My HugeGraph" --natdnshostresolver1 on
C:\Program Files\Oracle\VirtualBox>  VBoxManage modifyvm "CentOS7.5_My HugeGraph" --natdnsproxy1 on
```

步骤 4：重启虚拟机后发现并没有修复问题

```bash
[root@fdm network-scripts]#  time curl -s http://www.baidu.com > /dev/null

real 0m5.616s
user 0m0.001s
sys	0m0.005s
```

步骤 5：配置 DNS

```bash
# 查看 /etc/resolv.conf 文件 
[root@fdm network-scripts]# cat /etc/resolv.conf
# Generated by NetworkManager
search DHCP
nameserver 192.168.100.58
nameserver 192.168.1.1
nameserver 192.168.0.1
# NOTE: the libc resolver may not support more than 3 nameservers.
# The nameservers listed below may not be recognized.
nameserver 114.114.114.114
nameserver 192.168.172.2
```

TODO 发现 192.168.100.58 一般网络下无法访问，导致网络延迟高，删除后正常 偶发 未解决
 

参考链接 ：[CentOS 7 下，如何设置DNS服务器](https://blog.csdn.net/l1028386804/article/details/79850698) 

```bash
# 临时修改
[root@fdm ~]# cat /etc/resolv.conf
# Generated by NetworkManager
search DHCP
# nameserver 192.168.100.58
# nameserver 192.168.172.2
# nameserver 114.114.114.114
# nameserver 192.168.1.1
# nameserver 192.168.0.1
# NOTE: the libc resolver may not support more than 3 nameservers.
# The nameservers listed below may not be recognized.


修改 /etc/NetworkManager/NetworkManager.conf 添加。禁止从NetworkManager自动覆盖resolv.conf文件
[main]
#plugins=ifcfg-rh,ibft
dns=none


[root@fdm network-scripts]# time curl -s http://www.baidu.com > /dev/null
real	0m0.009s
user	0m0.004s
sys	0m0.002s
···
