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

![20200202_Win_VScode_目录结构错误问题.png](https://raw.githubusercontent.com/fansichao/images/master/markdown/20200202_Win_VScode_%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84%E9%94%99%E8%AF%AF%E9%97%AE%E9%A2%98.png)
[VSCode 中 Markdown 目录显示异常](https://jingyan.baidu.com/article/6b97984df62b501ca3b0bf7a.html)

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

**步骤 3**:同步 MarkDown 到印象笔记

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

### 1.6.2. VScode 编辑后自动保存

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

### 1.8.2. 插件

C/C++ [ms-vscode.cpptolls] 智能推导，调试和代码浏览

C/C++ Clang Command Adapter [mitaki28.vscode-clang] 使用 Clang 的命令来分析 C/C++/Object-C 的代码诊断，还有代码补全。

C/C++ Snippets [hars.cppsnippets] 有用的 C/C++代码片断，节省时间

C++ Algorithm Mnemonics [davidbroetje.algorithm-mnemonics-vscode] 写 C++不可能不接触 STL，这个插件能让你使用 STL 算法更有生产力

cppcheck [matthewferreira.cppcheck] 这个插件帮你方便的调用 cppcheck 这款 C++静态分析软件的命令来检查你的 C++代码隐患，包括越界，资源泄漏等

Clang-Format [xaver.clang-format] 把你的 C，C++ Java js 等代码格式化为 Clang 的代码风格

Python [donjayamanne.python] Python 的分析，运行，调试，代码格式化，重构，单元测试，代码片段，这些都支持

C# [ms-vscode.csharp] C#太重了，还是用 Visual Studio 把，别用 VSCode。

PowerShell [ms-vscode.powershell] PowerShell 脚本的语法高亮，代码补全，提示，代码片段，跳转等等

Bash Debug [rogalmic.bash-debug] bash 调试器的 GUI 前端

Bash Beautify [shakram02.bash-beautify] Bash 的格式化，美化代码风格

CMake [twxs.cmake] 对于我这种 C/C++需要跨平台构建的人，Cmake 是神物。其他构建系统都是渣渣。 主要功能是脚本代码着色，代码补全提示，常用代码块

CMake Tools [vector-of-bool.cmake-tools] 这个 Cmake 插件是对前一个的插件扩展，主要是 cmake 命令的支持方面，前一个插件是 cmake 脚本语言的支持

ESLint [dbaeumer.vscode-eslint] 经常写 js 的需要用，最好的 js 静态分析软件

hexdump for VSCode [slevesque.vscode-hexdump] 十六进制查看插件，以前都是用 BeyondCompare 的，这个就很方便集成进来了

HTML CSS Support [ecmel.vscode-html-css] 写前端的必备，确实，我业余会写下前端。主要支持 class，id 属性补全，远程 css。js，jade 模版，vue 文件等

HTML Snippets [abusaidm.html-snippets] 主要提供 HTML 5 的全部 TAG 不全，着色，还有有用的 TAG 片段

vscode-caniuse [agauniyal.vscode-caniuse] 检测用户使用的 Web 技术被各种主流浏览器支持的情况

Quokka.js [WallabyJs.quokka-vscode] 是一个调试工具插件，能够根据你正在编写的代码提供实时反馈。它易于配置，并能够预览变量的函数和计算值结果。另外，在使用 JSX 或 TypeScript 项目中，它能够开箱即用。

vscode-faker [deerawan.vscode-faker] 使用流行的 JavaScript 库 – Faker，能够帮你快速的插入用例数据。Faker 可以随机生成姓名、地址、图像、电话号码，或者经典的乱数假文段落，并且每个类别还包含了各种子类别，你可以根据自身的需求来使用这些数据。

Color Info [bierner.color-info] 这个便捷的插件，将为你提供你在 CSS 中使用颜色的相关信息。你只需在颜色上悬停光标，就可以预览色块中色彩模型的（HEX、 RGB、HSL 和 CMYK）相关信息了。

svg viewer [cssho.vscode-svgviewer] 此插件在 Visual Studio 代码中添加了许多实用的 SVG 程序，你无需离开编辑器，便可以打开 SVG 文件并查看它们。同时，它还包含了用于转换为 PNG 格式和生成数据 URI 模式的选项。

TODO Highlight [wayou.vscode-todo-highlight] 这个插件能够在你的代码中标记出所有的 TODO 注释，以便更容易追踪任何未完成的业务。在默认的情况下，它会查找 TODO 和 FIXME 关键字。当然，你也可以添加自定义表达式。

minify [HookyQR.minify] 这是一款用于压缩合并 JavaScript 和 CSS 文件的应用程序。它提供了大量自定义的设置，以及自动压缩保存并导出为.min 文件的选项。它能够分别通过 uglify-js、clean-css 和 html-minifier，与 JavaScript、CSS 和 HTML 协同工作。

change-case [wmaurer.change-case] 虽然 VSCode 内置了开箱即用的文本转换选项，但其只能进行文本大小写的转换。而此插件则添加了用于修改文本的更多命名格式，包括驼峰命名、下划线分隔命名，snake_case 命名以及 CONST_CAS 命名等。

Regex Previewer [chrmarti.regex] 这是一个用于实时测试正则表达式的实用工具。它可以将正则表达式模式应用在任何打开的文件上，并高亮所有的匹配项。

Auto Close Tag [formulahendry.auto-close-tag] 适用于 JSX、Vue、HTML，在打开标签并且键入 </ 的时候，能自动补全要闭合的标签

Auto Rename Tag [formulahendry.auto-rename-tag] 适用于 JSX、Vue、HTML，在修改标签名时，能在你修改开始（结束）标签的时候修改对应的结束（开始）标签，帮你减少 50% 的击键；

Path Intellisense [christian-kohler.path-intellisense] 文件路径补全，在你用任何方式引入文件系统中的路径时提供智能提示和自动完成；

npm Intellisense [christian-kohler.npm-intellisense] NPM 依赖补全，在你引入任何 node_modules 里面的依赖包时提供智能提示和自动完成；

npm [eg2.vscode-npm-script] npm 集成到 VSCode 里面来了，很方便

Intellisense for CSS class names [Zignd.html-css-class-completion] CSS 类名补全，会自动扫描整个项目里面的 CSS 类名并在你输入类名时做智能提示；

Bracket Pair Colorizer [CoenraadS.bracket-pair-colorizer] 识别代码中的各种括号，并且标记上不同的颜色，方便你扫视到匹配的括号，在括号使用非常多的情况下能环节眼部压力，编辑器快捷键固然好用，但是在临近嵌套多的情况下却有些力不从心；

NSIS Language Support [KrystofRiha.vscode-nsis] 提供 NSIS 打包（exe 安装包）软件的打包脚本 NSIS 语言的语法高亮等语言级的支持

Partial Diff [ryu1kn.partial-diff] 顾名思义，这个是文本比较的插件，而且是部分比较，没有 BeyondCompare 那样强大，它可以比较选中的文本差异

vscode-icons [robertohuertasm.vscode-icons] 专给 vscode 的图标插件，它根据不同的文件后缀类型，用相应的文件类型 LOGO 标记出文件区别。嗯，IDE 都有类似的功能

CSS Peek [pranaygp.vscode-css-peek] 使用此插件，你可以追踪至样式表中 CSS 类和 ids 定义的地方。当你在 HTML 文件中右键单击选择器时，选择“ Go to Definition 和 Peek definition ”选项，它便会给你发送样式设置的 CSS 代码。

vue [jcbuisson.vue] 主要给 vue.js 框架提供语法高亮

Vue 2 Snippets [hollowtree.vue-snippets] 这个扩展是提供 Vue 2.0 版本的有用的代码片段和语法高亮

React Native Tools [vsmobile.vscode-react-native] 用 React Native 做移动端开发越来越流行了

React-Native/React/Redux sippets for es6/es7 [EQuimper.react-native-react-redux] React 全家桶的插件，提供代码片段

React/Redux/react-router [discountry.react-redux-react-router-snippets] React 全家桶，代码片段

JavaScript (ES6) code snippets [xabikos.javascriptsnippets] ES6 标准的 js 代码片段补全

Prettier - JavaScript formatter [esbenp.prettier-vscode] 可以格式化你的 js，typescript css 代码，让你的代码更好看

JavaScript Standard Style [chenxsan.vscode-standardjs] 以权威 js 标准风格来检测你的 js 代码

Babel JavaScript [mgmcdermott.vscode-language-babel] 如果你使用最新的 ES 标准来编写跨浏览器的 js 程序，那么这个就是你的好帮手了。主要提供语法高亮，React 的 jsx 都高亮

markdownlint [DavidAnson.vscode-markdownlint] 我经常用 MarkDown 写文章的，所以需要 MD 静态分析软件提示错误，warning。或者编写的风格问题

Code Runner [formulahendry.code-runner] 可以运行代码文件，和选择一段代码运行，支持 C，C++，Java，JS，PHP，Python，Perl，Ruby 等，你几乎所想到的语言都支持

IORun [hoangnc.io-run] 算法，IO，ACM 党最爱，如果你经常在 OJ 上刷题，那么就适合你。支持运行和测试竞赛代码。 多种语言 C，C++，Haskell 等等。 因为我做 LeetCode 上的题目

XML Tools [DotJoshJohnson.xml] XML 的格式化 XML 树结构，Xpath，Xquery 等都支持了

REST Client [humao.rest-client] 在 VSCode 中发送 http 请求，显示 http 回复 非常方便调试测试 RESTful 的接口

Ruby [rebornix.ruby] 计算理论的代码是用 Ruby 写的，在 github 上，有时候会写写 Ruby

Haskell Syntax Highlighting [justusadam.language-haskell] Haskell 的语法高亮, 学 Haskell 是涨见识的

Haskell ghc-mod [hoovercj.vscode-ghc-mod] 通过 ghc-mod 提供 Haskell 的语言支持

Haskell GHCi debug viewer Phoityne [phoityne.phoityne-vscode] 这个插件是一个 ghci 的调试查看器

haskell-linter [hoovercj.haskell-linter] 一个 haskell 的代码静态分析工具, 其实就是 hlint 的封装

Haskelly [UCL.haskelly] 提供完全的，专家级的 Haskell 开发

Haskero [Vans.haskero] 功能比较齐全的 Haskell IDE

Docker [PeterJausovec.vscode-docker] 提供 Dockerfile 和 docker-compose 文件的语法高亮，命令的高亮，还有代码提示与检测

Docker Explorer [formulahendry.docker-explorer] 管理 Docker 容器，镜像，Docker Hub 等

Git History [donjayamanne.githistory] 可以查看 Git log, file, 和 line 历史记录。

Document This [joelday.docthis] 自动生成详细的 TypeScript 和 js 的文档型注释

Setting Sync [Shan.code-settings-sync] 跨机器同步 VSCode 的配置，需要用到 github 的 gist

Debugger for Chrome/ Debugger for Firefox 字面意思，无需多说

gitignore [codezombiech.gitignore] 帮助你更好的使用 gitignore

### 1.8.3. 快捷键使用

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
