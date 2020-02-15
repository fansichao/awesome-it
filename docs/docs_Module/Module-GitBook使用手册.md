# GitBook 使用手册

[toc]

## 简单使用流程

TODO

## 命令大全

```bash
# 初始化目录文件
gitbook init
# 列出gitbook所有的命令
gitbook help
# 输出gitbook-cli的帮助信息
gitbook --help
# 生成静态网页
gitbook build
# 生成静态网页并运行服务器
gitbook serve
# 生成时指定gitbook的版本, 本地没有会先下载
gitbook build --gitbook=2.0.1
# 列出本地所有的gitbook版本
gitbook ls
# 列出远程可用的gitbook版本
gitbook ls-remote
# 安装对应的gitbook版本
gitbook fetch 标签/版本号
# 更新到gitbook的最新版本
gitbook update
# 卸载对应的gitbook版本
gitbook uninstall 2.0.1
# 指定log的级别
gitbook build --log=debug
# 输出错误信息
gitbook builid --debug
```

# 参考资源

链接：
https://blog.csdn.net/axi295309066/article/details/61420694/
