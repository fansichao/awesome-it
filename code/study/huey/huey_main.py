#! -*- coding:utf-8 -*-
u""" 调用模块


"""
import uniout

from huey_tools import huey
from huey_task import add, minus, pre_execute_hook, post_execute_hook, setup_db_connection
from huey_task import huey_obj_exp,res_obj_exp,taskwrapper_obj_exp,print_signal_args


# 注销指定的执行前挂钩
#huey.unregister_pre_execute(pre_execute_hook)
# 注销指定的执行后挂钩
# huey.unregister_post_execute(pre_execute_hook)
#huey.unregister_pre_execute("xxxA")

if __name__ == '__main__':
    taskwrapper = add 
    res = taskwrapper(1,2)
    
    huey_obj_exp(huey, taskwrapper,a=1,b=2)
    res_obj_exp(res)
    taskwrapper_obj_exp(taskwrapper,a=1,b=2)

