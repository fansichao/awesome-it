# Linux-03 功能模块

## 功能模

### 删除乱码文件 tips

步骤 1：**查看文件的 num**

```bash
ls -li
```

步骤 2：**查看确定文件**

```bash
# 避免误删其他文件
find . -inum 1490945
```

步骤 3： **删除指定文件**

```bash
find . -inum 1490945 -exec rm {} -rf \;
```

![Linux功能模块-删除乱码文件.png](https://raw.githubusercontent.com/fansichao/awesome-it/master/images/20191129130808.png)

## 问题记录

### Linux 关机或重启时提示 A stop job is running for

Linux 关机或重启时提示 A stop job is running for .. 导致关机慢。

修改方法

```bash
vim /etc/systemd/system.conf
修改下面两个变量为：
DefaultTimeoutStartSec=10s
DefaultTimeoutStopSec=10s
# 执行命令
systemctl daemon-reload
```

