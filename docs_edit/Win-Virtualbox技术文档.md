# Win-Virtualbox技术文档.md

tags: 2019年 虚拟机 

## 简介说明



## 功能配置

### 配置非root用户可以访问主机文件

参考链接: [virtualbox+centos下非root用户访问不了共享目录](https://blog.csdn.net/longlongago7777/article/details/100808849)

**问题原因:** 共享目录用户组为 vboxsf,和非root用户属于不同用户组,所以无法访问。

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

## 附件

### 参考链接

### 问题