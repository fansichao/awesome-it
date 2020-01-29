# Huey 使用手册

环境依赖

- Python2.7+ or Python3.4+

[Huey官网](https://huey.readthedocs.io/en/latest/)

## Huey简介

一个轻量Python2.7+ Python3.4+ 轻巧的消息队列.

## 功能说明

huey支持：

- 多进程，多线程或greenlet任务执行模型
- 安排任务在给定时间或在给定延迟后执行
- 安排重复任务，例如crontab
- 自动重试失败的任务
- 任务优先级
- 任务结果存储
- 任务锁定
- 任务管道和链

不支持项:

- Huey服务异常,异常服务无法继续运行，需要重新运行。(根据任务队列进行运行。)
- 不支持彻底取消，即任务永不使用。
- 无法暂定任务。任务尚未开始时，可以取消和撤销，任务已经进行后，无法取消。
- 定时任务精准度为分钟，无法精确到秒。

Huey对象:

- Huey          Huey实例
- TaskWrapper   不需要TaskWrapper直接创建实例。在Huey.task()与Huey.periodic_task() 装饰会自动创建相应的TaskWrapper。
- Task          所述Task类表示的函数的执行。任务的实例被序列化并排入队列以供使用者执行，消费者反序列化并执行任务功能 
- Result        结果

[Huey启动参数](https://huey.readthedocs.io/en/latest/consumer.html): 保证huey的稳定持续启动,附带Worker检查等参数

## 安装部署

### 安装Huey

```bash
pip install huey
```

### 安装Redis

详见 "Module-Redis文档"


### 安装Sqlite3

```bash
yum install sqlite -y
```

### 软件使用

```bash
# 启动 Redis
redis-server /etc/redis.conf  

# 启动 Huey 命令
huey_consumer.py huey_task.huey -l /var/log/app.huey.log -k process -w 2 -q -c 100 -m 10 -v

# 运行 指定task任务
python huey_main.py

(env) [scfan@scfan huey]$ huey_consumer.py huey_main.huey -k process -w 2  1

[2019-10-04 17:46:21,985] INFO:huey.consumer:11137:Huey consumer started with 2 process, PID 11137 at 2019-10-04 09:46:21.985333
[2019-10-04 17:46:21,985] INFO:huey.consumer:11137:Scheduler runs every 1 second(s).
[2019-10-04 17:46:21,985] INFO:huey.consumer:11137:Periodic tasks are enabled.
[2019-10-04 17:46:21,986] INFO:huey.consumer:11137:The following commands are available:
+ huey_task.add_numbers_10
+ huey_task.add_numbers_20
```

## 问题记录

### DENIED Redis is running in protected mode

```bash
ResponseError: DENIED Redis is running in protected mode because protected mode is enabled, no bind address was specified, no authentication password is requested to clients. In this mode connections are only accepted from the loopback interface. If you want to connect from external computers to Redis you may adopt one of the following solutions: 1) Just disable protected mode sending the command 'CONFIG SET protected-mode no' from the loopback interface by connecting to Redis from the same host the server is running, however MAKE SURE Redis is not publicly accessible from internet if you do so. Use CONFIG REWRITE to make this change permanent. 2) Alternatively you can just disable the protected mode by editing the Redis configuration file, and setting the protected mode option to 'no', and then restarting the server. 3) If you started the server manually just for testing, restart it with the '--protected-mode no' option. 4) Setup a bind address or an authentication password. NOTE: You only need to do one of the above things in order for the server to start accepting connections from the outside.
[2019-10-04 10:31:51,683] ERROR:huey.consumer.Worker:32427:Error reading from queue
Traceback (most recent call last):
  File "/home/scfan/env/lib/python2.7/site-packages/huey/consumer.py", line 94, in loop
    task = self.huey.dequeue()
  File "/home/scfan/env/lib/python2.7/site-packages/huey/api.py", line 282, in dequeue
    data = self.storage.dequeue()
  File "/home/scfan/env/lib/python2.7/site-packages/huey/storage.py", line 423, in dequeue
    timeout=self.read_timeout)[1]
  File "/home/scfan/env/lib/python2.7/site-packages/redis/client.py", line 1635, in brpop
    return self.execute_command('BRPOP', *keys)
  File "/home/scfan/env/lib/python2.7/site-packages/redis/client.py", line 839, in execute_command
    return self.parse_response(conn, command_name, **options)
  File "/home/scfan/env/lib/python2.7/site-packages/redis/client.py", line 853, in parse_response
    response = connection.read_response()
  File "/home/scfan/env/lib/python2.7/site-packages/redis/connection.py", line 717, in read_response
    raise response
ResponseError: DENIED Redis is running in protected mode because protected mode is enabled, no bind address was specified, no authentication password is requested to clients. In this mode connections are only accepted from the loopback interface. If you want to connect from external computers to Redis you may adopt one of the following solutions: 1) Just disable protected mode sending the command 'CONFIG SET protected-mode no' from the loopback interface by connecting to Redis from the same host the server is running, however MAKE SURE Redis is not publicly accessible from internet if you do so. Use CONFIG REWRITE to make this change permanent. 2) Alternatively you can just disable the protected mode by editing the Redis configuration file, and setting the protected mode option to 'no', and then restarting the server. 3) If you started the server manually just for testing, restart it with the '--protected-mode no' option. 4) Setup a bind address or an authentication password. NOTE: You only need to do one of the above things in order for the server to start accepting connections from the outside.
```

**解决方法:** Redis服务处于保护模式, 需要修改配置文件redis.conf。
将NETWORK下的protected-mode yes修改为protected-mode no，然后重启Redis服务.

### The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128

日志信息

```bash
redis启动警告问题：WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
```

解决方法

```bash
# 临时修改
echo 511 > /proc/sys/net/core/somaxconn
# 永久修改
echo "net.core.somaxconn= 1024" >> /etc/sysctl.conf
# 使其生效
sysctl -p
# 重启 Redis 服务
```
