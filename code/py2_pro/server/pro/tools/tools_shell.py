#! -*- coding:utf-8 -*-
u""" Linux Bash Xshell 相关命令
    
"""
from .base_import import *

def run_cmd(cmd=None):
    os.system(cmd)

# Shell按日期循环
cmd001 = """
#! /bin/bash
start_date=20151101
end_date=20151103
start_sec=`date -d "$start_date" "+%s"`
end_sec=`date -d "$end_date" "+%s"`
for((i=start_sec;i<=end_sec;i+=86400)); do
    day=$(date -d "@$i" "+%Y-%m-%d")
    echo $day
done
"""
cmd002 = """
#! /bin/bash
start='2016-01-01'
# end=`date -d "1 day ${end}" +%Y-%m-%d`  # 日期自增
end='2016-01-03'

while [ "${start}" != "${end}" ]
do
  echo ${start}
  start=`date -d "1 day ${start}" +%Y-%m-%d`    # 日期自增
done
"""


# >>>>>>>>>>>>>>>>>>>>>>> 测试运行
def test():
    cmds = [cmd001,cmd002]
    for cmd in cmds:
        run_cmd(cmd)


