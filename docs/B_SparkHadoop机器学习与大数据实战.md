# B_SparkHadoop 机器学习与大数据实战

/\*

- @Author: Scfan
- @Date: 2018-12-10 09:55:05
- @LastEditors: Scfan
- @LastEditTime: 2018-12-12 15:29:20
- @Description: 工作&amp;学习&amp;生活
- @Email: 643566992@qq.com
- @Company: 上海
- @version: V1.0
  \*/

**本文件名称**
@import 'B_SparkHadoop 机器学习与大数据实战.md'

**书籍名称**
@import 'File/00IT 资料/00 书籍/20181120*精通 Python 网络爬虫核心技术与框架与项目实战*韦玮\_完整高清目录扫描版.pdf'

## Hadoop HDFS 命令

1. HDFS 启动命令：start-all.sh
2. HDFS 页面：[http://192.168.172.70:50070](http://192.168.172.70:50070)

### 常用命令

命令格式 `hadoop fs -命令`

| 命令                     | 说明                                        |
| ------------------------ | ------------------------------------------- |
| hadoop fs -mkdir         | 创建 HDFS 目录                              |
| hadoop fs -ls            | 列出 HDFS 目录                              |
| hadoop fs -copyFromLocal | 使用-copyFromLocal 复制本地文件到 HDFS 目录 |
| hadoop fs -put           | 使用-put 复制本地文件到 HDFS 目录           |
| hadoop fs -cat           | 列出 HDFS 目录下文件内容                    |
| hadoop fs -copyToLocal   | 使用-copyToLocal 将 HDFS 目录文件复制到本地 |
| hadoop fs -get           | 使用-get 将 HDFS 目录文件复制到本地         |
| hadoop fs -cp            | 复制 HDFS 文件                              |
| hadoop fs -rm            | 删除 HDFS 文件                              |

### 命令使用样例

```bash
# 创建目录
hadoop fs -mkdir -p /user/hduser/test
# 查看HDFS目录
hadoop fs -ls /user/hduser/test
# 查看所有子目录
hadoop fs -ls -R /
# 复制本地文件到HDFS
hadoop fs -copyFromLocal /user/local/hadoop/README.txt /user/hduser/test
# 复制本地文件到HDFS 强制，文件已经存在，会直接覆盖
hadoop fs -copyFromLocal -f /user/local/hadoop/README.txt /user/hduser/test
# 复制本地文件到HDFS 多个同时复制
hadoop fs -copyFromLocal -f /user/local/hadoop/README.txt a.txt /user/hduser/test
```

1. -put: 复制文件，如果文件存在，直接覆盖，无提示。 put 可以接受`stdin`标准输入
2. -copyFromLocal: 复制文件，如果文件存在，会提示。

```bash
# 使用put接受stdin标准输入
echo abc | hadoop fs -put - /user/hduser/test/test.txt
# 将本地目录列表存储到HDFS文件中
ls /usr/local/hadoop | hadoop fs -put - /user/hduser/test/hadooplist.txt
# 将HDFS文件复制到本地
hadoop fs -get /user/hduser/test/hadooplist.txt hadooplist.txt
```

## Hadoop MapReduce

MapRedu 一种程序开发模式，使用大量服务器并行处理。
Map 分配工作，Reduce 将结果汇总整理。

TODO java 测试样例 pass

## Spark RDD

Spark 的核心是 RDD(Resilient Distributed Dataset),即弹性分布式数据集，是由
AMPLab 实验室提出的概念，属于一种分布式内存系统数据集应用。
Spark 主要优势来源于 RDD 本身的特性，
RDD 可以兼容其他系统，可以导入其他外部存储数据。

### RDD 特性

#### RDD 运算类型

> RDD 的三种基本运算

1. **转换运算**:
   1. RDD 执行转换，会产生另外一个 RDD
   2. RDD 具有 lazy 特性，**转换**运算不会立刻执行，而是等到执行**动作**运算时执行
2. **动作运算**
   1. 指定**动作运算**后，会产生数据或写入文件系统。
   2. 执行**动作运算**后，会立即执行之前的转换运算和当前的动作运算
3. **持久化运算**
   1. 内存中使用，提高执行性能

> Lineage 机制具有容错功能

RDD 本身具有`Lineage`机制。会记录每个 RDD 与其父代 RDD 之间的关联，还会记录通过什么操作才能有父代 RDD 得到该 RDD 的信息。

### RDD 转换运算

```python
# 创建 intRDD
intRDD = sc.parallelize(List(3,1,2,5,5))
intRDD.collent()
# 创建stringRDD
stringRDD = sc.parallelize(List("a","b","a"))
# map运算介绍 可以传入函数 具名函数和匿名函数
def addone(x):
    return x+1
# 具名函数
intRDD.map(addone).collect()
# 匿名函数
intRDD.map(lambda x:x+1).collect()
```

> filter 数字运算
> filter 用于对 RDD 内每个元素进行筛选，并产生另外的 RDD。

```python
# intRDD 筛选数字1-5之间
intRDD.filter(lambda x:1<x and x<5).collect()
# strRDD 筛选指定字符串
stringRDD.filter(lambda x:"ra" in x).collect()
# distinct 删除重复元素
intRDD.distinct().collect()
stringRDD.distinct().collect()
```

> randomSplit 运算
> randomSplit 可以将整个集合元素以随机数的方式按比例分为多个 RDD。

```python
sRDD = intRDD.randomSplit([0.4,0.6])
print sRDD[0].collect()
print sRDD[1].collect()
```

> groupby 运算
> groupBy 可以按照匿名函数规则分为多个 List

```python
# 使用 groupBy 分为奇数和偶数
gRDD = intRDD.groupBy(lambda x:"even" if (x%2==0) else "odd").collect()

```

### 多个 RDD 转换运算

```python
# 使用 union 函数进行 并集运算
intRDD1.union(intRDD2).union(intRDD3).collect()
# 使用 intersection 进行 交集运算
intRDD1.intersection(intRDD2).collect()
# subtract 差集运算
intRDD1.subtract(intRDD2).collect()
# cartesian 笛卡尔乘积运算
print intRDD1.cartesian(intRDD2).collect()
```

### 基本 动作运算

动作运算 会立即执行。

> 读取元素

```python
# 取出 第一项数据
intRDD.fisrt()
# 去除 第二项数据
intRDD.take(2)
# 从小到大排序 取出前三项
intRDD.takeOrdered(3)
# 从大到小排序 取出前三项
intRDD.takeOrdered(3,key=lambda x:-x)
```

> 统计功能

```python
# 统计
intRDD.stats()
# 最小
intRDD.min()
# 最大
intRDD.max()
# 标准差
intRDD.stdev()
# 计数
intRDD.count()
# 总和
intRDD.sum()
# 平均
intRDD.mean()
```

### RDD K-V 转换

```python
# 创建 K-V RDD
kvRDD1 = sc.parallelize([(1,2),(2,3),(3,4)])
kvRDD1.collect()
# 列出 keys
kvRDD1.keys().collect()
# 列出 Values
kvRDD1.values().collect()
# 使用 filter 过滤 Key 元素
kvRDD1。filter(lambda kv:kv[0]<5).collect()
# 使用 filter 过滤 Values
kvRDD1。filter(lambda kv:kv[1]<5).collect()
# mapValues运算 针对每组进行运算，产生另外一个RDD
kvRDD1.mapValues(lambda x:x*x).collect()
# sortByKey() 按照key排序
kvRDD1.sortByKey(ascending=True).collect() # 默认 从小到大排序
# reduceByKey 根据key累加Value
kvRDD1.reduceByKey(lambda x,y:x+y).collect()
```

### 多个 RDD K-V 转换

```python
# join
kvRDD1.join(kvRDD2).collect()
# leftOuterJoin
kvRDD1.leftOuterJoin(kvRDD2).collect()
# rightOuterJoin
kvRDD1.rightOuterJoin(kvRDD2).collect()
# subtractByKey 运算
# 删除相同key的数据
kvRDD1.subtractByKey(kvRDD2).collect()
```

### RDD K-V 动作运算

```python
# 获取第一项数据
kvRDD1.first()
# 获取前两项数据
kvRDD1.take(2)
# 计算每个Key中值的项数
kvRDD1.countByKey()
# collectAsMap() 创建kv字典
kvRDD1.collectAsMap()
# lookup 根据Key 查找 Value
kvRDD1.lookup(3)
```

### Broadcast 广播变量

共享变量用于节省内存与运行时间，提高并行处理时的执行效率。

共享变量:
Broadcast 广播变量，
accumulator 累加器

```python
kv = sc.parallelize((1,"a"),(2,"b"))
kvMap = kv.collectAsMap()
# 转换为 广播变量
bc_kvMap = sc.broadcast(kvMap)
# ids 值
ids = sc.parallelize([1,2])
# 使用 Broadcast 进行转换
bc_kvMap_names =ids.map(lambda x:bc_kvMap.value[x]).collect()

# accumulator 累加器共享变量
# 创建 total 累加器
total = sc.accumulator(0.0)
# 创建 num 累加器
num = sc.accumulator(0)
# foreach
intRDD.foreach(lambda a:[total.add(a), num.add(1)])
# 计算平均、总和 数量
avg = total.value / num.value

```

### RDD 持久化

1. **RDD.persist** 存储等级，可以指定存储等级，默认是 MEMORY_ONLY
2. **RDD.unpersist** 取消持久化

持久化存储等级如下:

1. MEMORY_ONLY : 存储内存中，多余 RDD 重新计算
2. MEMORY_ADN_DISK: 存储内存中，多余 RDD 存储在硬盘中，在从硬盘读取。
3. MEMORY_ONLY_SER: 存储内存找那个，多使用 CPU 资源，内存消耗较少，多余 RDD 重新计算.
4. MEMORY_AND_DISK_SER: 存储内存找那个，多使用 CPU 资源，内存消耗较少，多余 RDD 存储硬盘中.
5. DIST_ONLY: 存储硬盘中
6. MEMORY_ONLY_2,MEMORY_ADN_DISK_2: 每个 RDD 节点都复制到两个节点上。

持久化样例

```python
# 创建 intRddMemory
intRddMemory = sc.parallelize([3,1,2,5])
# 持久化
intRddMemory.persist
# 查看是否已经缓存
intRddMemory.is_cached
# 取消持久化
intRddMemory.unpersist
# 查看是否取消缓存
intRddMemory.is_cached
# 设置存储等级
intRddMemoryAndDisk = sc.parallelize([3,1,2])
intRddMemoryAndDisk.persist(StorageLevel.MEMORY_ADN_DISK)
intRddMemoryAndDisk.is_cached
```
