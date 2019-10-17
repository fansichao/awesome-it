<!--
 * @Author: Scfan
 * @Date: 2019-08-10 20:47:12
 * @LastEditors: Scfan
 * @LastEditTime: 2019-08-10 20:47:15
 * @Description: 工作&学习&生活
 * @Email: 643566992@qq.com
 * @Company: 上海
 * @version: V1.0
 -->

# Title:MarkDown语法说明&技巧使用&相关工具

标签（空格分隔）： MarkDown 语法说明 技巧 BBS文档 CSDN博客 

---

初级目录

 - [MarkDown技巧](#MarkDown技巧)
 - [MarkDown工具]
 - [MarkDown相关链接]
 - 
 - [MarkDown语法说明
     - [CSDN的Markdown语法说明]
     - [CMDMarkdwon语法说明]

--- [toc]

# MarkDown技巧

**空格的使用：**
```Linux
&ensp;或&#8194;	半方大的空白
&emsp;或&#8195;	全方大的空白  
&nbsp;或&#160;	不断行的空白格
&emsp; 常用一个汉字的空格
```
**字体高亮：**
*字体高亮 字体Mark(有道云MarkDown可以使用)*
```==字体高亮 字体Mark==```
![字体高亮 字体Mark效果图](http://omhwhig1i.bkt.clouddn.com/17-3-9/64580645-file_1489027185910_6a2.png)
**图片链接跳转：**

[![B站](http://omhwhig1i.bkt.clouddn.com/17-4-7/30999908-file_1491561302289_dff0.jpg)](http://www.bilibili.com/)
```
[![](http://omhwhig1i.bkt.clouddn.com/17-4-7/30999908-file_1491561302289_dff0.jpg)](http://www.bilibili.com/) # 图片和链接的结合使用
```
**自动生成Markdown侧边栏目录：**
自动生成侧边栏目录，需要网站相适应，含css、js等文件，无法独立成为一个html
[自动生成Markdwon侧边栏目录：](http://pan.baidu.com/s/1o8hosf4)


----

# MarkDown工具
### **MarkDown编辑器：**
 - [Cmd Markdown 编辑阅读器](https://www.zybuluo.com/cmd/)
 - [有道云笔记MarkDown编辑器](http://note.youdao.com/)
### **MarkDown编辑器语法：**
 - [【简明版】有道云笔记Markdown指南](http://note.youdao.com/iyoudao/?p=2411)
 - [【进阶版】有道云笔记Markdown指南](http://note.youdao.com/iyoudao/?p=2445)
 - [Cmd MarkDown编辑器语法](https://www.zybuluo.com/mdeditor)
 - [CSDN MarkDown语法](http://blog.csdn.net/qq_21165007/article/details/60882874)
 - [GcsSloop的博客MarkDown高级语法教程](https://juejin.im/entry/5821943f5bbb500059f84b58#fnref:1)
 - [Cmd Markdown 简明语法手册](https://www.zybuluo.com/mdeditor?url=https://www.zybuluo.com/static/editor/md-help.markdown#2-%E6%A0%87%E7%AD%BE%E5%88%86%E7%B1%BB)

### 图片外链配置(★★★★☆):
 - 图片外链网站配置参考博客：http://blog.csdn.net/u014727260/article/details/54897041
 - 图片外链工具网站：
	 - 极简图床（http://yotuku.cn/#/）
	 - 七牛云存储（https://portal.qiniu.com）
 
----

### MarkDown相关链接
- [MarkDown技巧：两种方式实现页内跳转](http://www.tuicool.com/articles/viIVRfF)












-----








----
# MarkDown语法说明

## 欢迎使用Markdown编辑器写博客

本Markdown编辑器使用[StackEdit][6]修改而来，用它写博客，将会带来全新的体验哦：

- **Markdown和扩展Markdown简洁的语法**
- **代码块高亮**
- **图片链接和图片上传**
- ***LaTex*数学公式**
- **UML序列图和流程图**
- **离线写博客**
- **导入导出Markdown文件**
- **丰富的快捷键**

### 快捷键

 - 加粗    `Ctrl + B` 
 - 斜体    `Ctrl + I` 
 - 引用    `Ctrl + Q`
 - 插入链接    `Ctrl + L`
 - 插入代码    `Ctrl + K`
 - 插入图片    `Ctrl + G`
 - 提升标题    `Ctrl + H`
 - 有序列表    `Ctrl + O`
 - 无序列表    `Ctrl + U`
 - 横线    `Ctrl + R`
 - 撤销    `Ctrl + Z`
 - 重做    `Ctrl + Y`

### Markdown及扩展

> Markdown 是一种轻量级标记语言，它允许人们使用易读易写的纯文本格式编写文档，然后转换成格式丰富的HTML页面。    —— <a href="https://zh.wikipedia.org/wiki/Markdown" target="_blank"> [ 维基百科 ]

使用简单的符号标识不同的标题，将某些文字标记为**粗体**或者*斜体*，创建一个[链接](http://www.csdn.net)等，详细语法参考帮助？。

本编辑器支持 **Markdown Extra** , 　扩展了很多好用的功能。具体请参考[Github][2].  

#### 表格

**Markdown　Extra**　表格语法：

项目     | 价格
-------- | ---
Computer | $1600
Phone    | $12
Pipe     | $1

可以使用冒号来定义对齐方式：

| 项目      |    价格 | 数量  |
| :-------- | --------:| :--: |
| Computer  | 1600 元 |  5   |
| Phone     |   12 元 |  12  |
| Pipe      |    1 元 | 234  |

#### 定义列表

**Markdown　Extra**　定义列表语法：
项目１
项目２
:   定义 A
:   定义 B

项目３
:   定义 C

:   定义 D

	> 定义D内容

#### 代码块
代码块语法遵循标准markdown代码，例如：
``` python
@requires_authorization
def somefunc(param1='', param2=0):
    '''A docstring'''
    if param1 > param2: # interesting
        print 'Greater'
    return (param2 - param1 + 1) or None
class SomeClass:
    pass
>>> message = '''interpreter
... prompt'''
```

#### 脚注
生成一个脚注[^footnote].
  [^footnote]: 这里是 **脚注** 的 *内容*.
  
#### 目录
用 `[TOC]`来生成目录：

[TOC]

#### 数学公式
使用MathJax渲染*LaTex* 数学公式，详见[math.stackexchange.com][1].

 - 行内公式，数学公式为：$\Gamma(n) = (n-1)!\quad\forall n\in\mathbb N$。
 - 块级公式：

$$	x = \dfrac{-b \pm \sqrt{b^2 - 4ac}}{2a} $$

更多LaTex语法请参考 [这儿][3].

#### UML 图:

可以渲染序列图：

```sequence
张三->李四: 嘿，小四儿, 写博客了没?
Note right of 李四: 李四愣了一下，说：
李四-->张三: 忙得吐血，哪有时间写。
```

或者流程图：

```flow
st=>start: 开始
e=>end: 结束
op=>operation: 我的操作
cond=>condition: 确认？

st->op->cond
cond(yes)->e
cond(no)->op
```

- 关于 **序列图** 语法，参考 [这儿][4],
- 关于 **流程图** 语法，参考 [这儿][5].

### 离线写博客

即使用户在没有网络的情况下，也可以通过本编辑器离线写博客（直接在曾经使用过的浏览器中输入[write.blog.csdn.net/mdeditor](http://write.blog.csdn.net/mdeditor)即可。**Markdown编辑器**使用浏览器离线存储将内容保存在本地。

用户写博客的过程中，内容实时保存在浏览器缓存中，在用户关闭浏览器或者其它异常情况下，内容不会丢失。用户再次打开浏览器时，会显示上次用户正在编辑的没有发表的内容。

博客发表后，本地缓存将被删除。　

用户可以选择 <i class="icon-disk"></i> 把正在写的博客保存到服务器草稿箱，即使换浏览器或者清除缓存，内容也不会丢失。

> **注意：**虽然浏览器存储大部分时候都比较可靠，但为了您的数据安全，在联网后，**请务必及时发表或者保存到服务器草稿箱**。

### 浏览器兼容

 1. 目前，本编辑器对Chrome浏览器支持最为完整。建议大家使用较新版本的Chrome。
 3. IE９以下不支持
 4. IE９，１０，１１存在以下问题
    1. 不支持离线功能
    1. IE9不支持文件导入导出
    1. IE10不支持拖拽文件导入

---------

[1]: http://math.stackexchange.com/
[2]: https://github.com/jmcmanus/pagedown-extra "Pagedown Extra"
[3]: http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference
[4]: http://bramp.github.io/js-sequence-diagrams/
[5]: http://adrai.github.io/flowchart.js/
[6]: https://github.com/benweet/stackedit



## 欢迎使用 Cmd Markdown 编辑阅读器




我们理解您需要更便捷更高效的工具记录思想，整理笔记、知识，并将其中承载的价值传播给他人，**Cmd Markdown** 是我们给出的答案 —— 我们为记录思想和分享知识提供更专业的工具。 您可以使用 Cmd Markdown：

> * 整理知识，学习笔 


---
> * 发布日记，杂文，所见所想
> * 撰写发布技术文稿（代码支持）
> * 撰写发布学术论文（LaTeX 公式支持）

![cmd-markdown-logo](https://www.zybuluo.com/static/img/logo.png)

除了您现在看到的这个 Cmd Markdown 在线版本，您还可以前往以下网址下载：

#### [Windows/Mac/Linux 全平台客户端](https://www.zybuluo.com/cmd/)

> 请保留此份 Cmd Markdown 的欢迎稿兼使用说明，如需撰写新稿件，点击顶部工具栏右侧的 <i class="icon-file"></i> **新文稿** 或者使用快捷键 `Ctrl+Alt+N`。

------

### 什么是 Markdown

Markdown 是一种方便记忆、书写的纯文本标记语言，用户可以使用这些标记符号以最小的输入代价生成极富表现力的文档：譬如您正在阅读的这份文档。它使用简单的符号标记不同的标题，分割不同的段落，**粗体** 或者 *斜体* 某些文字，更棒的是，它还可以

#### 1. 制作一份待办事宜 [Todo 列表](https://www.zybuluo.com/mdeditor?url=https://www.zybuluo.com/static/editor/md-help.markdown#13-待办事宜-todo-列表)

- [ ] 支持以 PDF 格式导出文稿
- [ ] 改进 Cmd 渲染算法，使用局部渲染技术提高渲染效率
- [x] 新增 Todo 列表功能
- [x] 修复 LaTex 公式渲染问题
- [x] 新增 LaTex 公式编号功能

#### 2. 书写一个质能守恒公式[^LaTeX]

$$E=mc^2$$

#### 3. 高亮一段代码[^code]

```python
@requires_authorization
class SomeClass:
    pass

if __name__ == '__main__':
    # A comment
    print 'hello world'
```

#### 4. 高效绘制 [流程图](https://www.zybuluo.com/mdeditor?url=https://www.zybuluo.com/static/editor/md-help.markdown#7-流程图)

```flow
st=>start: Start
op=>operation: Your Operation
cond=>condition: Yes or No?
e=>end

st->op->cond
cond(yes)->e
cond(no)->op
```

#### 5. 高效绘制 [序列图](https://www.zybuluo.com/mdeditor?url=https://www.zybuluo.com/static/editor/md-help.markdown#8-序列图)

```seq
Alice->Bob: Hello Bob, how are you?
Note right of Bob: Bob thinks
Bob-->Alice: I am good thanks!
```

#### 6. 高效绘制 [甘特图](https://www.zybuluo.com/mdeditor?url=https://www.zybuluo.com/static/editor/md-help.markdown#9-甘特图)

```gantt
    title 项目开发流程
    section 项目确定
        需求分析       :a1, 2016-06-22, 3d
        可行性报告     :after a1, 5d
        概念验证       : 5d
    section 项目实施
        概要设计      :2016-07-05  , 5d
        详细设计      :2016-07-08, 10d
        编码          :2016-07-15, 10d
        测试          :2016-07-22, 5d
    section 发布验收
        发布: 2d
        验收: 3d
```

#### 7. 绘制表格

| 项目        | 价格   |  数量  |
| --------   | -----:  | :----:  |
| 计算机     | \$1600 |   5     |
| 手机        |   \$12   |   12   |
| 管线        |    \$1    |  234  |

#### 8. 更详细语法说明

想要查看更详细的语法说明，可以参考我们准备的 [Cmd Markdown 简明语法手册][1]，进阶用户可以参考 [Cmd Markdown 高阶语法手册][2] 了解更多高级功能。

总而言之，不同于其它 *所见即所得* 的编辑器：你只需使用键盘专注于书写文本内容，就可以生成印刷级的排版格式，省却在键盘和工具栏之间来回切换，调整内容和格式的麻烦。**Markdown 在流畅的书写和印刷级的阅读体验之间找到了平衡。** 目前它已经成为世界上最大的技术分享网站 GitHub 和 技术问答网站 StackOverFlow 的御用书写格式。

---

### 什么是 Cmd Markdown

您可以使用很多工具书写 Markdown，但是 Cmd Markdown 是这个星球上我们已知的、最好的 Markdown 工具——没有之一 ：）因为深信文字的力量，所以我们和你一样，对流畅书写，分享思想和知识，以及阅读体验有极致的追求，我们把对于这些诉求的回应整合在 Cmd Markdown，并且一次，两次，三次，乃至无数次地提升这个工具的体验，最终将它演化成一个 **编辑/发布/阅读** Markdown 的在线平台——您可以在任何地方，任何系统/设备上管理这里的文字。

#### 1. 实时同步预览

我们将 Cmd Markdown 的主界面一分为二，左边为**编辑区**，右边为**预览区**，在编辑区的操作会实时地渲染到预览区方便查看最终的版面效果，并且如果你在其中一个区拖动滚动条，我们有一个巧妙的算法把另一个区的滚动条同步到等价的位置，超酷！

#### 2. 编辑工具栏

也许您还是一个 Markdown 语法的新手，在您完全熟悉它之前，我们在 **编辑区** 的顶部放置了一个如下图所示的工具栏，您可以使用鼠标在工具栏上调整格式，不过我们仍旧鼓励你使用键盘标记格式，提高书写的流畅度。

![tool-editor](https://www.zybuluo.com/static/img/toolbar-editor.png)

#### 3. 编辑模式

完全心无旁骛的方式编辑文字：点击 **编辑工具栏** 最右侧的拉伸按钮或者按下 `Ctrl + M`，将 Cmd Markdown 切换到独立的编辑模式，这是一个极度简洁的写作环境，所有可能会引起分心的元素都已经被挪除，超清爽！

#### 4. 实时的云端文稿

为了保障数据安全，Cmd Markdown 会将您每一次击键的内容保存至云端，同时在 **编辑工具栏** 的最右侧提示 `已保存` 的字样。无需担心浏览器崩溃，机器掉电或者地震，海啸——在编辑的过程中随时关闭浏览器或者机器，下一次回到 Cmd Markdown 的时候继续写作。

#### 5. 离线模式

在网络环境不稳定的情况下记录文字一样很安全！在您写作的时候，如果电脑突然失去网络连接，Cmd Markdown 会智能切换至离线模式，将您后续键入的文字保存在本地，直到网络恢复再将他们传送至云端，即使在网络恢复前关闭浏览器或者电脑，一样没有问题，等到下次开启 Cmd Markdown 的时候，她会提醒您将离线保存的文字传送至云端。简而言之，我们尽最大的努力保障您文字的安全。

#### 6. 管理工具栏

为了便于管理您的文稿，在 **预览区** 的顶部放置了如下所示的 **管理工具栏**：

![tool-manager](https://www.zybuluo.com/static/img/toolbar-manager.jpg)

通过管理工具栏可以：

<i class="icon-share"></i> 发布：将当前的文稿生成固定链接，在网络上发布，分享
<i class="icon-file"></i> 新建：开始撰写一篇新的文稿
<i class="icon-trash"></i> 删除：删除当前的文稿
<i class="icon-cloud"></i> 导出：将当前的文稿转化为 Markdown 文本或者 Html 格式，并导出到本地
<i class="icon-reorder"></i> 列表：所有新增和过往的文稿都可以在这里查看、操作
<i class="icon-pencil"></i> 模式：切换 普通/Vim/Emacs 编辑模式

#### 7. 阅读工具栏

![tool-manager](https://www.zybuluo.com/static/img/toolbar-reader.jpg)

通过 **预览区** 右上角的 **阅读工具栏**，可以查看当前文稿的目录并增强阅读体验。

工具栏上的五个图标依次为：

<i class="icon-list"></i> 目录：快速导航当前文稿的目录结构以跳转到感兴趣的段落
<i class="icon-chevron-sign-left"></i> 视图：互换左边编辑区和右边预览区的位置
<i class="icon-adjust"></i> 主题：内置了黑白两种模式的主题，试试 **黑色主题**，超炫！
<i class="icon-desktop"></i> 阅读：心无旁骛的阅读模式提供超一流的阅读体验
<i class="icon-fullscreen"></i> 全屏：简洁，简洁，再简洁，一个完全沉浸式的写作和阅读环境

#### 8. 阅读模式

在 **阅读工具栏** 点击 <i class="icon-desktop"></i> 或者按下 `Ctrl+Alt+M` 随即进入独立的阅读模式界面，我们在版面渲染上的每一个细节：字体，字号，行间距，前背景色都倾注了大量的时间，努力提升阅读的体验和品质。

#### 9. 标签、分类和搜索

在编辑区任意行首位置输入以下格式的文字可以标签当前文档：

标签： 未分类

标签以后的文稿在【文件列表】（Ctrl+Alt+F）里会按照标签分类，用户可以同时使用键盘或者鼠标浏览查看，或者在【文件列表】的搜索文本框内搜索标题关键字过滤文稿，如下图所示：

![file-list](https://www.zybuluo.com/static/img/file-list.png)

#### 10. 文稿发布和分享

在您使用 Cmd Markdown 记录，创作，整理，阅读文稿的同时，我们不仅希望它是一个有力的工具，更希望您的思想和知识通过这个平台，连同优质的阅读体验，将他们分享给有相同志趣的人，进而鼓励更多的人来到这里记录分享他们的思想和知识，尝试点击 <i class="icon-share"></i> (Ctrl+Alt+P) 发布这份文档给好友吧！

------

再一次感谢您花费时间阅读这份欢迎稿，点击 <i class="icon-file"></i> (Ctrl+Alt+N) 开始撰写新的文稿吧！祝您在这里记录、阅读、分享愉快！

作者 [@ghosert][3]     
2016 年 07月 07日    

[^LaTeX]: 支持 **LaTeX** 编辑显示支持，例如：$\sum_{i=1}^n a_i=0$， 访问 [MathJax][4] 参考更多使用方法。

[^code]: 代码高亮功能支持包括 Java, Python, JavaScript 在内的，**四十一**种主流编程语言。

[1]: https://www.zybuluo.com/mdeditor?url=https://www.zybuluo.com/static/editor/md-help.markdown
[2]: https://www.zybuluo.com/mdeditor?url=https://www.zybuluo.com/static/editor/md-help.markdown#cmd-markdown-高阶语法手册
[3]: http://weibo.com/ghosert
[4]: http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference






```python

```
