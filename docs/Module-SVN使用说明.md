# Linux-SVN使用说明



## SVN EXCEL比对工具

## SVN WORD比对工具





### SVN创建分支
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