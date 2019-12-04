# Study-如何科学使用 Stack Overflow.md

tags: StackOverFlow 2019 年 12 月 搜索 必备知识 翻墙

[Stack OverFalow](https://stackoverflow.com/)作为程序员的帮助论坛，**Stack OverFalow 和 Google 远远优于百度**

## Stack OverFalow 简介

[作为初学者，如何有效使用 Stack Overflow？](https://www.quora.com/How-can-I-use-Stack-Overflow-effectively-as-a-beginner)

程序员的一个帮助论坛，您可以在其中发布问题或问题并获得解决方案。

最有可能的是，Stack Overflow 已经可以解决您的编程问题。您需要做的就是在 Google 中键入查询或关注的内容，默认情况下，Stack Overflow 将位于第一个链接中。

如果您的查询解决方案不在 Stack Overflow 中，请发布问题，您肯定会很快得到答案。

您可以从使用 Stack Overflow 获取查询的答案开始，一旦您觉得自己已经足够了解，也可以开始回答。

## Stack OverFlow 使用

### 如何搜索

本节内容翻译于 [Stack OverFlow 官网搜素方法](https://stackoverflow.com/help/searching)

**基础搜索:**

- 要在特定标签内[maintenance] seat 搜索，请在方括号中输入：在[maintenance]标签内搜索“ seat”的提述。
- 要查找特定短语，请在引号中输入它"flat tire"。
- 要将搜索限制为仅问题的标题，请 title:在搜索词后使用。同样，仅搜索正文（不包括标题）body:"phrase here"。
- 仅搜索您的帖子：在 user:me training 所有帖子中搜索“培训”一词。
- 要从标签，术语或短语中排除结果，请-在查询中为其添加前缀：waffles -unicorns 查找提及面糊早餐的帖子，其中不包含神话[laurel] -[hardy]人物，而仅包含与经典喜剧夫妇前半部分有关的帖子。
- 使用通配符搜索来扩大结果；*在单词中的任意位置（例如 encour*或）添加星号（）Ex\*nge。

**范围搜索:**
要仅搜索分数，答案数或视图数在特定范围内的问题，可以输入上限或下限参数或范围。

- score:-1 或 score:-1..都会返回分数均大于或等于-1 的帖子
- views:500..1000 否则 views:500-1000 将返回具有 500 到 1000 个视图的帖子
- answers:..3 将返回 3 个或以下答案的问题

**日期**
您可以使用以下日期运算符，使用特定的日期或日期范围将结果缩小到在特定时间段内创建或活动的帖子：

- created: 指定创建帖子的时间
- lastactive: 在指定时间段内处于活动状态的帖子
  可以采用以下格式输入日期：

- 绝对日期：
  - 仅年份 -例如，created:2012..2013 从 2012 年 1 月 1 日到 2013 年 12 月 31 日创建的搜索帖子；created:2012 搜索从 2012 年 1 月 1 日到 2012 年 12 月 31 日创建的帖子。
  - 年和月 –例如，created:2012-04..2012-05 在 2012 年 4 月 1 日至 2012 年 5 月 31 日之间创建的搜索帖子。
  - 日，月和年 –例如，lastactive:2012-04-03 搜索最近处于活动状态的帖子（2012 年 4 月 3 日上午 12:00 到 2012 年 4 月 3 日下午 11:59）。
- 相对日期
  - 1y，1m 和 1d 是简写“去年”，“上个月”和“昨天” -例如，如果今天是 4 月 15 日，created:1m3 月 1 日和 3 月 31 日之间创建搜索职位（可以替换任何数量 1 回首那很多年，几个月或几天。）
  - 范围（1y..）中的相对日期回溯到上一个期间的同一日期-例如，如果您想查看过去三个月中所有活动的帖子，请使用 lastactive:3m..4 月 15 日，它将显示从 1 月 15 日到最近活跃。您也可以关闭范围：lastactive:3m..1m。

请注意，**所有时间均以 UTC 记录；结果可能与您的时区不符**。

**用户运营商**
您也可以将搜索限制为特定用户的内容（您自己或他人的内容）。您将需要用户 ID 来搜索其他用户的帖子。

- user:mine 或 user:me（或任何用户 ID）仅返回您的帖子（或仅返回您输入 ID 的任何用户的帖子）
- infavorites:mine （或任何用户 ID）仅返回您（或您输入 ID 的用户）最喜欢的问题。
- intags:mine 仅返回出现在您标记为收藏的标签中的帖子。（如果您没有任何标签，则此运算符将不执行任何操作。为了获得更好的结果，请更新您的首选项。）

**布尔运算符**
可以将以下搜索运算符与 yes / no，true / false 或 1/0（每个对的行为相同）一起使用：

- isaccepted:yes / true / 1 仅返回已标记为“已接受”的答案；no / false / 0 仅返回未标记为接受的答案。
- hascode:yes / true / 1 仅返回包含代码块的帖子；no / false / 0 仅返回不包含代码的帖子。
- hasaccepted:是/真/ 1 只返回问题，已接受的答案; no / false / 0 仅返回没有接受答案的问题。
- isanswered:yes / true / 1 仅返回至少具有一个肯定评分答案的问题；no / false / 0 仅返回没有肯定评分答案的问题。
- closed:yes / true / 1 仅返回已关闭的问题；否/否/ 0 从搜索中排除已关闭的问题。
- duplicate:yes / true / 1 返回已被标记为另一个问题重复项的问题；否/否/ 0 从搜索中排除重复的问题。
- migrated:yes / true / 1 仅返回已迁移到其他站点的问题；no / false / 0 从搜索中排除迁移的问题。
- locked:yes / true / 1 仅返回锁定的帖子（已禁用编辑，投票，评论和新答案）；no / false / 0 仅返回未锁定的帖子。
- hasnotice:yes / true / 1 仅返回帖子下方显示通知的帖子；no / false / 0 仅返回未应用通知的帖子。
- wiki:yes / true / 1 仅返回社区 Wiki 帖子；no / false / 0 仅返回非社区 Wiki 帖子。

**OR 运算符**
要合并来自多个标签的结果，请用单词“或”将标签名称（用方括号括起来）分开：[widgets] or [geegaws]返回使用任一标签标记的问题。

**杂项运算符:**

- url:"example.com" 搜索包含网址“ example.com”的帖子
- is:question 将结果缩小为仅问题，is:answer 仅返回答案
- inquestion:50691 将搜索限制为 ID 为 50691 的问题。如果使用问题页面上的搜索框进行搜索，则可以 inquestion:this 将结果限制为已查看的帖子。

**删除的帖子**（需要 10,000 名声望）
当您获得“访问主持人工具”特权时，可以使用 deleted:操作员搜索自己删除的帖子。

- deleted:1 仅搜索您删除的帖子
- deleted:all 既搜索已创作的帖子，也搜索未删除的帖子
- deleted:0 仅搜索您撰写的未删除帖子（与相同 user:me）
  网站主持人可以使用该操作员搜索网站上的所有帖子，包括其他用户拥有的帖子。

### 如何提问

![20191202195053.png](https://raw.githubusercontent.com/fansichao/images/master/markdown/20191202195053.png)

#### 优雅提问

提问：

1，In my limited experience with .. 谦虚表达自己在某方面的经验

2， I am searching for a long time on net. But no use. Please help or try to give some ideas how to achieve this. 找了很久未果，求助攻

3，after searching around for a decent XX solution and found that everything out there was difficult to use. 找了 N 种方法都发现太 TM 难了。

4，I' ve looked around and apparently I've got the choice between these libraries/ solutions: 说明自己是努力搜索过的，然后目前有了哪几种方案

5，which seems it's a promising solution. 看起来是一个好解决方案

6，Ive tried multiple variations of this, but none of them seem to work. Any ideas? 试了很多种方法都无效，求助

7，Wanted to know if it's good practice to do that and what would be the best way to do that? 我的做法是否正确，是否有更好的法子？

8，Thanks in advance. 先行谢过

### 如何回答

#### 优雅回答

回答问题：

1，If I understand you correctly, you want to xxx 如果我没理解错，你想。。

2，Can you provided more details about your use case ? Can you provide more xml and code setting the url ? 提供更详细

## 附件

### 参考资源

- [好文-如何科学使用 Stack Overflow](https://blog.csdn.net/weixin_38233274/article/details/80349534)
- [如何优雅地使用 Stack Overflow](https://www.cnblogs.com/huangjianping/p/7941983.html)
- [为什么程序员一定要会用 Google 和 Stack Overflow](https://blog.csdn.net/u012207345/article/details/81139665)
