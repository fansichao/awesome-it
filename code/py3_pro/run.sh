# Git 初始化使用
git_init(){
    # 删除远程库链接
    git remote rm origin
    # 链接远程库
    git remote add origin git@github.com:fansichao/py3_pro.git
}

# Git 日常使用
git_daily(){
    # 更新
    git pull
    # 日常使用
    git add * 
    git commit -m "update" -a
    git push -u origin master
}

# 日常使用
Daily(){
    # Env 进入虚拟环境
    source ~/env3/bin/activate 
    # Git 日常使用
    git_daily

}
#git_init
Daily
