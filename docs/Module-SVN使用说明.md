# Linux-SVN 使用说明

[toc]

SVN 是 Subversion 的简称，是一个开放源代码的版本控制系统，相较于 RCS、CVS，它采用了分支管理系统，它的设计目标就是取代 CVS。互联网上很多版本控制服务已从 CVS 迁移到 Subversion。说得简单一点 SVN 就是用于多个人共同开发同一个项目，共用资源的目的。

Linux:涉及 SVN 的同步、更新以及同步到项目目录
SVN 基础用法：项目或者日常所需足以
SVN 进阶用法：svn 的问题难点等
SVN 终极用法：涉及 svn 的合并，分流，标签 tag 等很少使用的命令，了解即可。
Linux 中 SVN 扩充使用用法
SVN 使用注意事项:
SVN 细节 tips：

## SVN 插件

### SVN Excel 比对

https://blog.csdn.net/ccpat/article/details/50725774

## 基础用法

     1.安装SVN
          yum install subversion
     2.下载文件 svn co
          用户名 密码 80001  80001
          外网：svn co https://115.239.176.61:10081/svn/lqr/fb   出现输入用户名密码，之后会选择是否永久保存密码。保存/不保存都可。
          内网：svn co https://155.104.1.106:81/svn/lqr/fb
     3.添加文件到版本库，新增加的文件需要此操作
          svn add filename    添加文件到版本库控制
          svn ci -m "" filename    上传文件
     4.上传文件 svn ci -m "注释" filename
     5.更新文件 svn up filename
     6.比对本地和版本库中那些文件不同
          svn st 比对此目录下包含所有子目录的文件，显示状态如下：

     描述：输出WC中文件和目录的状态。如果WC提交，这些状态就会同步到库里。
     一般状态有         ' '  没有修改
     'A'  新增
     'D'  删除
     'M'  修改
     'R'  替代
     'C'  冲突
     'I'  忽略
     '?'  未受控
     '!'  丢失，一般是将受控文件直接删除导致
     7.比对文件 svn diff filename  比对当前文件和svn版本上文件的区别
     8.删除文件 svn delete filename
               svn ci -m"注释" filename  会删除版本库的文件，其他人电脑更新后也会删除
     9.导出文件夹
          svn export filename  这样不会有.svn文件，直接拷贝会有.svn文件（导致无法放入版本库中）
     10.查看文件日志
          svn log filename
     11.恢复到某一版本
          1.暂时恢复，不会影响版本库，但是提交前需要更新
          svn up -r 333 filename
          2.将版本库中恢复到过去版本
          svn merge -r 20:10 filename
          svn ci -m "注释back to r 10,xxxxx" filename
     12.查看svn的信息
          svn info  可以查看svn的路径等
     13.当svn up 出现  error:need cleanup
          svn cleanup 当up失败时，清除失败文件重新up
     14.移动文件
          svn move filename  在版本库中移动文件，当需要修改文件路径时，需要这么做。
     15.重命名文件
          svn rename filename 修改版本库中的文件名。
     16.svn 删除版本库目录下所有中.svn文件

**svn 删除版本库目录下所有中.svn 文件**

```python
find . -type d -name “.svn”|xargs rm -rf      或者
find . -type d -iname ”.svn” -exec rm -rf {} \;
```

## 进阶用法

1.svn up 更新过程中遇到冲突 1.显示信息：
选择: (p) 推迟，(df) 显示全部差异，(e) 编辑,
(mc) 我的版本, (tc) 他人的版本,
(s) 显示全部选项: 2.冲突出现时，一般按 p 查看冲突文件，
再解决冲突，解决之后，svn resolved filename 表示冲突已经解决

2.svn up 文件返回的信息
\$ svn update
U INSTALL 文件本地未修改
G README 文件本地已修改，修改内容无冲突，自动合并
C bar.c 文件本地已修改，修改内容有冲突，需要手动解决

3.对于多个文件的提交
1.svn st 得到差异文件 2.拷贝内容至编辑器，同类文件批量替换，例如 M --> svn ci -m "注释" 3.直接提交即可。

4.其他

svn ci -m"xxxx"web/a.py 会上传所有的的文件
svn ci -m"xxxx" web/a.py 只会上传一个

svn ci -m"" \* 会上传当前目录以及子目录下的所有文件，一般不用

1.svn ci -m"注释" xx.py 如果后续的 xx.py 等未添加，会上传当前目录所有文件。

SVN 终极用法--很少用的功能

SVN 使用 log list cat diff 查看所有以及特定文件版本信息
svn log 展示给你主要信息：每个版本附加在版本上的作者与日期信息和所有路径修改。
svn diff 显示特定修改的行级详细信息。
svn cat 取得在特定版本的某一个文件显示在当前屏幕。
svn list 显示一个目录在某一版本存在的文件。
使用 svn xxx 时，可以用 svn diff -c http://xxxxx/test.py用路径来做处理
-v 显示详细信息

svn log --verbose(-v)，详细模式下，显示路径修改的历史
svn log -r 8 -v
svn log --quiet(-v) 禁止显示日志信息的主要部分
svn log -v -q 只显示修改的文件名
svn diff -r 2:3 test.py
svn diff --change(-c) test.py 与前一个修订版本的文件比较
svn cat -r 2 test.py 仅仅查看，某个版本的内容
svn cat -r 2 test.py > test_2.py 重定向输出
svn list 不下载文件到本地目录的情况下来查看目录中的文件。

svn delete 之后未提交的文件恢复，svn revert(恢复)
svn 误删除文件之后的恢复（已经提交）。
Windows 的文件恢复
1.svn showlog 找到被删除的文件 2.右键文件选择 revert changes from this revision
3.(或许需要更新)便可查看被删除的文件
svn log | more 查看所有的版本信息（当页面无法显示所有的 log 时）

## 注意事项

1.不要直接替换文件，然后上传，应该用 svn up 更新无冲突后，在 svn ci 上传 2.如果需要拿出来文件，可以 svn co 从 xxxxx/xx/xx/xx/fb/xx 直接 svn 下载所需的文件夹，然后再 svn up 和 svn ci 上传文件 3.如果替换文件（不推荐）--必须在上传前，svn up 并且被替换文件无修改，无冲突（必须要被替换文件没有任何修改痕迹）等，才可以替换。
否则容易遗失。 4.如上

## 功能详解

TortoiseSVN 是 windows 下其中一个非常优秀的 SVN 客户端工具。通过使用它，我们可以可视化的管理我们的版本库。不过由于它只是一个客户端，所以它不能对版本库进行权限管理。

TortoiseSVN 不是一个独立的窗口程序，而是集成在 windows 右键菜单中，使用起来比较方便。

TortoiseSVN 每个菜单项都表示什么意思

```python
01、SVN Checkout(SVN取出)
点击SVN Checkout，弹出检出提示框，在URL of repository输入框中输入服务器仓库地址，在Checkout directory输入框中输入本地工作拷贝的路径，点击确定，即可检出服务器上的配置库。

02、SVN Update(SVN更新)
如果配置库在本地已有工作拷贝，则取得最新版本只是执行SVN Update即可，点击SVN Update，系统弹出更新提示框，点击确定，则把服务器是最新版本更新下来

03、Import（导入）
选择要提交到服务器的目录，右键选择TortoiseSVN----Import，系统弹出导入提示框，在URL of repository输入框中输入服务器仓库地址，在Import Message输入框中输入导入日志信息，点击确定，则文件导入到服务器仓库中。

04、Add(加入)
如果有多个文件及文件夹要提交到服务器，我们可以先把这些要提交的文件加入到提交列表中，要执行提交操作，一次性把所有文件提交，如图，可以选择要提交的文件，然后点击执行提交（SVN Commit）,即可把所有文件一次性提交到服务器上

05、Resolving Conflicts(解决冲突)
   有时你从档案库更新文件会有冲突。冲突产生于两人都修改文件的某一部分。解决冲突只能靠人而不是机器。当产生冲突时，你应该打开冲突的文件，查找以<<<<<<<开始的行。冲突部分被标记：
<<<<<<< filename
your changes
=======
code merged from repository
>>>>>>> revision
Subversion为每个冲突文件产生三个附加文件：
filename.ext.mine
更新前的本地文件。
filename.ext.rOLDREV
你作改动的基础版本。
filename.ext.rNEWREV
更新时从档案库得到的最新版本。
使用快捷菜单的编辑冲突Edit Conflict命令来解决冲突。然后从快捷菜单中执行已解决Resolved命令，将改动送交到档案库。请注意，解决命令并不解决冲突，而仅仅是删除filename.ext.mineandfilename.ext.r*文件并允许你送交。

06、Check for Modifications（检查更新）
点击Check for Modifications,系统列表所以待更新的文件及文件夹的状态.

07、Revision Graph(版本分支图)
查看文件的分支,版本结构,可以点击Revision Graph,系统以图形化形式显示版本分支.

08、Rename(改名)
   SVN支持文件改名,点击Rename,弹出文件名称输入框,输入新的文件名称,点击确定,再把修改提交,即可完成文件改名

09、Delete(删除)
   SVN支持文件删除,而且操作简单,方便,选择要删除的文件,点击Delete,再把删除操作提交到服务器

10、Moving(移动)
   选择待移动的文件和文件夹；按住右键拖动right-drag文件（夹）到跟踪拷贝内的新地方；松开左键；在弹出菜单中选择move files in Subversion to here

11、Revert(还原)
   还原操作,如刚才对文件做了删除操作,现在把它还原回来,点击删除后,再点击提交,会出现如上的提示框,点击删除后,再点击Revert,即已撤销删除操作,如果这时候点击提交,则系统弹出提示框:没有文件被修改或增加,不能提交

12、Branch/Tag(分支/标记)
   当需要创建分支，点击Branch/Tag，在弹出的提示框中，输入分支文件名，输入日志信息，点击确定，分支创建成功，然后可查看文件的版本分支情况

13、Switch(切换)
   文件创建分支后，你可以选择在主干工作，还是在分支工作，这时候你可以通过Switch来切换。

14、Merge(合并)
   主干和分支的版本进行合并，在源和目的各输入文件的路径，版本号，点击确定。系统即对文件进行合并，如果存在冲突，请参考冲突解决。

15、Export(导出)
   把整个工作拷贝导出到本地目录下,导出的文件将不带svn文件标志,文件及文件夹没有绿色的”√”符号标志。

16、Relocate(重新定位)
   当服务器上的文件库目录已经改变，我们可以把工作拷贝重新定位，在To URL输入框中输入新的地址

17、Add to Ignore List(添加到忽略列表)
   大多数项目会有一些文件（夹）不需要版本控制，如编译产生的*.obj, *.lst,等。每次送交，TortoiseSVN提示那些文件不需要控制，挺烦的。这时候可以把这些文件加入忽略列表。

18、SVN其它相关功能
   客户端修改用户密码:
   打开浏览器,在地址栏内输入http://192.168.1.250/cgi-bin/ChangePasswd,启动客户端修改用户密码的界面,输入正确的用户名,旧密码,新密码(注意密码的位数应该不小于6,尽量使用安全的密码),点击修改即可.

19、SVN Commit（版本提交）
把自己工作拷贝所做的修改提交到版本库中，这样别人在获取最新版本(Update)的时候就可以看到你的修改了。

20、Show log（显示日志）
显示当前文件(夹)的所有修改历史。SVN支持文件以及文件夹独立的版本追溯。

21、Repo-Browser（查看当前版本库）
查看当前版本库，这是TortoiseSVN查看版本库的入口，通过这个菜单项，我们就可以进入配置库的资源管理器，然后就可以对配置库的文件夹进行各种管理，相当于我们打开我的电脑进行文件管理一样。

22、Revision Graph（版本图形）
查看当前项目或文件的修订历史图示。如果项目比较大型的话，一般会建多个分支，并且多个里程碑（稳定版本发布），通过这里，我们就可以看到项目的全貌。

23、Resolved（解决冲突）
如果当前工作拷贝和版本库上的有冲突，不能自动合并到一起，那么当你提交修改的时候，tortoisesvn就会提示你存在冲突，这时候你就可以通过这个菜单项来解决冲突。冲突的解决有两种，一种是保留某一份拷贝，例如使用配置库覆盖当前工作拷贝，或者反过来。还有一种是手动解决冲突，对于文本文件，可以使用tortoiseSVN自带的工具，它会列出存在冲突的地方，然后你就可以和提交者讨论怎么解决这个冲突。同时它也对Word有很好的支持

24、Update to Revision(更新至版本)
从版本库中获取某一个历史版本。这个功能主要是方便查看历史版本用，而不是回滚版本。注意：获取下来之后，对这个文件不建议进行任何操作。如果你做了修改，那么当你提交的时候SVN会提示你，当前版本已失效（即不是最新版本），无法提交，需要先update一下。这样你所做的修改也就白费了。

25、Revert（回滚）
如果你对工作拷贝做了一些修改，但是你又不想要了，那么你可以使用这个选项把所做的修改撤销

26、Cleanup（清除状态）
如果当前工作拷贝有任何问题的话，可以使用这个选项进行修正。例如，有些文件原来是版本控制的，但是你没有通过tortoiseSVN就直接删除了，但是tortoiseSVN还是保留着原来的信息（每个文件夹下都有一个.svn的隐藏文件夹，存放着当前文件夹下所有文件夹的版本信息）所以这就会产生一些冲突。可以使用cleanup来清理一下。

27、GetLock/ReleaseLock（加锁/解锁）
如果你不想别人修改某个文件的话，那么你就可以把这个文件进行加锁，这样可以保证只有你对这个文件有修改权。除非你释放了锁，否则别人不可能提交任何修改到配置库中

28、Branch/tag（分支/标签）
     Branch是分支的意思。例如当在设计一个东西的时候，不同的人有不同的实现，但是没有经过实践检验，谁也不想直接覆盖掉其他人的设计，所以可以引出不同的分支。将来如果需要，可以将这些分支进行合并。
     tag是打标签的意思。通常当项目开发到一定程度，已经可以稳定运行的时候，可以对其打上一个标签，作为稳定版。将来可以方便的找到某个特定的版本（当然我们也可以使用版本号来查找，但是数字毕竟不方便）
SVN对于分支和标签都是采用类似Linux下硬链接的方式（同一个文件可以存在两个地方，删除一个不会影响另一个，所做修改会影响另一个），来管理文件的，而不是简单的复制一份文件的拷贝，所以不会有浪费存储空间的问题存在。

29、Export（导出）
这个功能是方便我们部署用。当我们需要发布一个稳定版本时，就可以使用这个功能将整个工程导出到某个文件夹，新的文件夹将不会包含任何版本信息了。

30、Relocate（版本库转移）
当我们版本库发生转移的时候就需要用到这个功能了。例如我原先的版本库是建在U盘上的，现在转移到（复制整个配置库文件夹）开发服务器上，使用https代替文件系统的访问。因此就需要将原来的工作拷贝的目标版本库重新定位到开发服务器上。

31、create patch（创建补丁）
创建补丁。如果管理员不想让任何人都随便提交修改，而是都要经过审核才能做出修改，那么其他人就可以通过创建补丁的方式，把修改信息（补丁文件）发送给管理员，管理员审核通过之后就可以使用apply patch提交这次修改了。
```

## 功能详解 2

```python
SVN命令简介

svn add [path]

别名：无
描述：添加文件或目录到你的wc，打上新增标记。这些文件会在下一次你提交wc的时候提交到svn服务器。
在提交前，你也可以用svn revert撤销新增的文件。
访问库：否
eg: svn add file.cpp

svn blame Target[@REV]
别名：praise,annotate,ann
描述：显示某个已受控文件的每一行的最后修改版本和作者
访问库：是
eg: svn blame file.cpp
eg: svn blame --xml file.cpp  ##加上xml参数可以以xml格式显示每一行的属性。

svn cat TARGET[@REV]
别名：无
描述：输出指定目标的内容，这里的目标一般是文件。
访问库：是
eg:svn cat file.cpp
eg:svn cat file.cpp -r 2 ##显示版本号为二的file.cpp内容。
eg:svn cat file.cpp --revision HEAD ##显示最新版本的file.cpp内容。


svn checkout URL[@REV]... [PATH]
别名：co
描述：检出
访问库：否
eg:svn checkout file:///var/svn/repos/test  file:///var/svn/repos/quiz working-copies
eg:svn checkout -r 2 file:///var/svn/repos/test mine  ##check out 版本号为2的项目

svn cleanup [PATH...]
别名：无
描述：递归的清理WC中过期的锁和未完成的操作。
访问库：否
eg：svn cleanup

svn commit [PATH...]
别名：ci
描述：把你WC的更改提交到仓库
访问库：是
eg：svn commit -m "added howto section." ##默认情况下提交必须提供log message

svn copy SRC[@REV]... DST
别名：cp
描述:copy操作可以从WC到WC；WC到URL；URL到WC；URL到URL。现在SVN只支持同一个仓库内文件的拷贝，不允许跨仓库操作。
访问库：是
eg：svn copy -r 11 file:///var/svn/repos/test/trunk \
           file:///var/svn/repos/test/tags/0.6.32-prerelease \
           -m "Forgot to tag at rev 11"
##copy命令是创建分支和标记的常用方式。copy到url的操作隐含了提交动作，所以需要提供log messages。

svn delete PATH...
别名：del，remove，rm
描述：删除
访问库：如果PATH是库地址时会，删除WC内的文件不会。
eg：svn del localfile.cpp    ##删除WC里的文件，在下一次提交WC的时候才会真正在仓库里将对应文件删除。
eg: svn del file:///var/svn/repos/test/yourfile  ##删除仓库里的文件

svn diff
别名：di
描述：用来比较并显示修改点。
访问库：
eg：svn diff   ##最常用的方式，用来显示WC基于最近一次更新以后的所有的本地修改点。
eg：svn diff -r 301 bin ## 比较WC和版本301中的bin目录的修改点
eg：svn diff -r 3000:3500 file:///var/svn/repos/myProject/trunk   ##比较库里主干3000版和3500版的差异。
eg：svn diff --summarize --xml http://svn.red-bean.com/repos/test@r2 http://svn.red-bean.com/repos/test  ##--summarize --xml 参数将差异情况以xml文档的方式显示出来。

svn export [-r REV] URL[@PEGREV] [PATH]
svn export [-r REV] PATH1[@PEGREV] [PATH2]
别名：无
描述：导出一个干净的目录树，不包含所有的受控信息。可以选择从URL或WC中导出。
访问库：如果访问的是URL则会。
eg：svn export file:///var/svn/repos my-export   ##导出到my-export目录。

svn help — Help!
别名：?,h
描述：不用解释了
访问库：否。

svn import [PATH] URL
别名：无
描述：导入本地一个目录到库中。但是导入后，本地的目录并不会处于受控状态。
访问库：是。
eg：svn import -m "New import" myproj http://svn.myProject.com/repos/trunk/misc

svn info [TARGET[@REV]...]
别名：无
描述：显示指定WC和URL信息。
访问库：仅当访问的是库路径时。
eg：svn info --xml http://svn.myProject.com/repos/test  ##将信息以xml格式显示。

svn list [TARGET[@REV]...]
别名：ls
描述：显示目标下的文件和目录列表。
访问库：如果访问的是库地址就会。
eg：svn list --verbose file:///var/svn/repos   ##--verbose参数表示显示详细信息。

svn lock TARGET...
别名：无
描述：对目标获得修改锁。如果目标已被其他用户锁定，则会抛出警告信息。用--force参数强制从其他用户那里获得锁。
访问库：是
eg：svn lock --force tree.jpg

svn log [PATH]
svn log URL[@REV] [PATH...]
别名：无
描述：从库中显示log消息。log消息代码 A ：added  D：deleted  M：modified  R：replaced
访问库：是
eg：svn log -v http://svn.myProject.com/repos/test/ foo.c bar.c   ##详细显示指定URL的库中foo.c和bar.c所有版本的log信息。
eg：svn log -r 14:15    ##显示当前WC的14和15版本log信息。
eg：##如果版本号不连续，只能采用如下方式。
$ svn log -r 14 > mylog
$ svn log -r 19 >> mylog
$ svn log -r 27 >> mylog


svn move SRC... DST
别名：mv, rename, ren
描述：等同于svn copy命令跟个svn delete命令。WC到URL的重命名是不被允许的。
访问库：只有当访问库地址时。
eg：svn move foo.c bar.c  ##将foo.c改名成bar.c。


svn resolve PATH...
别名：无
描述：将冲突的文件标记为已解决，并且删掉冲突产生的临时文件。注意这个命令并不是能把冲突解决，解决冲突还是得靠人工。
访问库：否
eg：svn resolve --accept mine-full foo.c   ##1.5版本后，加上--accept参数，尝试自动处理冲突。

svn resolved PATH...
别名：无
描述：已过时，被resolve --accept取代。去除冲突的状态和冲突临时文件。
访问库：否

svn revert PATH...
别名：无
描述：还原WC中所有的本地更改。
访问库：否
eg：svn revert --depth=infinity .   ##将整个目录所有文件还原

svn status [PATH...]
别名：stat, st
描述：输出WC中文件和目录的状态。如果WC提交，这些状态就会同步到库里。
一般状态有         ' '  没有修改
'A'  新增
'D'  删除
'M'  修改
'R'  替代
'C'  冲突
'I'  忽略
'?'  未受控
'!'  丢失，一般是将受控文件直接删除导致
访问库：加上--show-updates参数时会
eg：svn status wc

svn switch URL[@PEGREV] [PATH]
svn switch --relocate FROM TO [PATH...]
别名：sw
描述：将WC转向一个其他的库地址同步
访问库：是
eg：svn sw http://svn.myProject.com/repos/trunk/vendors .  ##将当前WC切换到另一个URL

svn unlock TARGET...
别名：无
描述：解锁
访问库：是
eg：svn unlock somefile

svn update [PATH...]
别名：up
描述：更新WC，更新反馈有如下几种分类。
        A  新增
B  锁破坏
D  删除
U  更新
C  冲突
G  合并
E  存在的
访问库：是
eg：svn up -r22   ##更新到一个指定版本

ps:如何去除SVN中保存的用户授权密码
在Subversion安装目录下找到auth/svn.simple目录，将下面的文件删除即可。
如果在乌龟中，可以setting->saved data->Authentication Data   点 clear 即可。

参考资料：http://svnbook.red-bean.com/en/1.5/svn.ref.svn.c.checkout.html
```

## 功能详解 3

```python
**
*  转载请注明作者longdick    http://longdick.javaeye.com
*
*/

SVN版本：1.5 及更新版本
名词说明：
WC：Working Copy 你的工作区
Versioned：受控的；受版本控制的

SVN是什么？

	*
SVN是开源的版本控制系统。
	*
比CVS更多的特性。一个更好的CVS？因此SVN具有大部分CVS拥有的特性。
	*
不仅仅是文件受控，目录也加入版本控制。
	*
复制，删除，重命名这些操作都是受控的。
	*
特殊作用的元数据（属性）。
	*
提交事务原子性。提交完成之前任何一个部分都不会正真生效。版本号基于提交，而不是基于文件。提交时的log message也是依附于提交的那个版本。
	*
创建分支和标记非常简单。简单的通过copy命令就可以创建分支和标记。
	*
合并跟踪。在合并时协助你处理所有的更改点。
	*
文件锁定。svn支持文件锁定修改策略。
	*
Unix的link可以受控了。前提是WC必须在Unix下。
	*
可选的Apache network server，基于WEBDAV/DeltaV 协议。熟悉Apache的管理员会很喜欢这一点。
	*
内置的server选择（svnserve）。如果不想用Apache，可以试试Svn自己的server：svnserve。同样也能提供授权和验证，ssh通道等功能。
	*
方便解析的输出。svn的输出尽量做到方便阅读和方便机器解析。
	*
冲突解决交互性良好。svn命令行客户端提供多种不同的方式解决冲突。
	*
svn提供一个实用工具，svnsync来实现从主库到只读附属库的同步。
	*
持续写入代理功能让只读的附属库专门处理所有的读请求。所有的写请求交给主库处理。这个功能只在使用Apache WebDAV server的时候才有效。
	*
基于本地化的客户机服务器体系，分层的库，明晰的API方便扩展。
	*
高效处理二进制文件。
	*
性能消耗与更改点的数量成正比。
	*
svn的api可以和多种语言集成。Python，Perl,Java,Ruby（svn本身是用C写的）
	*
ChangeLists功能。


Svn的安装分客户端和服务端。
你可以在如下地址找到下载：http://subversion.tigris.org/
这篇文章主要介绍的是svn客户端的命令，你至少需要安装客户端。默认就是以SVN做版本控制的。如果你不想在自己机器上安装服务版，google code是个练习svn命令的好地方。
http://code.google.com上申请托管项目很简单，但是现在不支持svn lock。目前最大支持1G空间。

以下是svn客户端常用命令一览：

svn add [path]
别名：无
描述：添加文件或目录到你的wc，打上新增标记。这些文件会在下一次你提交wc的时候提交到svn服务器。
在提交前，你也可以用svn revert撤销新增的文件。
访问库：否
eg: svn add file.cpp

svn blame Target[@REV]
别名：praise,annotate,ann
描述：显示某个已受控文件的每一行的最后修改版本和作者
访问库：是
eg: svn blame file.cpp
eg: svn blame --xml file.cpp  ##加上xml参数可以以xml格式显示每一行的属性。

svn cat TARGET[@REV]
别名：无
描述：输出指定目标的内容，这里的目标一般是文件。
访问库：是
eg:svn cat file.cpp
eg:svn cat file.cpp -r 2 ##显示版本号为二的file.cpp内容。
eg:svn cat file.cpp --revision HEAD ##显示最新版本的file.cpp内容。

svn changelist CLNAME TARGET...
svn changelist --remove TARGET
别名：cl
描述：可以将wc中的文件从逻辑上分组.
访问库：否
eg:svn cl clName file.cpp file2.cpp file3.cpp  ##将file.cpp等三个文件加入名叫clName的changelist
eg:svn commit --changelist clName -m "ci"  ##将clName下的所有文件提交

svn checkout URL[@REV]... [PATH]
别名：co
描述：检出
访问库：否
eg:svn checkout file:///var/svn/repos/test  file:///var/svn/repos/quiz working-copies
eg:svn checkout -r 2 file:///var/svn/repos/test mine  ##check out 版本号为2的项目

svn cleanup [PATH...]
别名：无
描述：递归的清理WC中过期的锁和未完成的操作。
访问库：否
eg：svn cleanup

svn commit [PATH...]
别名：ci
描述：把你WC的更改提交到仓库
访问库：是
eg：svn commit -m "added howto section." ##默认情况下提交必须提供log message

svn copy SRC[@REV]... DST
别名：cp
描述:copy操作可以从WC到WC；WC到URL；URL到WC；URL到URL。现在SVN只支持同一个仓库内文件的拷贝，不允许跨仓库操作。
访问库：是
eg：svn copy -r 11 file:///var/svn/repos/test/trunk \
           file:///var/svn/repos/test/tags/0.6.32-prerelease \
           -m "Forgot to tag at rev 11"
##copy命令是创建分支和标记的常用方式。copy到url的操作隐含了提交动作，所以需要提供log messages。

svn delete PATH...
别名：del，remove，rm
描述：删除
访问库：如果PATH是库地址时会，删除WC内的文件不会。
eg：svn del localfile.cpp    ##删除WC里的文件，在下一次提交WC的时候才会真正在仓库里将对应文件删除。
eg: svn del file:///var/svn/repos/test/yourfile  ##删除仓库里的文件

svn diff
别名：di
描述：用来比较并显示修改点。
访问库：
eg：svn diff   ##最常用的方式，用来显示WC基于最近一次更新以后的所有的本地修改点。
eg：svn diff -r 301 bin ## 比较WC和版本301中的bin目录的修改点
eg：svn diff -r 3000:3500 file:///var/svn/repos/myProject/trunk   ##比较库里主干3000版和3500版的差异。
eg：svn diff --summarize --xml http://svn.red-bean.com/repos/test@r2 http://svn.red-bean.com/repos/test  ##--summarize --xml 参数将差异情况以xml文档的方式显示出来。

svn export [-r REV] URL[@PEGREV] [PATH]
svn export [-r REV] PATH1[@PEGREV] [PATH2]
别名：无
描述：导出一个干净的目录树，不包含所有的受控信息。可以选择从URL或WC中导出。
访问库：如果访问的是URL则会。
eg：svn export file:///var/svn/repos my-export   ##导出到my-export目录。

svn help — Help!
别名：?,h
描述：不用解释了
访问库：否。

svn import [PATH] URL
别名：无
描述：导入本地一个目录到库中。但是导入后，本地的目录并不会处于受控状态。
访问库：是。
eg：svn import -m "New import" myproj http://svn.myProject.com/repos/trunk/misc

svn info [TARGET[@REV]...]
别名：无
描述：显示指定WC和URL信息。
访问库：仅当访问的是库路径时。
eg：svn info --xml http://svn.myProject.com/repos/test  ##将信息以xml格式显示。

svn list [TARGET[@REV]...]
别名：ls
描述：显示目标下的文件和目录列表。
访问库：如果访问的是库地址就会。
eg：svn list --verbose file:///var/svn/repos   ##--verbose参数表示显示详细信息。

svn lock TARGET...
别名：无
描述：对目标获得修改锁。如果目标已被其他用户锁定，则会抛出警告信息。用--force参数强制从其他用户那里获得锁。
访问库：是
eg：svn lock --force tree.jpg

svn log [PATH]
svn log URL[@REV] [PATH...]
别名：无
描述：从库中显示log消息。log消息代码 A ：added  D：deleted  M：modified  R：replaced
访问库：是
eg：svn log -v http://svn.myProject.com/repos/test/ foo.c bar.c   ##详细显示指定URL的库中foo.c和bar.c所有版本的log信息。
eg：svn log -r 14:15    ##显示当前WC的14和15版本log信息。
eg：##如果版本号不连续，只能采用如下方式。
$ svn log -r 14 > mylog
$ svn log -r 19 >> mylog
$ svn log -r 27 >> mylog

svn merge sourceURL1[@N] sourceURL2[@M] [WCPATH]
svn merge sourceWCPATH1@N sourceWCPATH2@M [WCPATH]
svn merge [[-c M]... | [-r N:M]...] [SOURCE[@REV] [WCPATH]]
别名：无
描述：合并两个受控源的不同之处，存放到一个WC里。
访问库：只有当访问库地址时。
eg：svn merge --reintegrate http://svn.example.com/repos/calc/branches/my-calc-branch  ##合并分支上的改变项到WC，往往用于分支合并到主干。
eg：svn merge -r 156:157 http://svn.example.com/repos/calc/branches/my-calc-branch   ##将制定URL版本156到157的所有更新合并到WC。

svn mkdir PATH...
svn mkdir URL...
别名：无
描述：在WC或库路径创建目录
访问库：只有当访问库地址时。
eg：svn mkdir newdir

svn move SRC... DST
别名：mv, rename, ren
描述：等同于svn copy命令跟个svn delete命令。WC到URL的重命名是不被允许的。
访问库：只有当访问库地址时。
eg：svn move foo.c bar.c  ##将foo.c改名成bar.c。

svn propdel PROPNAME [PATH...]
svn propdel PROPNAME --revprop -r REV [TARGET]
别名：pdel, pd
描述：从受控文件，目录等删除属性。第二种是删除某个指定版本上的附加属性。
访问库：只有当访问库地址时。
eg：svn propdel svn:mime-type someFile    ##从someFile上移除svn:mime-type这个属性。

svn propedit PROPNAME TARGET...
svn propedit PROPNAME --revprop -r REV [TARGET]
别名：pedit, pe
描述：编辑属性
访问库：只有当访问库地址时。
eg：svn propedit svn:keywords  file.c  ##修改file.c上的svn:keywords属性。

svn propget PROPNAME [TARGET[@REV]...]
svn propget PROPNAME --revprop -r REV [URL]
别名：pget,pg
描述：从文件，目录或版本取得指定属性的值。
访问库：只有当访问库地址时。
eg：svn propget svn:keywords file.c   ##从file.c中取得svn:keywords属性的值

svn proplist [TARGET[@REV]...]
svn proplist --revprop -r REV [TARGET]
别名：plist, pl
描述：列出文件、目录或版本上的所有附加属性
访问库：只有当访问库地址时。
eg：svn proplist --verbose file.c

svn propset PROPNAME [PROPVAL | -F VALFILE] PATH...
svn propset PROPNAME --revprop -r REV [PROPVAL | -F VALFILE] [TARGET]
别名：pset,ps
描述：给文件、目录或版本附加属性并赋值
访问库：只有当访问库地址时。
eg：svn propset svn:mime-type image/jpeg file.jpg   ##给file.jpg附加属性svn:mime-type 其值为image/jpeg
eg:svn propset --revprop -r 25 svn:log "Journaled about trip to New York."
##给版本25补上log message
eg:svn propset svn:ignore '.classpath' .
##在本地忽略掉.classpath文件

svn resolve PATH...
别名：无
描述：将冲突的文件标记为已解决，并且删掉冲突产生的临时文件。注意这个命令并不是能把冲突解决，解决冲突还是得靠人工。
访问库：否
eg：svn resolve --accept mine-full foo.c   ##1.5版本后，加上--accept参数，尝试自动处理冲突。

svn resolved PATH...
别名：无
描述：已过时，被resolve --accept取代。去除冲突的状态和冲突临时文件。
访问库：否

svn revert PATH...
别名：无
描述：还原WC中所有的本地更改。
访问库：否
eg：svn revert --depth=infinity .   ##将整个目录所有文件还原

svn status [PATH...]
别名：stat, st
描述：输出WC中文件和目录的状态。如果WC提交，这些状态就会同步到库里。
一般状态有         ' '  没有修改
'A'  新增
'D'  删除
'M'  修改
'R'  替代
'C'  冲突
'I'  忽略
'?'  未受控
'!'  丢失，一般是将受控文件直接删除导致
访问库：加上--show-updates参数时会
eg：svn status wc

svn switch URL[@PEGREV] [PATH]
svn switch --relocate FROM TO [PATH...]
别名：sw
描述：将WC转向一个其他的库地址同步
访问库：是
eg：svn sw http://svn.myProject.com/repos/trunk/vendors .  ##将当前WC切换到另一个URL

svn unlock TARGET...
别名：无
描述：解锁
访问库：是
eg：svn unlock somefile

svn update [PATH...]
别名：up
描述：更新WC，更新反馈有如下几种分类。
        A  新增
B  锁破坏
D  删除
U  更新
C  冲突
G  合并
E  存在的
访问库：是
eg：svn up -r22   ##更新到一个指定版本

ps:如何去除SVN中保存的用户授权密码
在Subversion安装目录下找到auth/svn.simple目录，将下面的文件删除即可。
如果在乌龟中，可以setting->saved data->Authentication Data   点 clear 即可。


参考资料：http://svnbook.red-bean.com/en/1.5/svn.ref.svn.c.checkout.html
```

## 功能模块

## SVN EXCEL 比对工具

## SVN WORD 比对工具

### SVN 创建分支

```bash
# copy trunk
svn copy svn://127.0.0.1/repos/trunk svn://127.0.0.1/repos/tags/suzhou-prod-1.1.1.190920_release -m "创建tags suzhou-prod-1.1.1.190920_release"
# 在其中修改提交即可 提交到单独的分支 branchs/branch_01

如果SVN中显示
(env) [scfan@scfan tags]$ svn st suzhou-prod-1.1.1.190920_release
?       suzhou-prod-1.1.1.190920_release
但是里面内容已经提交了
mv suzhou-prod-1.1.1.190920_release suzhou-prod-1.1.1.190920_release_bak
svn up 即可
```

### 提交时 忽略文件/文件夹

@创建日期: 2018-06-28
@创建作者: scfan

**方法 1: 配置忽略文件**
对版本库修改，客户端无影响。

```python
步骤1：配置SVN默认编辑器
vi ~/.bash_profile
最后一行加上：
export SVN_EDITOR=vim  # 定义svn editor为vim编辑

步骤2：让配置生效
source ~/.bash_profile

步骤3.设置忽略文件：
先切换到项目目录，如test
输入：
svn propedit svn:ignore .  #‘.’号需加上，代表当前目录；
输入需要忽略的文件/文件夹
如：
conf/db.php   #代表忽略conf文件下db.php这个文件
uploads       #代表忽略uploads这个文件夹
以上忽略的文件都是该项目目录的相对路径！

步骤4：检验忽略是否成功
然后使用svn st查看，会显示：
M       conf/db.php
我们需要提交，然后这个svn:ignore属性才会起作用

svn ci -m '忽略test.php文件'

这时候，无论你如何修改conf/db.php文件，再使用svn st时，也不会出现修改提示
符合M了。
```

**方法 2：配置客户端**
对客户端修改，版本库无影响。

```python
svn 客户端的配置
对 svn 命令的配置文件修改即可。进入个人用户目录
$ vim .subversion/config
找到包含  [miscellany] 这一行，取消注释，然后编辑包含 global-ignores 的那一行，取消注释，并添加需要过滤文件的通配符即可。如下所示：注意开头不能有空格，否则svn会报错。

global-ignores = *.so *.a *.o *.lo *.la .*.rej *.rej .*~ *~ .#* .DS_Store

这个配置是对客户端的修改，对版本库没有任何影响。同时，这个配置也是全局的，适用于本机所有 svn 管理的项目。
```
