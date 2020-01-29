# Dask 并行任务调度

## Dask 说明介绍

[Dask](https://docs.dask.org/en/latest/)是用于 Python 中并行计算的灵活库。

达斯由两部分组成：

- 动态任务调度针对计算进行了优化。这类似于 Airflow，Luigi，Celery 或 Make，但已针对交互式计算工作负载进行了优化。
- “大数据”集合（如并行数组，数据帧和列表）将诸如 NumPy，Pandas 或 Python 迭代器之类的通用接口扩展到内存或分布式环境。这些并行集合在动态任务计划程序之上运行。

达斯克强调以下优点：

- 熟悉：提供并行的 NumPy 数组和 Pandas DataFrame 对象
- 灵活：提供任务计划界面，以实现更多自定义工作负载并与其他项目集成。
- Native：在纯 Python 中启用分布式计算并可以访问 PyData 堆栈。
- 快速：以低开销，低延迟和快速数值算法所需的最少序列化操作
- 扩大规模：在具有 1000 个核心的集群上弹性运行
- 缩小：在单个过程中轻松设置并在笔记本电脑上运行
- 响应式：在设计时考虑了交互式计算，它提供了快速的反馈和诊断功能，以帮助人类

![20191205_Dask_架构图.png](https://raw.githubusercontent.com/fansichao/images/master/markdown/20191205_Dask_架构图.png)

### Dask 分析

(env36) [scfan@fdm tools]$  dask-scheduler
(env36) [scfan@fdm ~]$ dask-worker 10.0.2.14:8786

python3

Dask-资源分析
Dask-任务管理

### Dask 优缺点

优点

- 支持单机、分布式环境
- 类 Pandas 风格,修改成本低

缺点

- Dask-DataFrame
  - 读取文件不支持 excel。支持 read_csv read_table read_fwf read_parquet read_hdf read_json read_orc

## Dask 部署

## 附件

### 性能测试

使用 自主建模-字段加工节点 测试 Pandas & Dask 性能

### 参考资源

- [Jupyter-Data Science with Python and Dask](https://github.com/jcdaniel91/data-science-python-dask)

### Dask & Pandas 语法差异表

[Github-Dask Collections API compatibility](https://github.com/dask/dask/issues/3688)

样例

```python
# Dask 没有 pandas.core.series.Series
if data_mode.upper() == 'DASK':
    pass
else:
    if varname.startswith('df') and not isinstance(argls[index], pandas.core.series.Series):
        raise RuntimeError('第%s个参数必须为一列' % (index + 1))

# Dask DataFrame.replace 没有 inplace 参数
if data_mode == 'DASK':
    data = data.replace(to_replace='nan',value='')
else:
    data.replace(to_replace='nan',value='',inplace=True)

# Dask DataFrame.to_csv
# data.to_csv('a1.csv') 会创建目录
# data.to_csv(['a1.csv']) 会创建文件
# data.to_csv('a-*.csv') 会创建分区文件,创建多个文件
if data_mode == 'DASK':
    data.to_csv(['a1.csv'],index=False)
else:
    data.to_csv('a.csv',index=False)
```

### Dask & Pandas 细节语法性能差异

- [[译] 在 Python 中，如何运用 Dask 数据进行并行数据分析](https://blog.csdn.net/weixin_33682790/article/details/87957809)
- [Python 大规模数据存储与读取、并行计算：Dask 库简述](https://msd.misuland.com/pd/2884249965817764970?page=1)

### 开启程序

#### Dask-scheduler

开启 dask-scheduler

```bash
(env36) [scfan@fdm tools]$ dask-scheduler
distributed.scheduler - INFO - -----------------------------------------------
distributed.dashboard.proxy - INFO - To route to workers diagnostics web server please install jupyter-server-proxy: pip install jupyter-server-proxy
distributed.scheduler - INFO - Local Directory:    /tmp/scheduler-bdk4b7li
distributed.scheduler - INFO - -----------------------------------------------
distributed.scheduler - INFO - Clear task state
distributed.scheduler - INFO -   Scheduler at:      tcp://10.0.2.14:8786
distributed.scheduler - INFO -   dashboard at:                     :8787
distributed.scheduler - INFO - Register tcp://10.0.2.14:30547
distributed.scheduler - INFO - Starting worker compute stream, tcp://10.0.2.14:30547
distributed.core - INFO - Starting established connection
distributed.scheduler - INFO - Register tcp://10.0.2.14:9190
distributed.scheduler - INFO - Starting worker compute stream, tcp://10.0.2.14:9190
distributed.core - INFO - Starting established connection
```

Dask-Scheduler 可视化界面
![20191205_Dask_Scheduler_可视化界面.png](https://raw.githubusercontent.com/fansichao/images/master/markdown/20191205_Dask_Scheduler_可视化界面.png)

#### Dask-Worker

开启 Worker

```bash
(env36) [scfan@fdm tools]$ dask-worker 10.0.2.14:8786
distributed.nanny - INFO -         Start Nanny at: 'tcp://10.0.2.14:12075'
distributed.diskutils - INFO - Found stale lock file and directory '/home/scfan/project/FISAMS/branches/branch_scfan/src/server/fdm/tools/worker-yyz2l21f', purging
distributed.dashboard.proxy - INFO - To route to workers diagnostics web server please install jupyter-server-proxy: pip install jupyter-server-proxy
distributed.worker - INFO -       Start worker at:      tcp://10.0.2.14:17181
distributed.worker - INFO -          Listening to:      tcp://10.0.2.14:17181
distributed.worker - INFO -          dashboard at:            10.0.2.14:36300
distributed.worker - INFO - Waiting to connect to:       tcp://10.0.2.14:8786
distributed.worker - INFO - -------------------------------------------------
distributed.worker - INFO -               Threads:                          4
distributed.worker - INFO -                Memory:                   10.32 GB
distributed.worker - INFO -       Local Directory: /home/scfan/project/FISAMS/branches/branch_scfan/src/server/fdm/tools/worker-5304u4tp
distributed.worker - INFO - -------------------------------------------------
distributed.worker - INFO -         Registered to:       tcp://10.0.2.14:8786
distributed.worker - INFO - -------------------------------------------------
distributed.core - INFO - Starting established connection
```

Dask-Worker 可视化界面
![20191205_Dask_Worker_可视化界面.png](https://raw.githubusercontent.com/fansichao/images/master/markdown/20191205_Dask_Worker_可视化界面.png)

# Dask 对比

Dask 缺点

- dataframe
  - 不提供 sql 支持,可以使用 dask.dataframe.from_sql
  - 支持的数据格式
    - Tabular: Parquet, ORC, CSV, Line Delimited JSON, Avro, text
    - Arrays: HDF5, NetCDF, Zarr, GRIB
    - 不支持 Excel

Dask 优点

- Dask 可以抵抗工作节点的故障
- Dask 虽然较新 2015 年,但是已经成熟,而且随 Pandas 更新而更新
- Dask 是通用并行编程解决方案。类似 Pandsa,使用方便,和 pandas 有细微差异
- 支持本地 Dask 的概要分析和检查执行情况
  - https://docs.dask.org/en/latest/diagnostics-local.html#example

Dask 支持项

- 支持 单机调度程序、分布式调度程序(本地或集群)
- dask-worker 资源控制
  --resources <resources>
  用于任务约束的资源，例如“ GPU = 2 MEM = 10e9”。
  资源分别应用于每个工作进程（仅在使用“ –nprocs”启动多个工作进程时才相关）。
- 可视化界面
  - http://192.168.172.72:27831/status Scheduler
  - http://192.168.172.72:8787/status worker
