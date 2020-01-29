# Module-Vaex 使用手册

tags: Pandas vaex Python3 2019 年 12 月

## 介绍说明

[Vaex](https://docs.vaex.io/en/latest/index.html) 是用于惰性核心数据框架（类似于 Pandas）的 python 库，用于可视化和探索大型表格数据集。它可以在 N 维网格上计算统计数据，例如均值，总和，计数，标准差等，最大可达十亿（109）每秒的对象/行数。可视化使用直方图，密度图和 3d 体积渲染完成，从而可以交互式探索大数据。Vaex 使用内存映射，零内存复制策略和惰性计算来获得最佳性能（不浪费内存）

### 特性

### 架构

### 优点

- 性能：适用于海量表格数据，流程>10^9 行/秒
- 惰性/虚拟列：动态计算，不浪费内存
- 高效的内存在执行过滤/选择/子集时没有内存副本。
- 可视化：直接支持，单线通常就足够了。
- 用户友好的 API：您只需要处理 DataFrame 对象，制表符补全和 docstring 可以帮助您：`ds.mean<tab>`，感觉与 Pandas 非常相似。
- 精益：分成多个包
  - vaex-core：DataFrame 和核心算法，将 numpy 数组作为输入列。
  - vaex-hdf5：将内存映射的 numpy 数组提供给 DataFrame。
  - vaex-arrow：箭头支持跨语言数据共享。
  - vaex-viz：基于 matplotlib 的可视化。
  - vaex-jupyter：基于 Jupyter 小部件/ ipywidgets，bqplot，ipyvolume 和 ipyleaflet 的交互式可视化。
  - vaex-astro：与天文学有关的转换和 FITS 文件支持。
  - vaex-server：提供服务器以远程访问 DataFrame。
  - vaex-distributed：（概念证明）将多个服务器/群集组合到单个 DataFrame 中，以进行分布式计算。
  - vaex-qt：使用 Qt GUI 编写的程序。
  - vaex：安装上述所有程序的 Meta 软件包。
  - vaex-ml：机器学习
  - Jupyter 集成：vaex-jupyter 将为您提供在 Jupyter 笔记本和 Jupyter 实验室中的交互式可视化和选择。

## 如何使用

## 附件

### 涉及技术

- [HDF5](https://blog.csdn.net/mzpmzk/article/details/89188968)是一种存储相同类型数值的大数组的机制，适用于可被层次性组织且数据集需要被元数据标记的数据模型.

### 参考资源

- [知乎-如何使用 Python 分析笔记本电脑上的 100 GB 数据~](https://www.zhihu.com/search?type=content&q=vaex)
  - 零内存策略/内存映射策略,少许内存即可轻松快速处理大量数据.
- [Vaex：一种具有超级字符串功能的 DataFrame Python 库](https://baijiahao.baidu.com/s?id=1631752978489322985&wfr=spider&for=pc)

## 项目测试

https://fisams.coding.net/p/FISAMS/assignments/issues/681?filter=e4bfeefd1d7d88d9becee3bd13f03c7e

2019-12-13 Vaex 测试说明

1. 使用 自主建模-字段加工 测试 vaex, 并未发现调用并行计算，仍使用单核计算
2. 1000000 数据测试
   1. vaex 1m58.867s
   2. pandas 9.27s
   3. dask 4.23s
3. vaex 不支持 dataframe.replace . 仅支持 单列的 replace DataFrame.col.str.replace

暂未发现 Vaex 的多核计算功能.
