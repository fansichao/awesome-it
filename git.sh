# ">>>>>>>>>>>>> Base_Func >>>>>>>>>>>>>>>>>>>"
git_init(){
    # 删除远程库链接
    git remote rm origin
    # 链接远程库
    git remote add origin git@github.com:fansichao/awesome-it.git
}

# Git 日常使用
git_daily(){
    # 更新
    git pull
    # 日常使用
    git add * --all
    git commit -m "定时提交" -a
    git push -u origin master
}

# ">>>>>>>>>>>>> Using_Func >>>>>>>>>>>>>>>>>>>"
# 日常使用
Daily(){
    # Env 进入虚拟环境
    #source ~/env/bin/activate
    # Git 日常使用
    git_daily

}
# Git 初始化使用
#git_init
Daily


