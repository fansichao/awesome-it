# 1. Visual Studio Code 软件使用大全 Windows

tags: Win Vscode IDE 工具 2018 年

Visual Studio Code，初用，不断完善中......

## 1.1. 软件介绍

## 1.2. 软件下载&安装

[Visual Studio Code](https://code.visualstudio.com/Download)
[Visual Studio Code 官方文档](https://code.visualstudio.com/docs)

## 1.3. 小技巧

### 1.3.1. 修改语言为中文

步骤一: 在扩展中添加 中文简体语言包

![在这里插入图片描述](https://img-blog.csdnimg.cn/20181120173149450.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzIxMTY1MDA3,size_16,color_FFFFFF,t_70)

**步骤二**: 打开配置文件

点击快捷键`ctrl+shift+p`，输入 `Configure Display Language`
![在这里插入图片描述](https://img-blog.csdnimg.cn/20181120173515295.png)

**步骤三**: 修改配置文件

修改成如图所示即可`"locale":"zh-cn"`。
保存`ctrl+s`，重启 vscode 软件即可生效。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20181120173612808.png)

### 1.3.2. 打开用户设置

**步骤一:** 打开设置
文件 -> 首选项 -> 设置

**步骤二:** 打开用户设置文件

输入 settings，点击"在 settings.json 中编辑"即可进入用户设置。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20181121085624513.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzIxMTY1MDA3,size_16,color_FFFFFF,t_70)

### 1.3.3. 修改用户配置文件

当前使用配置

```python
{
    "python.linting.pylintEnabled": true,
    "python.pythonPath": "C:\\Users\\scfan\\Anaconda2\\python.exe",
    "C_Cpp.errorSquiggles": "Disabled",
    "remote.onstartup": true,
    "fileheader.customMade": {
        "Author": "Scfan",
        "Date": "Do not edit",
        "LastEditors": "Scfan",
        "LastEditTime": "Do not edit",
        "Description": "工作&学习&生活",
        "Email": "643566992@qq.com",
        "Company": "上海",
        "version": "V1.0",
    },
    "workbench.iconTheme": "vscode-icons",
    "workbench.colorTheme": "Visual Studio Dark",
    "files.autoSave": "afterDelay",
    "terminal.integrated.shell.windows": "C:\\WINDOWS\\System32\\cmd.exe",
    "python.autoComplete.extraPaths": ["C:/Users/scfan/AppData/Local/Programs/Python/Python37/python3", "C:/Users/scfan/Anaconda2"],
    "python.jediEnabled": false,
    "editor.tabCompletion": "onlySnippets",
    "emmet.triggerExpansionOnTab": true,
    "editor.fontSize": 16,
}
```

## 1.4. 常用命令

### 1.4.1. 基础界面命令

- ctrl+y 取消撤销
- ctrl+sheif+f 全局搜索文件，搜索所有文件中内容

## 1.5. 详细插件使用

Vscode 插件市场:

- [https://marketplace.visualstudio.com](https://marketplace.visualstudio.com)

### 1.5.1. 插件快捷键

简单列出如下插件的常用快捷键。

- koroFileHeader
  - `ctrl+alt+t`: 当前位置，生成函数注释。
  - `ctrl+alt+i`: 光标位置，生成头部注释。

### 1.5.2. vscode-icons(图标显示)

根据文件类型显示对应图标。
![在这里插入图片描述](https://img-blog.csdnimg.cn/2018112017423218.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzIxMTY1MDA3,size_16,color_FFFFFF,t_70)

### 1.5.3. koroFileHeader(自定义注释模板)

**使用说明**:

- settings.json 自定义注释模板
- `ctrl+alt+t`: 当前位置，生成函数注释。
- `ctrl+alt+i`: 光标位置，生成头部注释。

### 1.5.4. Markdown Preview Enhanced(MarkDown 使用软件)

**使用说明**:

- 参考链接: [markdown-preview-enhanced](https://shd101wyy.github.io/markdown-preview-enhanced/#/)

![Markdown Preview Enhanced(MarkDown使用软件)](https://user-images.githubusercontent.com/1908863/28227953-eb6eefa4-68a1-11e7-8769-96ea83facf3b.png)

### 1.5.5. AutoFileName(文件路径自动补全)

### 1.5.6. Sort Lines(代码行排序插件)

选择要排序的行，按 F1 键排序并选择所需的排序。常规排序具有默认热键 F9。

![Sort Lines(代码行排序插件)2](https://github.com/Tyriar/vscode-sort-lines/raw/master/images/usage-animation.gif)

### 1.5.7. Git History

以图表的形式查看 git 日志
![Git History](https://upload-images.jianshu.io/upload_images/4804567-08e039a3cc452782.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
git 存储库，方便文件备份。

**步骤一:** 配置关联到 github 仓库

pass ,详见网上
参考链接: [https://blog.csdn.net/lhb_11/article/details/77837078](https://blog.csdn.net/lhb_11/article/details/77837078)

**步骤二:** vscode 中 git 使用

- `ctrl+shift+p`命令快捷键，输入 git，有全部提交选项
- Vscode 侧边栏有文件修改未提交提示
- 暂存修改、放弃修改等，全部提交等
- 提交后,将本地修改 push 到 git 库上

```bash
git push -u origin master
```

- 右上角按钮, git history 可以查看当前文件的修改日志。

### 1.5.8. GitLen 版本库

显示文件最近的 commit 和作者，显示当前行 commit 信息
![GitLen版本库](https://upload-images.jianshu.io/upload_images/4804567-9144297c7a2ad208.gif?imageMogr2/auto-orient/strip)

### 1.5.9. MarkDown TOC 目录

- 使用:
  - 安装插件`MarkDown TOC`
  - 在 MarkDown 文件中右键
    - MarkDown Sections:Delete 删除目录序号
    - MarkDown Sections: Insert\Update 增加目录序号
    - MarkDown Toc:Delete 删除目录
    - MarkDown Toc: Insert\Update 插入目录
- 官网链接:
  - [https://marketplace.visualstudio.com/items?itemName=AlanWalk.markdown-toc](https://marketplace.visualstudio.com/items?itemName=AlanWalk.markdown-toc)

### 1.5.10. Markdown AutoTOC 目录

- 说明:
  - 自动生成 MarkDown 目录
- 使用:
  - 安装插件`Markdown AutoTOC`
  - 在文章头部输入`[[toc]]`,即可自动生成文档目录

### 1.5.11. Excel to Markdown table 表复制

Excel 便利复制到 MarkDown 中

- 安装插件`Excel to Markdown table`
- 使用命令`Shift+Alt+V`,即可复制 Excel 表格

### 1.5.12. MarkDown PDF

官网链接:

- [https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf](https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf)

命令使用

- 下载插件`Markdown PDF`
- Menu 右键菜单
- 命令面板查看`export`

### 1.5.13. 待办事项树 Tree

- 安装插件`TODO TREE`
- 推荐用户配置

```json
"todo-tree.defaultHighlight": {
"icon": "alert",
"type": "text",
"foreground": "red",
"background": "white",
"iconColour": "blue"
},
"todo-tree.customHighlight": {
"TODO": {
"icon": "check",
"type": "line"
},
"FIXME": {
"foreground": "black",
"iconColour": "yellow"
}
},
```

- 重启 vscode 软件即可生效
- 左侧导航栏存一个 `TODO TREE`

### 1.5.14. 插件-sftp VScode 连接服务器

**步骤 1:** 安装插件 sftp

**步骤 2:** 配置 stp-config

在 vscode 工作区.vscode 目录建 sftp.json 文件

内容如下

```json
{
  "host": "IP地址",
  "port": 22,
  "username": "用户",
  "password": "密码",
  "protocol": "sftp",
  "agent": null,
  "privateKeyPath": null,
  "passphrase": null,
  "passive": false,
  "interactiveAuth": true,
  "remotePath": "远程服务器路径",
  "uploadOnSave": true,
  "syncMode": "update",
  "ignore": ["**/.vscode/**", "**/.git/**", "**/.DS_Store"],
  "watcher": {
    "files": "glob",
    "autoUpload": true,
    "autoDelete": true
  }
}
```

**步骤三**: 重启 vscode，查看效果

## 1.6. 功能模块

### 1.6.1. MarkDown 同步印象笔记

参考链接: [https://www.cnblogs.com/rengised/p/6985031.html](https://www.cnblogs.com/rengised/p/6985031.html)

**步骤 1**: 安装软件

- 安装 Vscode
- 安装印象笔记
- 安装 vscode 插件 **EverMonkey**，**Auto-Open Markdown Preview**
- 重启 Vscode

**步骤 2**: 配置 EverMonkey

EverMonkey 插件主要负责将 vscode 中的文章同步到印象笔记.
使用命令`ctrl+Shift+P`打开输入栏,输入`ever token`
![步骤2: 配置EverMonkey](https://raw.githubusercontent.com/chenkang084/notes/master/imgs/blogs/vscode-2.gif)
国际版 International 中国版 China
将 token 和 noteStoreUrl 配置到 vscode 的用户设置中,
步骤为 File --> Preferences --> Settings

```conf
evermonkey.token: your developer token
evermonkey.noteStoreUrl: your API url
```

重启 Vscode

**步骤 3**:同步 MarkDown

编写 MarkDown 文件，文件头部加入如下

```markdown
---
title: 文件名称
tags: 标签（多个标签用逗号分隔）
notebook: （所属的目录）
---
```

完成文章内容编写之后，输入 Ctrl+Shift+P 打开 command,输入 ever publish,提示成功后.
快速提交文章的快捷键是 Alt+P
**其他步骤: 相关问题**
重要提示: 如果报 Evernote Error: 5 - Note.title，错误（这个错误坑了好一会）。说明是换行符有问题，请将 vscode 右下角的换行符从 CRLF 切换成 LF,然后再次执行 ever publish，就会有 blogs>>vscode 中使用印象笔记 created successfully.提示。如果还有错误，请到 git issue 查找相关问题。

### VScode 编辑后自动保存

参考链接: [vscode 如何设置自动保存](https://jingyan.baidu.com/article/f25ef25486bd5c482c1b82b8.html)

左下角设置图标 -> 设置

- Auto Save = off 不自动保存，每次都需要用户自己手动保存
- Auto Save = afterDelay 固定间隔时间，自动保存
- Auto Save = onFocusChange 当焦点离开编辑器的当前窗口时，自动保存
- onWindowChange 当编辑器窗口失去焦点时，自动保存,只有焦点离开整个编辑器，才会触发保存，在编辑器内部切换页签是不会自动保存的。

## 1.7. 新增功能

### 1.7.1. 插件-PicGo MarkDwon 支持图片上传到 Github

**参考链接:**

- [vscode 书写 Markdown 快速插入图片 picgo 2.0 插件使用](https://blog.csdn.net/li123_123_/article/details/102819890)
- [github 生成 token 的方法](https://www.cnblogs.com/leon-2016/p/9284837.html)

PicGo 配置如下:
![PicGo-Vscode-MarkDwon-Images图片上传.png](https://raw.githubusercontent.com/fansichao/awesome-it/master/images/20191127010011.png)

**PicGo 快捷键使用:**

- Ctrl+alt+U 剪切板
- Ctrl+alt+E 文件夹
- Ctrl+alt+O 指定路径

## 1.8. 其他

### 1.8.1. 网上插件推荐清单

参考链接:

- [VSCode 拓展插件推荐](https://www.cnblogs.com/zzsdream/p/6592429.html)
- [Visual Studio Code 必备插件](https://blog.csdn.net/x550392236/article/details/78646555)
- [VS Code 必备插件推荐](https://blog.csdn.net/shenxianhui1995/article/details/81604818)
- [精选！15 个必备的 VSCode 插件](https://blog.csdn.net/qq_38906523/article/details/77278403)

**精选插件清单**:

- HTML Snippets: 超级实用且初级的 H5 代码片段以及提示
- HTMLHint: html 代码检测
- HTML CSS Support : 让 html 标签上写 class 智能提示当前项目所支持的样式。新版已经支持 scss 文件检索，这个也是必备插件之一
- Auto Close Tag : 匹配标签，关闭对应的标签。很实用【HTML/XML】
- Auto Rename Tag : 修改 html 标签，自动帮你完成尾部闭合标签的同步修改
- Path Autocomplete : 路径智能补全
- Path Intellisense : 路径智能提示
- JavaScript Snippet Pack: 针对 js 的插件，包含了 js 的常用语法关键字，很实用；
- View InBrowser: 从浏览器中查看 html 文件，使用系统的当前默认浏览器
- Class autocomplete for HTML: 编写 html 代码的朋友们对 html 代码的一大体现就是重复，如果纯用手敲不仅累还会影响项目进度，这款自动补全插件真的很棒；
- beautify : 格式化代码的工具，可以格式化 JSON|JS|HTML|CSS|SCSS,比内置格式化好用
- Debugger for Chrome: 让 vscode 映射 chrome 的 debug 功能，静态页面都可以用 vscode 来打断点调试，真 666~
- jQuery Code Snippets: jquery 重度患者必须品
- vscode-icon: 让 vscode 资源树目录加上图标，必备良品！
- VSCode Great Icons: 另一款资源树目录图标
- colorize : 会给颜色代码增加一个当前匹配代码颜色的背景，非常好
- Color Info: 提供你在 CSS 中使用颜色的相关信息。你只需在颜色上悬停光标，就可以预览色块中色彩模型的（HEX、 RGB、HSL 和 CMYK）相关信息了。
- Bracket Pair Colorizer: 让括号拥有独立的颜色，易于区分。可以配合任意主题使用。
- vscode-fileheader: 顶部注释模板，可定义作者、时间等信息，并会自动更新最后修改时间
- Document This : js 的注释模板 （注意: 新版的 vscode 已经原生支持,在 function 上输入/\*\* tab）
- filesize: 在底部状态栏显示当前文件大小，点击后还可以看到详细创建、修改时间
- Code Runner : 代码编译运行看结果，支持众多语言
- Bootstrap 3 Sinnpet: 常用 bootstrap 的可以下
- GitLens: 丰富的 git 日志插件
- vetur: vue 语法高亮、智能感知、Emmet 等
- VueHelper: vue 代码提示
- Bookmarks: 一个书签工具,还是很有必要的
- tortoise-svn: SVN 的集成插件

### 1.8.2. 快捷键使用

在 Ctrl+P 下输入>又可以回到主命令框 Ctrl+Shift+P 模式。
在 Ctrl+P 窗口下还可以

```bash
直接输入文件名，快速打开文件
? 列出当前可执行的动作
! 显示Errors或Warnings，也可以Ctrl+Shift+M
: 跳转到行数，也可以Ctrl+G直接进入
@ 跳转到symbol（搜索变量或者函数），也可以Ctrl+Shift+O直接进入
@:根据分类跳转symbol，查找属性或函数，也可以Ctrl+Shift+O后输入:进入
# 6. 根据名字查找symbol，也可以Ctrl+T
```

- [官网快捷键文档](https://code.visualstudio.com/docs/getstarted/keybindings)
- [visualstudio 快捷键](https://blog.csdn.net/p358278505/article/details/74221214)
- [快捷方式清单](https://blog.csdn.net/qq_22338889/article/details/78790964)
