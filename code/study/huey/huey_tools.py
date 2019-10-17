#! -*- coding:utf-8 -*-
u""" HueyTools 包含Huey对象的模块

"""
import time
import datetime
import functools
import subprocess
import os

import sqlite3
import huey
from huey import RedisHuey, crontab, SqliteHuey


# Huey配置文件
HUEY_CONFIG = {
    # Huey 使用的底层服务 sqlite/redis
    'HUEY_SERVICE_DTYPE': 'sqlite',
    'HUEY_SERVICE_NAME': '/tmp/fdm.db',
    'HUEY_SERVICE_PORT': '6379',
    'HUEY_SERVICE_HOST': '0.0.0.0',
    'HUEY_SERVICE_IMMEDIATE': True,
    # Huey
}

# 开发者模式
develop = True
HUEY_SERVICE_IMMEDIATE = True if develop else False
HUEY_CONFIG['HUEY_SERVICE_IMMEDIATE'] = HUEY_SERVICE_IMMEDIATE


def huey_init(name=None, host=None, port=None, dtype=None, immediate=False):
    u""" 初始化 huey

    :param str name: Sqlite3数据文件路径/Redis名称
    :param str host: RedisIP地址
    :param int port: Redis端口
    :param str dtype: 指定Sqlite/Redis类型
    :param bool immediate: 运行模式，立即模式开启与否
        在测试和开发过程中非常有用,Huey将立即执行任务功能而不是将它们排队，
        同时仍保留运行专用消费者进程时所期望的API和行为.
        立即模式在启用时切换到内存存储。
        如果立即模式未开启时，不会立即执行，而是加入任务队列中，等待调度执行。
    """
    name = name if name is not None else HUEY_CONFIG.get('HUEY_SERVICE_NAME')
    dtype = dtype if dtype is not None else HUEY_CONFIG.get('HUEY_SERVICE_DTYPE')
    host = host if host is not None else HUEY_CONFIG.get('HUEY_SERVICE_HOST')
    port = port if port is not None else HUEY_CONFIG.get('HUEY_SERVICE_PORT')
    immediate = immediate if immediate is not None else HUEY_CONFIG.get('HUEY_SERVICE_IMMEDIATE')

    if dtype.lower() == 'redis':
        huey = RedisHuey(name, host=host, port=int(port))
        # RedisHuey 不支持任务优先级
        # PriorityRedisHuey 支持任务优先级，要求版本 5.0+
    else:
        # 'SqliteHuey' 不支持  'huey_lock'
        huey = SqliteHuey(filename=name)
    huey.immediate = immediate
    return huey

huey = huey_init()


def huey_tools_task(func, task_name=None, huey_periodic=False, huey_crontab=None, huey_retries=1, huey_retry_delay=1,
                    huey_priority=0, huey_lock=False, huey_lock_msg=''):
    u""" 添加 Huey Worker. 对 Huey 进行封装

    :param func: 函数实体。
    :parma task_name: 任务名称. 显示在 huey 中
    :params huey_periodic: 是否定期执行任务
    :param huey_crontab: 定时设置
    :param int huey_retries: 失败重试次数
    :parma int huey_retry_delay: 失败重试延迟时间 秒
    :param int huey_priority: 任务优先级.任务优先级仅影响从待处理任务队列中提取任务的顺序
    :param bool huey_lock: 是否锁定任务，此锁可防止多个任务调用同时运行。
    :param str huey_lock_msg: 锁定任务信息
    :param bool huey_canel: 是否取消/暂定任务

    """
    data = func
    task_name = task_name if task_name is not None else data.func_name


    # 是否定期任务
    if huey_periodic:
        huey_crontab = huey_crontab if huey_crontab is not None else crontab(minute='0', hour='*/3')
        data = huey.periodic_task(huey_crontab, retries=huey_retries, retry_delay=huey_retry_delay,
                                  name=task_name,
                                  priority=huey_priority)(
            data)
    else:
        data = huey.task(name=task_name, retries=huey_retries, retry_delay=huey_retry_delay,
                         priority=huey_priority)(data)

    # 是否锁住 worker
    if huey_lock:
        data = huey.huey_lock(huey_lock_msg)(data)

    return data


def task_revoke(func, restore=False, revoke_once=None, revoke_until=None):
    u""" 任务处理

    :param func: 任务实体
    :param restore: 是否恢复
    :param revoke_once: 取消下一次，之后自动恢复
    :param revoke_until: 指定恢复的时间 datetime

    如果任务尚未开始执行，则可以取消（“撤销”）任何任务。
    类似地，可以恢复已撤销的任务，前提是它尚未被消费者处理和丢弃

    定期任务 取消/暂停
    # 取消下一次，之后自动恢复
    send_notification_emails.revoke(revoke_once=True)
    # 指定恢复的时间 datetime
    send_notification_emails.revoke(revoke_until=eta)

    可以使用 restore() 恢复任务
    is_revoked 检查状态

    """
    # 取消任务

    func.revoke(revoke_once=revoke_once, revoke_until=revoke_until)
    print "取消任务[%s]" % func.name

    # 检查取消状态
    func.is_revoked()
    # 恢复任务
    if restore:
        func.restore()



if __name__ == '__main__':
    pass

