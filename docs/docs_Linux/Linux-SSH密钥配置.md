# Linux-SSH 使用说明

[toc]

## 简介

SSH(远程连接工具)连接原理：ssh 服务是一个守护进程(demon)，系统后台监听客户端的连接，ssh 服务端的进程名为 sshd,负责实时监听客户端的请求(IP 22 端口)，包括公共秘钥等交换等信息。ssh 服务端由 2 部分组成： openssh(提供 ssh 服务)    openssl(提供加密的程序)ssh 的客户端可以用 XSHELL，Securecrt, Mobaxterm 等工具进行连接

## 功能模块-配置 SSH 免密码登录

```bash
配置1：ssh免密钥登录设置
客户端配置 – 服务器1
1.查看~/.ssh文件夹,若已经存在有公钥文件(id_rsa.pub),私钥文件(id_rsa),则可以跳过客户端配置.
2.生成密钥文件.
$ ssh-keygen
然后一路回车.
然后~/.ssh下会生成id_rsa.pub和id_rsa, 其中id_rsa文件起到唯一标识你的客户机的作用.
注意:不要改这两个文件的文件名,ssh登陆时会读取id_rsa文件.
# 服务器配置 – 服务器2
1.修改sshd配置文件(/etc/ssh/sshd_config).
找到以下内容，并去掉注释符”#“
=========================
　　RSAAuthentication yes
　　PubkeyAuthentication yes
　　AuthorizedKeysFile  .ssh/authorized_keys
=========================
2.配置authorized_keys文件.
若’~/.ssh/authorized_keys’不存在,则建立.ssh文件夹和authorized_keys文件.
将上文中客户机id_rsa.pub的内容拷贝到authorized_keys中.
注意:
1) .ssh目录的权限必须是700
2) .ssh/authorized_keys文件权限必须是600
3.重启sshd.
$ /etc/init.d/sshd restart  # 非必需
# 测试
客户机执行:ssh -v user@host (-v 调试模式)
会显示一些登陆信息.

# 关键命令
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
/etc/init.d/sshd restart # 非必需
```

## 功能模块-只允许密钥登录(禁用密码登录)

为了服务器主机安全，需要设定密钥登录，并且指定 root 不可远程登录。

[toc]

### 步骤 1：生成客户端密钥

生成密钥方式有如下两种：

- Linux 主机
- Win 主机-Xshell 软件

### 步骤 2：添加密钥到服务端

将 id_rsa.pub 中内容复制到 `~/.ssh/authorized_keys`

### 步骤 3：修改服务端配置文件

配置文件修改后生效，需要重启服务
配置文件：`/etc/ssh/sshd_config`
重启服务：`service sshd restart` 或 `/bin/systemctl restart sshd.service`

开启密钥登录

```bash
RSAAuthentication yes # 启用 RSA 认证  # 非必需修改，不存在时不创建不修改。
PubkeyAuthentication yes # 启用公钥私钥配对认证方式
```

禁止 root 远程登录

```bash
PermitRootLogin yes # 禁止 root 远程登录
```

关闭密码登陆方式

```bash
PasswordAuthentication no
ChallengeResponseAuthentication no
```

修改完成后重启服务

```bash
/bin/systemctl restart sshd.service
```

## SSH 配置文件

**常用配置项说明:**

```bash

```

**SSH 客户端配置文件：** `/etc/ssh/ssh_config`

```bash
[root@WOM ~]# cat  /etc/ssh/ssh_config
#   $OpenBSD: ssh_config,v 1.25 2009/02/17 01:28:32 djm Exp $

# This is the ssh client system-wide configuration file.  See
# ssh_config(5) for more information.  This file provides defaults for
# users, and the values can be changed in per-user configuration files
# or on the command line.

# Configuration data is parsed as follows:
#  1. command line options
#  2. user-specific file
#  3. system-wide file
# Any configuration value is only changed the first time it is set.
# Thus, host-specific definitions should be at the beginning of the
# configuration file, and defaults at the end.

# Site-wide defaults for some commonly used options.  For a comprehensive
# list of available options, their meanings and defaults, please see the
# ssh_config(5) man page.

# Host *
#   ForwardAgent no
#   ForwardX11 no
#   RhostsRSAAuthentication no
#   RSAAuthentication yes
#   PasswordAuthentication yes
#   HostbasedAuthentication no
#   GSSAPIAuthentication no
#   GSSAPIDelegateCredentials no
#   GSSAPIKeyExchange no
#   GSSAPITrustDNS no
#   BatchMode no
#   CheckHostIP yes
#   AddressFamily any
#   ConnectTimeout 0
#   StrictHostKeyChecking ask
#   IdentityFile ~/.ssh/identity
#   IdentityFile ~/.ssh/id_rsa
#   IdentityFile ~/.ssh/id_dsa
#   Port 22
#   Protocol 2,1
#   Cipher 3des
#   Ciphers aes128-ctr,aes192-ctr,aes256-ctr,arcfour256,arcfour128,aes128-cbc,3des-cbc
#   MACs hmac-md5,hmac-sha1,umac-64@openssh.com,hmac-ripemd160
#   EscapeChar ~
#   Tunnel no
#   TunnelDevice any:any
#   PermitLocalCommand no
#   VisualHostKey no
Host *
    GSSAPIAuthentication yes
# If this option is set to yes then remote X11 clients will have full access
# to the original X11 display. As virtually no X11 client supports the untrusted
# mode correctly we set this to yes.
    ForwardX11Trusted yes
# Send locale-related environment variables
    SendEnv LANG LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE LC_MONETARY LC_MESSAGES
    SendEnv LC_PAPER LC_NAME LC_ADDRESS LC_TELEPHONE LC_MEASUREMENT
    SendEnv LC_IDENTIFICATION LC_ALL LANGUAGE
    SendEnv XMODIFIERS
```

**SSH 服务端配置文件：** `/etc/ssh/sshd_config`

```bash
[root@WOM ~]# cat  /etc/ssh/sshd_config
#   $OpenBSD: sshd_config,v 1.80 2008/07/02 02:24:18 djm Exp $

# This is the sshd server system-wide configuration file.  See
# sshd_config(5) for more information.

# This sshd was compiled with PATH=/usr/local/bin:/bin:/usr/bin

# The strategy used for options in the default sshd_config shipped with
# OpenSSH is to specify options with their default value where
# possible, but leave them commented.  Uncommented options change a
# default value.

#Port 22
#AddressFamily any
#ListenAddress 0.0.0.0
#ListenAddress ::

# Disable legacy (protocol version 1) support in the server for new
# installations. In future the default will change to require explicit
# activation of protocol 1
Protocol 2

# HostKey for protocol version 1
#HostKey /etc/ssh/ssh_host_key
# HostKeys for protocol version 2
#HostKey /etc/ssh/ssh_host_rsa_key
#HostKey /etc/ssh/ssh_host_dsa_key

# Lifetime and size of ephemeral version 1 server key
#KeyRegenerationInterval 1h
#ServerKeyBits 1024

# Logging
# obsoletes QuietMode and FascistLogging
#SyslogFacility AUTH
SyslogFacility AUTHPRIV
#LogLevel INFO

# Authentication:

#LoginGraceTime 2m
#PermitRootLogin yes
#StrictModes yes
#MaxAuthTries 6
#MaxSessions 10

#RSAAuthentication yes
#PubkeyAuthentication yes
#AuthorizedKeysFile .ssh/authorized_keys
#AuthorizedKeysCommand none
#AuthorizedKeysCommandRunAs nobody

# For this to work you will also need host keys in /etc/ssh/ssh_known_hosts
#RhostsRSAAuthentication no
# similar for protocol version 2
#HostbasedAuthentication no
# Change to yes if you don't trust ~/.ssh/known_hosts for
# RhostsRSAAuthentication and HostbasedAuthentication
#IgnoreUserKnownHosts no
# Don't read the user's ~/.rhosts and ~/.shosts files
#IgnoreRhosts yes

# To disable tunneled clear text passwords, change to no here!
#PasswordAuthentication no
#PermitEmptyPasswords no
PasswordAuthentication yes

# Change to no to disable s/key passwords
#ChallengeResponseAuthentication yes
ChallengeResponseAuthentication no

# Kerberos options
#KerberosAuthentication no
#KerberosOrLocalPasswd yes
#KerberosTicketCleanup yes
#KerberosGetAFSToken no
#KerberosUseKuserok yes

# GSSAPI options
#GSSAPIAuthentication no
GSSAPIAuthentication yes
#GSSAPICleanupCredentials yes
GSSAPICleanupCredentials yes
#GSSAPIStrictAcceptorCheck yes
#GSSAPIKeyExchange no

# Set this to 'yes' to enable PAM authentication, account processing,
# and session processing. If this is enabled, PAM authentication will
# be allowed through the ChallengeResponseAuthentication and
# PasswordAuthentication.  Depending on your PAM configuration,
# PAM authentication via ChallengeResponseAuthentication may bypass
# the setting of "PermitRootLogin without-password".
# If you just want the PAM account and session checks to run without
# PAM authentication, then enable this but set PasswordAuthentication
# and ChallengeResponseAuthentication to 'no'.
#UsePAM no
UsePAM yes

# Accept locale-related environment variables
AcceptEnv LANG LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE LC_MONETARY LC_MESSAGES
AcceptEnv LC_PAPER LC_NAME LC_ADDRESS LC_TELEPHONE LC_MEASUREMENT
AcceptEnv LC_IDENTIFICATION LC_ALL LANGUAGE
AcceptEnv XMODIFIERS

#AllowAgentForwarding yes
#AllowTcpForwarding yes
#GatewayPorts no
#X11Forwarding no
X11Forwarding yes
#X11DisplayOffset 10
#X11UseLocalhost yes
#PrintMotd yes
#PrintLastLog yes
#TCPKeepAlive yes
#UseLogin no
#UsePrivilegeSeparation yes
#PermitUserEnvironment no
#Compression delayed
#ClientAliveInterval 0
#ClientAliveCountMax 3
#ShowPatchLevel no
#UseDNS yes
#PidFile /var/run/sshd.pid
#MaxStartups 10:30:100
#PermitTunnel no
#ChrootDirectory none

# no default banner path
#Banner none

# override default of no subsystems
Subsystem   sftp    /usr/libexec/openssh/sftp-server

# Example of overriding settings on a per-user basis
#Match User anoncvs
#   X11Forwarding no
#   AllowTcpForwarding no
#   ForceCommand cvs server
```

## Resources

参考链接：

- Linux 实现密钥登陆： [https://www.cnblogs.com/gsxx/p/4447390.html](https://www.cnblogs.com/gsxx/p/4447390.html)
- Linux ssh 命令详解： [https://www.cnblogs.com/ftl1012/p/ssh.html](https://www.cnblogs.com/ftl1012/p/ssh.html)
- Linux：SSH 服务配置文件详解： [https://www.cnblogs.com/Spiro-K/p/6685943.html](https://www.cnblogs.com/ftl1012/p/ssh.html)
