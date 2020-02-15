# Linux-Git使用手册.md

## GitHub插入MarkDown图片

```bash
原链接:https://github.com/fansichao/awesome-it/blob/master/images/Linux-Nosetests02静态类图.png
将blob 修改为 raw 即可
![xxx](https://github.com/fansichao/awesome-it/raw/master/images/Linux-Nosetests02静态类图.png)
```

![xxx](https://github.com/fansichao/awesome-it/raw/master/images/Linux-Nosetests02静态类图.png)

## Github常用脚本

使用脚本

```python
# ">>>>>>>>>>>>> Base_Func >>>>>>>>>>>>>>>>>>>"
git_init(){
    # 删除远程库链接
    git remote rm origin
    # 链接远程库
    git remote add origin git@github.com:fansichao/code.git
}

# Git 日常使用
git_daily(){
    # 更新
    git pull
    # 日常使用
    git add * 
    git commit -m "定时提交" -a
    git push -u origin master
}

# ">>>>>>>>>>>>> Using_Func >>>>>>>>>>>>>>>>>>>"
# 日常使用
Daily(){
    # Env 进入虚拟环境
    source ~/env/bin/activate 
    # Git 日常使用
    git_daily

}
# Git 初始化使用
#git_init
Daily
```

## 命令大全

TODO