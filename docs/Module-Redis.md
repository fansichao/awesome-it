# Module-Redis

tags: Redis Centos7 2019 年 12 月

环境说明: CentoS7.5

## Redis 部署

```bash
# Install
yum install lrzsz -y
pip install redis

# wget http://download.redis.io/releases/redis-5.0.5.tar.gz
wget http://download.redis.io/releases/redis-3.2.9.tar.gz
tar -zxf redis-3.2.9.tar.gz
# # 编译并指定安装目录
cd redis-3.2.9
# # 创建软链接
make PREFIX=/usr/local/redis-3.2.9 install
ln -s /usr/local/redis-3.2.9 /usr/local/redis
cp redis.conf /etc/redis.conf
cp /usr/local/redis/bin/redis-server /usr/local/bin/redis-server
```

配置 Redis

```bash
# 配置 overcommit_memory 参数
echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf
# 使其生效
sysctl vm.overcommit_memory=1

# 关闭透明大页面-临时
echo never > /sys/kernel/mm/transparent_hugepage/enabled
# 关闭透明大页面-永久,开机生效
echo "echo never > /sys/kernel/mm/transparent_hugepage/enabled" >> /etc/rc.local

# 修改 redis.conf
protected-mode yes 修改为 protected-mode no
```

## Redis 使用

```bash
# 启动 Redis
redis-server /etc/redis.conf
```

**启动页面内容**如下

````bash
[root@e7489d44f6bf redis-3.2.9]# redis-server /etc/redis.conf
                _._
           _.-``__ ''-._
      _.-``    `.  `_.  ''-._           Redis 3.2.9 (00000000/0) 64 bit
  .-`` .-```.  ```\/    _.,_ ''-._
 (    '      ,       .-`  | `,    )     Running in standalone mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
 |    `-._   `._    /     _.-'    |     PID: 4682
  `-._    `-._  `-./  _.-'    _.-'
 |`-._`-._    `-.__.-'    _.-'_.-'|
 |    `-._`-._        _.-'_.-'    |           http://redis.io
  `-._    `-._`-.__.-'_.-'    _.-'
 |`-._`-._    `-.__.-'    _.-'_.-'|
 |    `-._`-._        _.-'_.-'    |
  `-._    `-._`-.__.-'_.-'    _.-'
      `-._    `-.__.-'    _.-'
          `-._        _.-'
              `-.__.-'

4682:M 25 Dec 04:20:48.273 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
4682:M 25 Dec 04:20:48.274 # Server started, Redis version 3.2.9
4682:M 25 Dec 04:20:48.274 * The server is now ready to accept connections on port 6379
````
