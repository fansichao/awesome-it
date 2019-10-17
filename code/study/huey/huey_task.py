#! -*- coding:utf-8 -*-
u""" HueyTask 

记录Huey中的Tasks


"""
import datetime
import peewee

from huey_tools import huey, crontab
from huey import CancelExecution
from huey.signals import SIGNAL_ERROR, SIGNAL_LOCKED

def huey_add_task(huey, func, retries=0, retry_delay=0, priority=None, context=False, name=None, **kwargs):
    u"""向huey中添加task
        
    """
    # ... https://huey.readthedocs.io/en/latest/troubleshooting.html
    # HueyException: __main__.minus not found in TaskRegistry
    # 无法后续创建taskwarapper. taskwarapper必须被导入
    # TODO
    taskwrapper = huey.task(retries=0, retry_delay=0, priority=None, context=False,  **kwargs)(func)
    return taskwrapper 


@huey.task(retries=0,retry_delay=0,priority=None,context=False,name=None)
# 利用存储键/值API来实现简单的锁定
@huey.lock_task('reports-lock')
def add(a, b):
    u"""
        # TaskWrapper任务
        # retries 重试次数
        # retry_delay 重试之间等待的秒数
        # priority 优先级
        # context 执行任务时,将Task实例作为关键字参数包含在内 
        # name 此任务的名称。如果未提供,Huey将默认使用模块名称加函数名称
    """
    print(u">> 调用任务add")
    return a + b


# priority 优先级默认0,最高100
@huey.periodic_task(crontab(minute='3', hour='0'),retries=0,retry_delay=0,priority=None,context=False,name=None)
def minus(a, b):
    u"""
        # TaskWrapper定期任务
        # crontab(minute='3', hour='0') 指定定时时间 每三分钟执行一次
    """
    print("调用定期任务")
    return a-b
    

@huey.pre_execute(name="preA")
def pre_execute_hook(task):
    u"""执行前
    
    # pre_execute 指定执行前挂钩的名称
    """
    print(u">> [%s]执行前"%datetime.datetime.now())

    if datetime.datetime.now().weekday() == 6:
        raise CancelExecution('No tasks on sunday!')

    return task

@huey.post_execute(name="postA")
def post_execute_hook(task, task_value, exc):
    u"""执行后
    # post_execute 指定执行后挂钩的名称
    """
    print(u">> [%s]执行后"%datetime.datetime.now())
    if exc is not None:
        print('Task "%s" failed with error: %s!' % (task.id, exc))

    return task


db_connection = None
# on_startup: 注册一个启动挂钩。每当工作人员联机时,将执行回调
@huey.on_startup(name="startupA")
def setup_db_connection():
    pass
    global db_connection
    # db_connection = psycopg2.connect(database='my_db')


# 信号
@huey.signal(SIGNAL_ERROR, SIGNAL_LOCKED)
def task_not_run_handler(signal, task, exc=None):
    pass

# 缓存任意键/值数据
@huey.task()
def calculate_something():
    # By default, the result store treats get() like a pop(), so in
    # order to preserve the data so it can be read again, we specify
    # the second argument, peek=True.
    prev_results = huey.get('calculate-something.result', peek=True)
    if prev_results is None:
        # No previous results found, start from the beginning.
        data = start_from_beginning()
    else:
        # Only calculate what has changed since last time.
        data = just_what_changed(prev_results)

    # We can store the updated data back in the result store.
    huey.put('calculate-something.result', data)
    # data2 = huey.get('calculate-something.result')
    return data


def huey_obj_exp(huey, taskwrapper=None,*args,**kwargs):
    u"""Huey实例对象样例
    """
    print ">>>>. huey_instance_res"

    # Task等待运行的实例列表
    print huey.pending(limit=None)
    # Task计划在将来某个时间执行的实例的列表
    print huey.scheduled(limit=None)
    # 结果存储区中所有键/值对的序列化结果数据的task-id字典
    print huey.all_results()
    # 返回当前在队列中的项目数。
    print huey.__len__()

    if taskwrapper:
        # 将任务加入队列中
        huey.enqueue(taskwrapper.s(*args,**kwargs))


now = datetime.datetime.now()
eta = now + datetime.timedelta(seconds=3)


def res_obj_exp(res, blocking=True):
    u""" res对象样例 
    """
    print ">>>>. res_instance"
    result = res(blocking=blocking)

    # 返回相应任务的唯一ID
    print res.id
    # 尝试检索任务的返回值
    print res.get()
    # 撤销给定的任务。除非它在执行过程中,否则该任务将被丢弃而不执行
    res.revoke(revoke_once=True)
    # 恢复给定的任务实例。除非任务实例已经出队并被丢弃,否则它将还原并按计划运行。
    res.restore()
    # 检查是否已被吊销
    print res.is_revoked()
    # 重新安排给定的任务。原始任务实例将被吊销,但不会进行任何检查以确认它尚未执行。
    # 如果既未指定etaa delay也未指定a,则该任务将在工作者收到任务后立即运行
    res.reschedule(eta = None,delay = None)
    # 重置缓存的结果,并允许重新获取给定任务的新结果（即在任务错误和随后的重试之后）
    print res.reset()

    return result



def taskwrapper_obj_exp(taskwrapper,*args,**kwargs):
    u""" Huey.task()与Huey.periodic_task() 装饰会自动创建相应的TaskWrapper
    """
    print ">>>>. taskwrapper_obj_exp"

    
    # args（tuple）–装饰函数的参数。
    # kwargs（dict）–装饰函数的关键字参数。
    # eta（datetime）–应该执行功能的时间。
    # delay（int）–执行功能之前要等待的秒数
    res = taskwrapper.schedule(args=(1,2),kwargs=None,eta=None,delay = 2)
    
    # 撤销任务
    # revoke_until（datetime）–在给定的datetime之后自动还原任务。
    # revoke_once（bool）–撤销任务的下一次执行,然后自动还原。
    taskwrapper.revoke(revoke_until = None,revoke_once = False)

    # 检查是否撤销
    taskwrapper.is_revoked()
    # 删除先前的任务吊销
    taskwrapper.restore()

    # 直接调用原有函数
    print taskwrapper.call_local(*args,**kwargs)

    
    # 创建一个Task实例,该实例使用给定的参数和关键字参数来调用任务函数。返回的任务实例不会自动排队。
    taskwrapper.s(*args,**kwargs)
    
    
    pass

# 信号处理器
@huey.signal()
def print_signal_args(signal, task, exc=None):
    # 打印信号名称和相关任务的ID
    if signal == "SIGNAL_ERROR":
        print('%s - %s - exception: %s' % (signal, task.id, exc))
    else:
        print('%s - %s' % (signal, task.id))



@huey.task(retries=3)
def run_bash_task(cmd, std_out, working_dir):
    print("Entring %s" % working_dir)
    print("Running command %s, stdout to %s" % (cmd, std_out))
    os.chdir(working_dir)
    if std_out is None:
        subprocess.check_call(cmd)
    else:
        with open(std_out, "w") as f:
            subprocess.check_call(cmd, stdout=f)
    print("finish task %s\n" % cmd)


if __name__ == '__main__':
    pass

