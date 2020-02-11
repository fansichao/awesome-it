# VNC 使用手册

远程登录图形化界面。

[toc]

## 安装 VNC

VNC 服务，可以用于远程登录图形化界面。

```bash
1.安装vnc相关包
rpm –ivh  tigervnc-server-1.1.0-24.el6.x86_64.rpm
yum install vnc
yum install vnc-server
yum install tigervnc-server

# 检查安装包是否已经安装
rpm -qa | grep vnc

vnc-server-4.1.2-14.el5_3.1
vnc-4.1.2-14.el5_3.1

2. 配置vncservers文件
# vim /etc/sysconfig/vncservers 增加如下两行
VNCSERVERS="1:oracle"                      设置登录“显示号”和用户
VNCSERVERARGS[1]="-geometry 1024x768"    设置屏幕分辨率
3.配置xstartup文件
编辑配置之前，需要使用vncserver命令创建默认配置文件
[root@web~]# vncserver
输入口令：qwe123
确认口令：qwe123
                            # vim /root/.vnc/xstartup 加入最后一行
                            gnome-session & set starting GNOME desktop （增加这一行，表使用gnome界面，否则是xfce界面）
                   4. 设置远程登录口令
[root@web~]# vncpasswd
Password:qwe123
Verifu:qwe123
5.启动vncserver服务
（1）主服务启动：
[root@web~]# service vncserver start （只启动/etc/sysconfig/vncservers 所定义的界面）
[root@web~]# vncserver  :2  （启动root登录的第二个界面）
6.停止vncserver服务
[root@web~]# service vncserver stop（停止start时候所启动的界面:1，其它另启的界面:2不停止）
[root@web~]# vncserver -kill :1  （停止某个界面，要用kill命令来杀掉界面1的进程）
[root@web~]# vncserver -kill :2  （停止某个界面，要用kill命令来杀掉界面2的进程）
通过 #service vncserver status 命令可以查看出有多少个进程pid号，表示启动了多少个界面。
7.让vncserver服务随机启动
默认状态下，vncserver服务不是开机自动启动，需要手工启动。
[root@web~]# chkconfig --list vncserver
[root@web~]# chkconfig vncserver on
保存后，重启测试。
8.客户端登录vncserver服务
（1）先安装vncviewer来远程登录，
（2）然后在地址栏输入“主机地址:1”（即主机IP加界面号的方式）

# 重启VNC服务
vncserver -kill :1
vncserver :1
```

### 关闭防火墙

需要关闭防火墙，或者配置相应的端口

VNC 服务使用的端口号与桌面号相关，VNC 使用 TCP 端口从 5900 开始，对应关系如下：
桌面号为“1” ---- 端口号为 5901
桌面号为“2” ---- 端口号为 5902
桌面号为“3” ---- 端口号为 5903
……
基于 Java 的 VNC 客户程序 Web 服务 TCP 端口从 5800 开始，也是与桌面号相关，对应关系如下
桌面号为“1” ---- 端口号为 5801
桌面号为“2” ---- 端口号为 5802
桌面号为“3” ---- 端口号为 5803
……
基于上面的介绍，如果 Linux 开启了防火墙功能，就需要手工开启相应的端口，以开启桌面号为“1”相应的端口为例，命令如下

## 登录 vnc

Server 输入 IP:1

vnc viewer 客户端界面登录(192.168.1.70:1)：
![Software_VNC](https://github.com/fansichao/file/raw/master/picture/Software_VNC001.png)

vnc viewer 客户端界面登录 输入密码(qwe123)：
![Software_VNC](https://github.com/fansichao/file/raw/master/picture/Software_VNC002.png)

vnc viewer 客户端界面登录 登录后界面：
**github 路径 blob->raw 才可以使用 github 图片**
![Software_VNC](https://github.com/fansichao/file/raw/master/picture/Software_VNC003.png)
