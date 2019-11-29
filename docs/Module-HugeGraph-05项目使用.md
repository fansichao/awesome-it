# HugeGraph-项目开发文档

tags: HugeGraph 图库 2019 年 11 月

## HugeGraph 使用

- [Github-PyHugeGraphClient](https://github.com/tanglion/PyHugeGraph/blob/master/PyHugeGraph/PyHugeGraphClient.py)

TODO Gremlin 语法

## 问题项

### 问题 2-数据查询时,无法对属性进行大小过滤

- [关于条件查询顶点的两个疑问](https://github.com/hugegraph/hugegraph/issues/560)

> iterateVertices 接口目前没有提供小于及大于语义的条件查询，仅提供了等于条件查询。
> Gremlin 更加自由，完全支持小于条件查询，但是 Gremlin 语法目前没有支持分页的机制，所以如你所说也没办法分页。如果结果集大于百万以上，建议每次查询再加上大于条件，相当于分为一个一个时间区间进行查询。

### 问题 1-数据导入时,发现部分边缺失(起始顶点和结束顶点重复时)

问题场景: 使用 HugeGraph-loader 导入数据时，发现原文件 edge 26663，实际入库的只有 26661

对比 数据文件 edge - HugeGraph 数据

```bash
              cust_certno data_mark         peer_certno     tran_amt tran_cnt tran_date
6615   310116199507048741      mark  331102197108166692  468577630.0        4  20170213
16277  431227199801126424      mark  445300194807241683   40649080.0        4  20170206
```

查询数据文件

```bash
(env) [scfan@fdm hugegraph_data]$ grep -rn "310116199507048741" edge_mark_CUSTACCTTRANJRNL.csv  | grep 331102197108166692
6617:468577630.0,20170213,310116199507048741,4,331102197108166692,mark,310116199507048741,331102197108166692
6618:167389.0,20170224,310116199507048741,4,331102197108166692,mark,310116199507048741,331102197108166692
```

问题原因:

发现由于 起始顶点-结束顶点 相同时，HugeGraph 未录入第二条数据.

根据 起始顶点和结束顶点 对原数据文件去重，仅发现两条相同的 起始顶点-结束顶点 数据，都未导入。

解决方案:

- [如何创建两个顶点间的多边](https://github.com/hugegraph/hugegraph/issues/763)
- [Hugegraph 中 edgelabel 的 sortKey 方法调用](https://github.com/hugegraph/hugegraph/issues/97)

**代码样例:**

```python
 548         # https://github.com/hugegraph/hugegraph/issues/97 指定 sortkeys,用于在两个节点中增加多条边
 549         # sortKeys中字段必须在属性中,重复字段报错! 必须建库第一次使用,后续创建无效!!  exp: .multiTimes().sortKeys("tran_date","tran_cnt")
 550         sortKeys = list(set([i for i in sortKeys if i in cols and i not in primary_cols]))
 551         sortKeys_val = str(sortKeys).replace(')', '').replace('(', '').replace(']', '').replace('[', '')
 552         if bool(sortKeys):
 553             schema_line = 'schema.edgeLabel("%s").sourceLabel("%s").targetLabel("%s").properties(%s).multiTimes().sortKeys(%s).ifNotExist().create();' % (
 554                 edge_label, node_label, node_label, properties, sortKeys_val)
 555         else:
 556             schema_line = 'schema.edgeLabel("%s").sourceLabel("%s").targetLabel("%s").properties(%s).ifNotExist().create();' % (
 557                 edge_label, node_label, node_label, properties)
 558         schema_list.append(schema_line)
```

**界面样例:**
![HugeGraph_顶点之间多边.png](https://raw.githubusercontent.com/fansichao/awesome-it/master/images/20191128092739.png)

## 其他

### 待完成

- [restful 和 gremlin 接口的使用场景，底层区别简介](https://github.com/hugegraph/hugegraph/issues/412)

## 功能

### 字符串属性的模糊查询

[字符串属性的模糊查询](https://github.com/hugegraph/hugegraph/issues/258)

```python
g.V().hasLabel("person").has("lived", Text.contains("海淀区"))
# Text.contains只支持分词后的全词匹配.
# 用 child来搜索"My children"可能会搜索不到.目前hugegraph还无法支持这种搜索，建议上层使用ES等索引库来实现这种模糊查询
```

### 最短路径

[使用 HugeGraph 怎么求解最短路径](https://github.com/hugegraph/hugegraph/issues/29)

Restful-Api-shortestpath

```python
其URL地址形如：http://localhost:8080/graphs/hugegraph/traversers/shortestpath
```

Gremlin-最短路径

```python
# 最短路径
g.V("src_v_id")
 .repeat(out().simplePath()).until(hasId("target_v_id")
 .or().loops().is(gte(4))).hasId("target_v_id")
 .path().limit(1)
# limit(-1) 多条路径不限制
```

### K neighbor API，根据起始顶点，查找 N 步以内可达的所有邻居

[使用 gremlin 执行 k nearest neighbor](https://github.com/hugegraph/hugegraph/issues/716)

```python
g.V("1:3301167").repeat(__.out("MyEdge")).times(2).dedup().count().next()
```

g.V(1).repeat(out().simplePath()).until(hasId(5)).path().limit(1)


## Gremlin语法

https://blog.csdn.net/weixin_42076409/article/details/80856911

http://tang.love/2018/11/15/gremlin_traversal_language/



[Gremlin基础语法-条件和过滤](https://blog.csdn.net/linlin1989117/article/details/82692587)
[Gremlin -- 常用查询用法](https://blog.csdn.net/CSDN___LYY/article/details/84771820)

[深入学习Gremlin（2）：边的遍历操作](https://blog.csdn.net/linlin1989117/article/details/82658777)
[gremlin语句详解](https://blog.csdn.net/weixin_42076409/article/details/80856911)

[GremLin官方文档](http://tinkerpop.apache.org/docs/3.2.5/reference/#drop-step)

[深入学习Gremlin（3）：has条件过滤](https://blog.csdn.net/linlin1989117/article/details/82589895)
[深入学习Gremlin（9）：条件和过滤](https://blog.csdn.net/linlin1989117/article/details/82692587)

[深入学习Gremlin（10）：逻辑运算](https://blog.csdn.net/u010260089/article/details/82769959)

[深入学习Gremlin（5）：查询路径path](https://blog.csdn.net/linlin1989117/article/details/82625906?utm_source=blogxgwz2)
[深入学习Gremlin（13）：路径选取与过滤](https://blog.csdn.net/javeme/article/details/88417208)
[Gremlin 常用语法总结](http://tang.love/2018/11/15/gremlin_traversal_language/)