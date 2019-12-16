# Module-Apache 使用说明

## Apache 简介

> [Apache](http://httpd.apache.org/) 是世界使用排名第一的 Web 服务器软件。它可以运行在几乎所有广泛使用的计算机平台上，由于其跨平台和安全性被广泛使用，是最流行的 Web 服务器端软件之一。它快速、可靠并且可通过简单的 API 扩充，将 Perl/Python 等解释器编译到服务器中。同时 Apache 音译为阿帕奇，是北美印第安人的一个部落，叫阿帕奇族，在美国的西南部。也是一个基金会的名称、一种武装直升机等等. [百度百科 Apache](https://baike.baidu.com/item/apache/6265)

**Apacheweb 服务器软件拥有以下特性：**

- 1.支持最新的 HTTP/1.1 通信协议
- 2.拥有简单而强有力的基于文件的配置过程
- 3.支持通用网关接口
- 4.支持基于 IP 和基于域名的虚拟主机
- 5.支持多种方式的 HTTP 认证
- 6.集成 Perl 处理模块
- 7.集成代理服务器模块
- 8.支持实时监视服务器状态和定制服务器日志
- 9.支持服务器端包含指令(SSI)
- 10.支持安全 Socket 层(SSL)
- 11.提供用户会话过程的跟踪
- 12.支持 FastCGI
- 13.通过第三方模块可以支持 JavaServlets

## Apache 功能

TODO Apache 功能 后置,暂无需求

### Apache 参数详解

参考链接: [centos7 部署 Apache 服务器](https://blog.csdn.net/loveer0/article/details/82498851)

## 附件

### Centos7-Apache 配置示例

**步骤 1 配置 scfan.conf 配置文件:**

```conf
# /etc/httpd/conf.d/scfan.conf
User scfan
Group scfan

<VirtualHost *:80>
    DocumentRoot "/home/scfan/project/FISAMS/branches/branch_scfan/src/web/fdm"
    <Directory "/home/scfan/project/FISAMS/branches/branch_scfan/src/web/fdm">
        options Indexes MultiViews
        AllowOverride all
        Allow from all
    </Directory>
</VirtualHost>
```

**步骤 2 重命名 welcome.conf:**

```bash
# 重命名后不会再显示 testing 123 而是会显示详细报错
mv  /etc/httpd/conf.d/welcome.conf /etc/httpd/conf.d/welcome.conf.bak
```

**步骤 3 重启服务:**

```bash
/bin/systemctl restart httpd.service
```

报错: [StackOverFlow - You don't have permission to access / on this server.](https://stackoverflow.com/questions/10873295/error-message-forbidden-you-dont-have-permission-to-access-on-this-server),后续步骤已解决此问题,此处可供参考

**步骤 4 目录授权:**

```bash
# 采用单层授权, 避免整个目录文件都权限被变更
[root@fdm conf]# chmod +x  /home/scfan/project/FISAMS/branches/branch_scfan/src/web/fdm
[root@fdm conf]# chmod +x  /home/scfan/project/FISAMS/branches/branch_scfan/src/web/
[root@fdm conf]# chmod +x  /home/scfan/project/FISAMS/branches/branch_scfan/src/
[root@fdm conf]# chmod +x  /home/scfan/project/FISAMS/branches/branch_scfan/
[root@fdm conf]# chmod +x  /home/scfan/project/FISAMS/branches/
[root@fdm conf]# chmod +x  /home/scfan/project/FISAMS/
[root@fdm conf]# chmod +x  /home/scfan/project
[root@fdm conf]# chmod +x  /home/scfan
[root@fdm conf]# chmod +x  /home
```

**步骤 5 修改 配置文件 /etc/httpd/conf/httpd.conf:**

```conf
# 配置监听端口 对应 scfan.conf 配置文件
41 #Listen 12.34.56.78:80
42 Listen 80
43 Listen 8888
44 LimitRequestLine 40940  # 限制 Apache 请求长度,根据实际需要增加

# 注释如下代码
105 # <Directory />
106 #     AllowOverride none
107 #     Require all denied
108 # </Directory>
```

**步骤 6 重启服务:**

```bash
/bin/systemctl restart httpd.service
```

### Apache 测试页面

**Apache 测试页意味着:**

Apache 测试页，意味着您的服务器已正确配置并可以使用。从技术上讲，此页面是首次安装 Apache Web 服务器时的默认索引页面。

**那么如何使 Apache 测试页消失呢:**

只需打开`/var/www/index.html` 文件并对其进行修改或删除文件（尽管它可能会触发新的错误）。在 `Red Hat Enterprise Linux/CentOS/Fedora Core` 下，重命名或删除文件`/etc/httpd/conf.d/welcome.conf` 以确保您没有看到 Apache 测试页。

您现在可以将内容添加到目录`/var/www/html/`中。请注意，在您这样做之前，访问您网站的用户将看到默认页面，而不是您的内容。要防止使用此页面，请遵循文件`/etc/httpd/conf.d/welcome.conf` 中的说明。

## Apache 问题记录

### Apache has not been designed to serve pages while running as root

**问题说明:**

root 用户下无法启动 httpd 服务

**日志信息:**

```bash
[root@cf8d90d17e9a ~]# systemctl status httpd.service
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
   Active: failed (Result: exit-code) since Mon 2019-12-16 02:06:58 UTC; 25s ago
     Docs: man:httpd(8)
           man:apachectl(8)
  Process: 9553 ExecStop=/bin/kill -WINCH ${MAINPID} (code=exited, status=1/FAILURE)
  Process: 9552 ExecStart=/usr/sbin/httpd $OPTIONS -DFOREGROUND (code=exited, status=1/FAILURE)
 Main PID: 9552 (code=exited, status=1/FAILURE)

Dec 16 02:06:58 cf8d90d17e9a systemd[1]: Starting The Apache HTTP Server...
Dec 16 02:06:58 cf8d90d17e9a httpd[9552]: AH00526: Syntax error on line 1 of /etc/httpd/conf.d/fdm.conf:
Dec 16 02:06:58 cf8d90d17e9a httpd[9552]: Error:\tApache has not been designed to serve pages while\n\trunning as root.  There are known ...
Dec 16 02:06:58 cf8d90d17e9a systemd[1]: httpd.service: main process exited, code=exited, status=1/FAILURE
Dec 16 02:06:58 cf8d90d17e9a kill[9553]: kill: cannot find process ""
Dec 16 02:06:58 cf8d90d17e9a systemd[1]: httpd.service: control process exited, code=exited status=1
Dec 16 02:06:58 cf8d90d17e9a systemd[1]: Failed to start The Apache HTTP Server.
Dec 16 02:06:58 cf8d90d17e9a systemd[1]: Unit httpd.service entered failed state.
Dec 16 02:06:58 cf8d90d17e9a systemd[1]: httpd.service failed.
```

**解决方法:**

用于 `/etc/httpd/conf.d/fdm.conf` 配置中 User 和 Group 不能为`root`,修改为其他用户即可

```bash
User fdm
Group fdm
<VirtualHost *:80>
    DocumentRoot /home/fdm/web/fdm
    <Directory /home/fdm/web/fdm>
        options Indexes MultiViews
        AllowOverride all
        Allow from all
    </Directory>
</VirtualHost>
```

### Forbidden You don't have permission to access xxx.html

**问题说明:**

文件权限不足

**解决方法 1:**

```bash
# 一层层授权
chmod +x /dira
chmod +x /dira/dirb/
chmod +x /dira/dirb/index.html
# 或者 直接 chmod 777 -R /dira/dirb/index.html
```

**解决方法 2:**

修改配置文件`/etc/httpd/conf/httpd.conf`

```bash
DocumentRoot "/home/fdm/web/fdm"
```

**解决方法 3:**
修改配置文件`/etc/httpd/conf/httpd.conf`

```conf
# 注释如下代码
105 # <Directory />
106 #     AllowOverride none
107 #     Require all denied
108 # </Directory>
```

以上情况,不同问题解决方法不同,可以叠加使用。

## Apache 注意事项

### 参考资源

使用 & 简单配置 & 复杂配置 & 参数详解 & 相关说明

- [Centos7 配置 Apache 实现 HTTPS](https://blog.51cto.com/13043516/2300167)
- [Centos7 下配置 Apache 的虚拟主机](https://www.cnblogs.com/jxc321/p/8490446.html)
- [CentOS 7 Apache 服务的安装与配置](https://www.cnblogs.com/fisherpau/p/11375874.html)
- [centos7 上搭建 http 服务器以及设置目录访问](https://www.cnblogs.com/snake553/p/8856729.html)
