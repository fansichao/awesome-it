# Gremlin

## Gremlin 语法

### 功能模块

#### 最短路径

```python
g.V("1:130133198506126945")
.repeat(bothE().otherV().simplePath()).until(hasId("1:530924194403163587")
.or().loops().is(gte(4))).hasId("1:530924194403163587")
.path().limit(1)
```

.has('tran_amt',gte(1))

- 想要同时获得经过的边的信息，可以用 bothE().otherV()替换 both()

最短路径

```python
g.V("1:4822")
.repeat(bothE().otherV().simplePath()).until(hasId("1:9947")
.or().loops().is(gte(4))).hasId("1:9947")
.path().limit(-1)
```

hugegraph.traversal()

#### 邻居节点

```python
g.V("1:130133198506126945")
.repeat(bothE().has('tran_amt',gte(10000000)).has('tran_amt',lte(10000000000)).has('tran_date',gte(20170210)).has('tran_date',lte(20170230))
.otherV().simplePath())
.until(loops().is(gte(2))) .path().limit(200)
```

has("tran_date",gte(%s))
