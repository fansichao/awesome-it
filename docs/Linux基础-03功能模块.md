# Linux-03 功能模块

## 功能模

### 删除乱码文件 tips

步骤 1：**查看文件的 num**

```bash
ls -li
```

步骤 2：**查看确定文件**

```bash
find . -inum 1490945
```

步骤 3： **删除指定文件**

```bash
find . -inum 1490945 -exec rm {} -rf \;
```

![Linux功能模块-删除乱码文件.png](https://raw.githubusercontent.com/fansichao/awesome-it/master/images/20191129130808.png)
