# HugeGraph使用文档.md

tags: HugeGraph 图库 2019年

**文档说明**:

- Api使用
  - HTTPAPI
  - GremliAPI
- 数据导入样例
- 使用代码样例
- 问题

TODO Api的任务撤销功能

TODO Gremlin使用

## Api-HTTP使用

注: API详细使用详见官网[HugeGraph Restful API](https://hugegraph.github.io/hugegraph-doc/clients/hugegraph-api.html),此处仅展现部分项目将使用. 

ApiHTTP

- 顶点
- 边
- 遍历
- 任务




### 2.1 Vertex

#### 2.1.5 获取符合条件的顶点

##### Params

- label: 顶点类型
- properties: 属性键值对(根据属性查询的前提是建立了索引)
- limit: 查询最大数目
- page: 页号

以上参数都是可选的，如果提供page参数，必须提供limit参数，不允许带其他参数。`label, properties`和`limit`可以任意组合。

**查询所有 age 为 20 且 label 为 person 的顶点**

##### Method & Url

```
GET http://localhost:8080/graphs/hugegraph/graph/vertices?label=person&properties={"age":29}&limit=1
```

##### Response Status

```json
200
```

##### Response Body

```json
{
    "vertices": [
        {
            "id": "1:marko",
            "label": "person",
            "type": "vertex",
            "properties": {
                "city": [
                    {
                        "id": "1:marko>city",
                        "value": "Beijing"
                    }
                ],
                "name": [
                    {
                        "id": "1:marko>name",
                        "value": "marko"
                    }
                ],
                "age": [
                    {
                        "id": "1:marko>age",
                        "value": 29
                    }
                ]
            }
        }
    ]
}
```

**分页查询所有顶点，获取第一页（page不带参数值），限定3条**

##### Method & Url

```
GET http://localhost:8080/graphs/hugegraph/graph/vertices?page&limit=3
```

##### Response Status

```json
200
```

##### Response Body

```json
{
	"vertices": [{
			"id": "2:ripple",
			"label": "software",
			"type": "vertex",
			"properties": {
				"price": [{
					"id": "2:ripple>price",
					"value": 199
				}],
				"name": [{
					"id": "2:ripple>name",
					"value": "ripple"
				}],
				"lang": [{
					"id": "2:ripple>lang",
					"value": "java"
				}]
			}
		},
		{
			"id": "1:vadas",
			"label": "person",
			"type": "vertex",
			"properties": {
				"city": [{
					"id": "1:vadas>city",
					"value": "Hongkong"
				}],
				"name": [{
					"id": "1:vadas>name",
					"value": "vadas"
				}],
				"age": [{
					"id": "1:vadas>age",
					"value": 27
				}]
			}
		},
		{
			"id": "1:peter",
			"label": "person",
			"type": "vertex",
			"properties": {
				"city": [{
					"id": "1:peter>city",
					"value": "Shanghai"
				}],
				"name": [{
					"id": "1:peter>name",
					"value": "peter"
				}],
				"age": [{
					"id": "1:peter>age",
					"value": 35
				}]
			}
		}
	],
	"page": "001000100853313a706574657200f07ffffffc00e797c6349be736fffc8699e8a502efe10004"
}
```

返回的body里面是带有下一页的页号信息的，`"page": "001000100853313a706574657200f07ffffffc00e797c6349be736fffc8699e8a502efe10004"`，
在查询下一页的时候将该值赋给page参数。

**分页查询所有顶点，获取下一页（page带上上一页返回的page值），限定3条**

##### Method & Url

```
GET http://localhost:8080/graphs/hugegraph/graph/vertices?page=001000100853313a706574657200f07ffffffc00e797c6349be736fffc8699e8a502efe10004&limit=3
```

##### Response Status

```json
200
```

##### Response Body

```json
{
	"vertices": [{
			"id": "1:josh",
			"label": "person",
			"type": "vertex",
			"properties": {
				"city": [{
					"id": "1:josh>city",
					"value": "Beijing"
				}],
				"name": [{
					"id": "1:josh>name",
					"value": "josh"
				}],
				"age": [{
					"id": "1:josh>age",
					"value": 32
				}]
			}
		},
		{
			"id": "1:marko",
			"label": "person",
			"type": "vertex",
			"properties": {
				"city": [{
					"id": "1:marko>city",
					"value": "Beijing"
				}],
				"name": [{
					"id": "1:marko>name",
					"value": "marko"
				}],
				"age": [{
					"id": "1:marko>age",
					"value": 29
				}]
			}
		},
		{
			"id": "2:lop",
			"label": "software",
			"type": "vertex",
			"properties": {
				"price": [{
					"id": "2:lop>price",
					"value": 328
				}],
				"name": [{
					"id": "2:lop>name",
					"value": "lop"
				}],
				"lang": [{
					"id": "2:lop>lang",
					"value": "java"
				}]
			}
		}
	],
	"page": null
}
```

此时`"page": null`表示已经没有下一页了。

### 2.2 Edge

#### 2.2.5 获取符合条件的边

##### Params

- vertex_id: 顶点id
- direction: 边的方向(OUT | IN | BOTH)
- label: 边的标签
- properties: 属性键值对(根据属性查询的前提是建立了索引)
- offset：偏移，默认为0
- limit: 查询数目，默认为100
- page: 页号

支持的查询有以下几种：

- 提供vertex_id参数时，不可以使用参数page，direction、label、properties可选，offset和limit可以
限制结果范围
- 不提供vertex_id参数时，label和properties可选
    - 如果使用page参数，则：offset参数不可用（不填或者为0），direction不可用，properties最多只能有一个
    - 如果不使用page参数，则：offset和limit可以用来限制结果范围，direction参数忽略

**查询与顶点 person:josh(vertex_id="1:josh") 相连且 label 为 created 的边**

##### Method & Url

```
GET http://127.0.0.1:8080/graphs/hugegraph/graph/edges?vertex_id="1:josh"&direction=BOTH&label=created&properties={}
```

##### Response Status

```json
200
```

##### Response Body

```json
{
    "edges": [
        {
            "id": "S1:josh>1>>S2:lop",
            "label": "created",
            "type": "edge",
            "inVLabel": "software",
            "outVLabel": "person",
            "inV": "2:lop",
            "outV": "1:josh",
            "properties": {
                "date": "20091111",
                "weight": 0.4
            }
        },
        {
            "id": "S1:josh>1>>S2:ripple",
            "label": "created",
            "type": "edge",
            "inVLabel": "software",
            "outVLabel": "person",
            "inV": "2:ripple",
            "outV": "1:josh",
            "properties": {
                "date": "20171210",
                "weight": 1
            }
        }
    ]
}
```

**分页查询所有边，获取第一页（page不带参数值），限定3条**

##### Method & Url

```
GET http://127.0.0.1:8080/graphs/hugegraph/graph/edges?page&limit=3
```

##### Response Status

```json
200
```

##### Response Body

```json
{
	"edges": [{
			"id": "S1:peter>2>>S2:lop",
			"label": "created",
			"type": "edge",
			"inVLabel": "software",
			"outVLabel": "person",
			"inV": "2:lop",
			"outV": "1:peter",
			"properties": {
				"weight": 0.2,
				"date": "20170324"
			}
		},
		{
			"id": "S1:josh>2>>S2:lop",
			"label": "created",
			"type": "edge",
			"inVLabel": "software",
			"outVLabel": "person",
			"inV": "2:lop",
			"outV": "1:josh",
			"properties": {
				"weight": 0.4,
				"date": "20091111"
			}
		},
		{
			"id": "S1:josh>2>>S2:ripple",
			"label": "created",
			"type": "edge",
			"inVLabel": "software",
			"outVLabel": "person",
			"inV": "2:ripple",
			"outV": "1:josh",
			"properties": {
				"weight": 1,
				"date": "20171210"
			}
		}
	],
	"page": "002500100753313a6a6f73681210010004000000020953323a726970706c65f07ffffffcf07ffffffd8460d63f4b398dd2721ed4fdb7716b420004"
}
```

返回的body里面是带有下一页的页号信息的，`"page": "002500100753313a6a6f73681210010004000000020953323a726970706c65f07ffffffcf07ffffffd8460d63f4b398dd2721ed4fdb7716b420004"`，
在查询下一页的时候将该值赋给page参数。

**分页查询所有边，获取下一页（page带上上一页返回的page值），限定3条**

##### Method & Url

```
GET http://127.0.0.1:8080/graphs/hugegraph/graph/edges?page=002500100753313a6a6f73681210010004000000020953323a726970706c65f07ffffffcf07ffffffd8460d63f4b398dd2721ed4fdb7716b420004&limit=3
```

##### Response Status

```json
200
```

##### Response Body

```json
{
	"edges": [{
			"id": "S1:marko>1>20130220>S1:josh",
			"label": "knows",
			"type": "edge",
			"inVLabel": "person",
			"outVLabel": "person",
			"inV": "1:josh",
			"outV": "1:marko",
			"properties": {
				"weight": 1,
				"date": "20130220"
			}
		},
		{
			"id": "S1:marko>1>20160110>S1:vadas",
			"label": "knows",
			"type": "edge",
			"inVLabel": "person",
			"outVLabel": "person",
			"inV": "1:vadas",
			"outV": "1:marko",
			"properties": {
				"weight": 0.5,
				"date": "20160110"
			}
		},
		{
			"id": "S1:marko>2>>S2:lop",
			"label": "created",
			"type": "edge",
			"inVLabel": "software",
			"outVLabel": "person",
			"inV": "2:lop",
			"outV": "1:marko",
			"properties": {
				"weight": 0.4,
				"date": "20171210"
			}
		}
	],
	"page": null
}
```

此时`"page": null`表示已经没有下一页了。







### 3.1 traverser API概述

HugeGraphServer为HugeGraph图数据库提供了RESTful API接口。除了顶点和边的CRUD基本操作以外，还提供了一些遍历（traverser）方法，我们称为`traverser API`。这些遍历方法实现了一些复杂的图算法，方便用户对图进行分析和挖掘。

HugeGraph支持的traverser API包括：

- K-out API，根据起始顶点，查找恰好N步可达的邻居
- K-neighbor API，根据起始顶点，查找N步以内可达的所有邻居
- Shortest Path API，查找两个顶点之间的最短路径
- Paths API，查找两个顶点间的全部路径
- Customized Paths API，从一批顶点出发，按（一种）模式遍历经过的全部路径
- Crosspoints API，查找两个顶点的交点（共同祖先或者共同子孙）
- Customized Crosspoints API，从一批顶点出发，按多种模式遍历，最后一步到达的顶点的交点
- Rings API，从起始顶点出发，可到达的环路路径
- Rays API，从起始顶点出发，可到达边界的路径（即无环路径）
- Vertices API
	- 按ID批量查询顶点；
	- 获取顶点的分区；
	- 按分区查询顶点；
- Edges API
	- 按ID批量查询边；
	- 获取边的分区；
	- 按分区查询边；



#### 3.2.2 K-neighbor

##### 3.2.2.1 功能介绍

根据起始顶点、方向、边的类型（可选）和深度depth，查找包括起始顶点在内、depth步之内可达的所有顶点

> 相当于：起始顶点、K-out(1)、K-out(2)、... 、K-out(max_depth)的并集

###### Params

- source: 起始顶点id，必填项
- direction: 起始顶点向外发散的方向（OUT,IN,BOTH），选填项，默认是BOTH
- max_depth: 步数，必填项
- label: 边的类型，选填项，默认代表所有edge label
- max_degree: 查询过程中，单个顶点最大边数目，选填项，默认为10000
- limit: 返回的顶点的最大数目，也即遍历过程中最大的访问的顶点数目，选填项，默认为10000000

##### 3.2.2.2 使用方法

###### Method & Url

```
GET http://localhost:8080/graphs/{graph}/traversers/kneighbor?source=“1:marko”&max_depth=2
```

###### Response Status

```json
200
```

###### Response Body

```json
{
    "vertices":[
        "2:ripple",
        "1:marko",
        "1:josh",
        "1:vadas",
        "1:peter",
        "2:lop"
    ]
}
```

##### 3.2.2.3 适用场景

查找N步以内可达的所有顶点，例如：

- 家族关系中，查找一个人五服以内所有子孙，person A通过连续的5条“亲子”边到达的顶点集合。
- 社交关系中发现好友圈子，例如目标用户通过1条、2条、3条“朋友”边可到达的用户可以组成目标用户的朋友圈子

#### 3.2.3 Shortest Path

##### 3.2.3.1 功能介绍

根据起始顶点、目的顶点、方向、边的类型（可选）和最大深度，查找一条最短路径

###### Params

- source: 起始顶点id，必填项
- target: 目的顶点id，必填项
- direction: 起始顶点向外发散的方向（OUT,IN,BOTH），选填项，默认是BOTH
- max_depth: 最大步数，必填项
- label: 边的类型，选填项，默认代表所有edge label
- max_degree: 查询过程中，单个顶点最大边数目，选填项，默认为10000
- skip_degree: 查询过程中需要跳过的顶点的最小的边数目，即当顶点的边数目大于 skip_degree 时，跳过该顶点，可用于规避超级点，选填项，默认为0，表示不跳过任何点
- capacity: 遍历过程中最大的访问的顶点数目，选填项，默认为10000000

##### 3.2.3.2 使用方法

###### Method & Url

```
GET http://localhost:8080/graphs/{graph}/traversers/shortestpath?source="1:marko"&target="2:ripple"&max_depth=3
```

###### Response Status

```json
200
```

###### Response Body

```json
{
    "path":[
        "1:marko",
        "1:josh",
        "2:ripple"
    ]
}
```

##### 3.2.3.3 适用场景

查找两个顶点间的最短路径，例如：

- 社交关系网中，查找两个用户有关系的最短路径，即最近的朋友关系链
- 设备关联网络中，查找两个设备最短的关联关系

#### 3.2.4 Paths

##### 3.2.4.1 功能介绍

根据起始顶点、目的顶点、方向、边的类型（可选）和最大深度等条件查找所有路径

###### Params

- source: 起始顶点id，必填项
- target: 目的顶点id，必填项
- direction: 起始顶点向外发散的方向（OUT,IN,BOTH），选填项，默认是BOTH
- label: 边的类型，选填项，默认代表所有edge label
- max_depth: 步数，必填项
- max_degree: 查询过程中，单个顶点最大边数目，选填项，默认为10000
- capacity: 遍历过程中最大的访问的顶点数目，选填项，默认为10000000
- limit: 返回的路径的最大数目，选填项，默认为10

##### 3.2.4.2 使用方法

###### Method & Url

```
GET http://localhost:8080/graphs/{graph}/traversers/paths?source="1:marko"&target="1:josh"&max_depth=5
```

###### Response Status

```json
200
```

###### Response Body

```json
{
    "paths":[
        {
            "objects":[
                "1:marko",
                "1:josh"
            ]
        },
        {
            "objects":[
                "1:marko",
                "2:lop",
                "1:josh"
            ]
        }
    ]
}
```

##### 3.2.4.3 适用场景

查找两个顶点间的所有路径，例如：

- 社交网络中，查找两个用户所有可能的关系路径
- 设备关联网络中，查找两个设备之间所有的关联路径



#### 3.2.8 Customized Paths

##### 3.2.8.1 功能介绍

根据一批起始顶点、边规则（包括方向、边的类型和属性过滤）和最大深度等条件查找符合条件的所有的路径

###### Params

- sources: 定义起始顶点，必填项，指定方式包括：
	- ids：通过顶点id列表提供起始顶点
	- labels和properties：如果没有指定ids，则使用label和properties的联合条件查询起始顶点
		- labels：顶点的类型列表
		- properties：通过属性的值查询起始顶点
		> 注意：properties中的属性值可以是列表，表示只要key对应的value在列表中就可以

- steps: 表示从起始顶点走过的路径规则，是一组Step的列表。必填项。每个Step的结构如下：
	- direction：表示边的方向（OUT,IN,BOTH），默认是BOTH
	- labels：边的类型列表
	- properties：通过属性的值过滤边
	- weight_by：根据指定的属性计算边的权重，sort_by不为NONE时有效，与default_weight互斥
	- default_weight：当边没有属性作为权重计算值时，采取的默认权重，sort_by不为NONE时有效，与weight_by互斥
	- degree：查询过程中，单个顶点最大边数目，默认为10000
	- sample：当需要对某个step的符合条件的边进行采样时设置，-1表示不采样，默认为采样100
- sort_by: 根据路径的权重排序，选填项，默认为 NONE：
	- NONE表示不排序，默认值
	- INCR表示按照路径权重的升序排序
	- DECR表示按照路径权重的降序排序
- capacity: 遍历过程中最大的访问的顶点数目，选填项，默认为10000000
- limit: 返回的路径的最大数目，选填项，默认为10
- with_vertex：true表示返回结果包含完整的顶点信息（路径中的全部顶点），false时表示只返回顶点id，选填项，默认为 false

##### 3.2.8.2 使用方法

###### Method & Url

```
POST http://localhost:8080/graphs/{graph}/traversers/customizedpaths
```

###### Request Body

```json
{
    "sources":{
        "ids":[

        ],
        "label":"person",
        "properties":{
            "name":"marko"
        }
    },
    "steps":[
        {
            "direction":"OUT",
            "labels":[
                "knows"
            ],
            "weight_by":"weight",
            "degree":-1
        },
        {
            "direction":"OUT",
            "labels":[
                "created"
            ],
            "default_weight":8,
            "degree":-1,
            "sample":1
        }
    ],
    "sort_by":"INCR",
    "with_vertex":true,
    "capacity":-1,
    "limit":-1
}
```

###### Response Status

```json
201
```

###### Response Body

```json
{
    "paths":[
        {
            "objects":[
                "1:marko",
                "1:josh",
                "2:lop"
            ],
            "weights":[
                1,
                8
            ]
        }
    ],
    "vertices":[
        {
            "id":"1:marko",
            "label":"person",
            "type":"vertex",
            "properties":{
                "city":[
                    {
                        "id":"1:marko>city",
                        "value":"Beijing"
                    }
                ],
                "name":[
                    {
                        "id":"1:marko>name",
                        "value":"marko"
                    }
                ],
                "age":[
                    {
                        "id":"1:marko>age",
                        "value":29
                    }
                ]
            }
        },
        {
            "id":"1:josh",
            "label":"person",
            "type":"vertex",
            "properties":{
                "city":[
                    {
                        "id":"1:josh>city",
                        "value":"Beijing"
                    }
                ],
                "name":[
                    {
                        "id":"1:josh>name",
                        "value":"josh"
                    }
                ],
                "age":[
                    {
                        "id":"1:josh>age",
                        "value":32
                    }
                ]
            }
        },
        {
            "id":"2:lop",
            "label":"software",
            "type":"vertex",
            "properties":{
                "price":[
                    {
                        "id":"2:lop>price",
                        "value":328
                    }
                ],
                "name":[
                    {
                        "id":"2:lop>name",
                        "value":"lop"
                    }
                ],
                "lang":[
                    {
                        "id":"2:lop>lang",
                        "value":"java"
                    }
                ]
            }
        }
    ]
}
```

##### 3.2.8.3 适用场景

适合查找各种复杂的路径集合，例如：

- 社交网络中，查找看过张艺谋所导演的电影的用户关注的大V的路径（张艺谋--->电影---->用户--->大V）
- 风控网络中，查找多个高风险用户的直系亲属的朋友的路径（高风险用户--->直系亲属--->朋友）

#### 3.2.10 Vertices

##### 3.2.10.1 根据顶点的id列表，批量查询顶点

###### Params

- ids: 要查询的顶点id列表

###### Method & Url

```
GET http://localhost:8080/graphs/hugegraph/traversers/vertices?ids="1:marko"&ids="2:lop"
```

###### Response Status

```json
200
```

###### Response Body

```json
{
    "vertices":[
        {
            "id":"1:marko",
            "label":"person",
            "type":"vertex",
            "properties":{
                "city":[
                    {
                        "id":"1:marko>city",
                        "value":"Beijing"
                    }
                ],
                "name":[
                    {
                        "id":"1:marko>name",
                        "value":"marko"
                    }
                ],
                "age":[
                    {
                        "id":"1:marko>age",
                        "value":29
                    }
                ]
            }
        },
        {
            "id":"2:lop",
            "label":"software",
            "type":"vertex",
            "properties":{
                "price":[
                    {
                        "id":"2:lop>price",
                        "value":328
                    }
                ],
                "name":[
                    {
                        "id":"2:lop>name",
                        "value":"lop"
                    }
                ],
                "lang":[
                    {
                        "id":"2:lop>lang",
                        "value":"java"
                    }
                ]
            }
        }
    ]
}
```

##### 3.2.10.2 获取顶点 Shard 信息

通过指定的分片大小split_size，获取顶点分片信息（可以与 3.2.10.3 中的 Scan 配合使用来获取顶点）。

###### Params

- split_size: 分片大小，必填项

###### Method & Url

```
GET http://localhost:8080/graphs/hugegraph/traversers/vertices/shards?split_size=67108864
```

###### Response Status

```json
200
```

###### Response Body

```json
{
    "shards":[
        {
            "start": "0",
            "end": "2165893",
            "length": 0
        },
        {
            "start": "2165893",
            "end": "4331786",
            "length": 0
        },
        {
            "start": "4331786",
            "end": "6497679",
            "length": 0
        },
        {
            "start": "6497679",
            "end": "8663572",
            "length": 0
        },
        ......
    ]
}
```

##### 3.2.10.3 根据Shard信息批量获取顶点

通过指定的分片信息批量查询顶点（Shard信息的获取参见 3.2.10.2 Shard）。

###### Params

- start: 分片起始位置，必填项
- end: 分片结束位置，必填项
- page：分页位置，选填项，默认为null，不分页；当page为“”时表示分页的第一页，从start指示的位置开始
- page_limit：分页获取顶点时，一页中顶点数目的上限，选填项，默认为 100000

###### Method & Url

```
GET http://localhost:8080/graphs/hugegraph/traversers/vertices/scan?start=0&end=4294967295
```

###### Response Status

```json
200
```

###### Response Body

```json
{
    "vertices":[
        {
            "id":"2:ripple",
            "label":"software",
            "type":"vertex",
            "properties":{
                "price":[
                    {
                        "id":"2:ripple>price",
                        "value":199
                    }
                ],
                "name":[
                    {
                        "id":"2:ripple>name",
                        "value":"ripple"
                    }
                ],
                "lang":[
                    {
                        "id":"2:ripple>lang",
                        "value":"java"
                    }
                ]
            }
        },
        {
            "id":"1:vadas",
            "label":"person",
            "type":"vertex",
            "properties":{
                "city":[
                    {
                        "id":"1:vadas>city",
                        "value":"Hongkong"
                    }
                ],
                "name":[
                    {
                        "id":"1:vadas>name",
                        "value":"vadas"
                    }
                ],
                "age":[
                    {
                        "id":"1:vadas>age",
                        "value":27
                    }
                ]
            }
        },
        {
            "id":"1:peter",
            "label":"person",
            "type":"vertex",
            "properties":{
                "city":[
                    {
                        "id":"1:peter>city",
                        "value":"Shanghai"
                    }
                ],
                "name":[
                    {
                        "id":"1:peter>name",
                        "value":"peter"
                    }
                ],
                "age":[
                    {
                        "id":"1:peter>age",
                        "value":35
                    }
                ]
            }
        },
        {
            "id":"1:josh",
            "label":"person",
            "type":"vertex",
            "properties":{
                "city":[
                    {
                        "id":"1:josh>city",
                        "value":"Beijing"
                    }
                ],
                "name":[
                    {
                        "id":"1:josh>name",
                        "value":"josh"
                    }
                ],
                "age":[
                    {
                        "id":"1:josh>age",
                        "value":32
                    }
                ]
            }
        },
        {
            "id":"1:marko",
            "label":"person",
            "type":"vertex",
            "properties":{
                "city":[
                    {
                        "id":"1:marko>city",
                        "value":"Beijing"
                    }
                ],
                "name":[
                    {
                        "id":"1:marko>name",
                        "value":"marko"
                    }
                ],
                "age":[
                    {
                        "id":"1:marko>age",
                        "value":29
                    }
                ]
            }
        },
        {
            "id":"2:lop",
            "label":"software",
            "type":"vertex",
            "properties":{
                "price":[
                    {
                        "id":"2:lop>price",
                        "value":328
                    }
                ],
                "name":[
                    {
                        "id":"2:lop>name",
                        "value":"lop"
                    }
                ],
                "lang":[
                    {
                        "id":"2:lop>lang",
                        "value":"java"
                    }
                ]
            }
        }
    ]
}
```

##### 3.2.10.4 适用场景

- 按id列表查询顶点，可用于批量查询顶点，比如在path查询到多条路径之后，可以进一步查询某条路径的所有顶点属性。
- 获取分片和按分片查询顶点，可以用来遍历全部顶点

#### 3.2.11 Edges

##### 3.2.11.1 根据边的id列表，批量查询边

###### Params

- ids: 要查询的边id列表

###### Method & Url

```
GET http://localhost:8080/graphs/hugegraph/traversers/edges?ids="S1:josh>1>>S2:lop"&ids="S1:josh>1>>S2:ripple"
```

###### Response Status

```json
200
```

###### Response Body

```json
{
    "edges": [
        {
            "id": "S1:josh>1>>S2:lop",
            "label": "created",
            "type": "edge",
            "inVLabel": "software",
            "outVLabel": "person",
            "inV": "2:lop",
            "outV": "1:josh",
            "properties": {
                "date": "20091111",
                "weight": 0.4
            }
        },
        {
            "id": "S1:josh>1>>S2:ripple",
            "label": "created",
            "type": "edge",
            "inVLabel": "software",
            "outVLabel": "person",
            "inV": "2:ripple",
            "outV": "1:josh",
            "properties": {
                "date": "20171210",
                "weight": 1
            }
        }
    ]
}
```

##### 3.2.11.2 获取边 Shard 信息

通过指定的分片大小split_size，获取边分片信息（可以与 3.2.11.3 中的 Scan 配合使用来获取边）。

###### Params

- split_size: 分片大小，必填项

###### Method & Url

```
GET http://localhost:8080/graphs/hugegraph/traversers/edges/shards?split_size=4294967295
```

###### Response Status

```json
200
```

###### Response Body

```json
{
    "shards":[
        {
            "start": "0",
            "end": "1073741823",
            "length": 0
        },
        {
            "start": "1073741823",
            "end": "2147483646",
            "length": 0
        },
        {
            "start": "2147483646",
            "end": "3221225469",
            "length": 0
        },
        {
            "start": "3221225469",
            "end": "4294967292",
            "length": 0
        },
        {
            "start": "4294967292",
            "end": "4294967295",
            "length": 0
        }
    ]
}
```

##### 3.2.11.3 根据 Shard 信息批量获取边

通过指定的分片信息批量查询边（Shard信息的获取参见 3.2.11.2）。

###### Params

- start: 分片起始位置，必填项
- end: 分片结束位置，必填项
- page：分页位置，选填项，默认为null，不分页；当page为“”时表示分页的第一页，从start指示的位置开始
- page_limit：分页获取边时，一页中边数目的上限，选填项，默认为 100000

###### Method & Url

```
GET http://localhost:8080/graphs/hugegraph/traversers/edges/scan?start=0&end=3221225469
```

###### Response Status

```json
200
```

###### Response Body

```json
{
    "edges":[
        {
            "id":"S1:peter>2>>S2:lop",
            "label":"created",
            "type":"edge",
            "inVLabel":"software",
            "outVLabel":"person",
            "inV":"2:lop",
            "outV":"1:peter",
            "properties":{
                "weight":0.2,
                "date":"20170324"
            }
        },
        {
            "id":"S1:josh>2>>S2:lop",
            "label":"created",
            "type":"edge",
            "inVLabel":"software",
            "outVLabel":"person",
            "inV":"2:lop",
            "outV":"1:josh",
            "properties":{
                "weight":0.4,
                "date":"20091111"
            }
        },
        {
            "id":"S1:josh>2>>S2:ripple",
            "label":"created",
            "type":"edge",
            "inVLabel":"software",
            "outVLabel":"person",
            "inV":"2:ripple",
            "outV":"1:josh",
            "properties":{
                "weight":1,
                "date":"20171210"
            }
        },
        {
            "id":"S1:marko>1>20130220>S1:josh",
            "label":"knows",
            "type":"edge",
            "inVLabel":"person",
            "outVLabel":"person",
            "inV":"1:josh",
            "outV":"1:marko",
            "properties":{
                "weight":1,
                "date":"20130220"
            }
        },
        {
            "id":"S1:marko>1>20160110>S1:vadas",
            "label":"knows",
            "type":"edge",
            "inVLabel":"person",
            "outVLabel":"person",
            "inV":"1:vadas",
            "outV":"1:marko",
            "properties":{
                "weight":0.5,
                "date":"20160110"
            }
        },
        {
            "id":"S1:marko>2>>S2:lop",
            "label":"created",
            "type":"edge",
            "inVLabel":"software",
            "outVLabel":"person",
            "inV":"2:lop",
            "outV":"1:marko",
            "properties":{
                "weight":0.4,
                "date":"20171210"
            }
        }
    ]
}
```

##### 3.2.11.4 适用场景

- 按id列表查询边，可用于批量查询边
- 获取分片和按分片查询边，可以用来遍历全部边



### 5.1 Graphs


#### 5.1.3 清空某个图的全部数据，包括schema、vertex、edge和index等，**该操作需要管理员权限**

##### Params

由于清空图是一个比较危险的操作，为避免用户误调用，我们给API添加了用于确认的参数：

- confirm_message: 默认为`I'm sure to delete all data`

##### Method & Url

```
DELETE http://localhost:8080/graphs/hugegraph/clear?confirm_message=I%27m+sure+to+delete+all+data
```

##### Response Status

```json
204
```


### 6.1 Task



#### 6.1.1 列出某个图中全部的异步任务

##### Params

- status: 异步任务的状态
- limit：返回异步任务数目上限

##### Method & Url

```
GET http://localhost:8080/graphs/hugegraph/tasks?status=success
```

##### Response Status

```json
200
```

##### Response Body

```json
{
	"tasks": [{
		"task_name": "hugegraph.traversal().V()",
		"task_progress": 0,
		"task_create": 1532943976585,
		"task_status": "success",
		"task_update": 1532943976736,
		"task_result": "0",
		"task_retries": 0,
		"id": 2,
		"task_type": "gremlin",
		"task_callable": "com.baidu.hugegraph.api.job.GremlinAPI$GremlinJob",
		"task_input": "{\"gremlin\":\"hugegraph.traversal().V()\",\"bindings\":{},\"language\":\"gremlin-groovy\",\"aliases\":{\"hugegraph\":\"graph\"}}"
	}]
}
```

#### 6.1.2 查看某个异步任务的信息

##### Method & Url

```
GET http://localhost:8080/graphs/hugegraph/tasks/2
```

##### Response Status

```json
200
```

##### Response Body

```json
{
	"task_name": "hugegraph.traversal().V()",
	"task_progress": 0,
	"task_create": 1532943976585,
	"task_status": "success",
	"task_update": 1532943976736,
	"task_result": "0",
	"task_retries": 0,
	"id": 2,
	"task_type": "gremlin",
	"task_callable": "com.baidu.hugegraph.api.job.GremlinAPI$GremlinJob",
	"task_input": "{\"gremlin\":\"hugegraph.traversal().V()\",\"bindings\":{},\"language\":\"gremlin-groovy\",\"aliases\":{\"hugegraph\":\"graph\"}}"
}
```

#### 6.1.4 取消某个异步任务，**该异步任务必须具有处理中断的能力**

假设已经通过[Gremlin API](gremlin.md)创建了一个异步任务如下：

```groovy
"for (int i = 0; i < 10; i++) {" +
    "hugegraph.addVertex(T.label, 'man');" +
    "hugegraph.tx().commit();" +
    "try {" +
        "sleep(1000);" +
    "} catch (InterruptedException e) {" +
        "break;" +
    "}" +
"}"
```

##### Method & Url

```
PUT http://localhost:8080/graphs/hugegraph/tasks/2?action=cancel
```

> 请保证在10秒内发送该请求，如果超过10秒发送，任务可能已经执行完成，无法取消。

##### Response Status

```json
202
```

##### Response Body

```json
{
    "cancelled": true
}
```

此时查询 label 为 man 的顶点数目，一定是小于 10 的。






## Api-Gremlin使用

## 附件


### 导入案例

hugegraph-loader-0.9.0目录结构

```bash
.
├── bin
│   └── hugegraph-loader
├── conf
│   └── log4j2.xml
├── example
│   ├── file
│   ├── graph_schema.groovy
│   ├── graph_struct.json
│   ├── hdfs
│   └── mysql
├── lib
├── LICENSE
├── logs
│   ├── edge_insert_error.data
│   ├── hugegraph-loader.log
│   ├── parse_error.data
│   └── vertex_insert_error.data
└── README.md
```

数据文件 支持csv/text/json等(详情见官网)

```csv
==> cust_01_100000.csv <==
mob_phone:string,birthday:int,name:string,cust_no:string,cust_namespell:string,address:string,sex:string,id:ID,cust_certtype:string
13965170263,19340324,巢海燕,350124193403249522,chaohaiyan,西藏自治区通辽市海港蔚路x座 213898,女,350124193403249522,2
13844740188,19950101,蒋静,411281199501016156,jiangjing,安徽省金凤县萧山六安路X座 814241,男,411281199501016156,0

==> tran_01_148111.csv <==
tran_amt:float,tran_date:int,:START_ID,tran_cnt:int,:END_ID
455229.75,20170103,110000194107111151,1,141123197707099408
83693.8,20170101,110000194508084959,1,513435194206212598
```

graph_schema.groovy(指定Schema文件)

```groovy
schema.propertyKey("id").asText().ifNotExist().create();
schema.propertyKey("mob_phone").asText().ifNotExist().create();
schema.propertyKey("birthday").asInt().ifNotExist().create();
schema.propertyKey("name").asText().ifNotExist().create();
schema.propertyKey("cust_no").asText().ifNotExist().create();
schema.propertyKey("cust_namespell").asText().ifNotExist().create();
schema.propertyKey("address").asText().ifNotExist().create();
schema.propertyKey("sex").asText().ifNotExist().create();
schema.propertyKey("cust_certtype").asText().ifNotExist().create();

schema.propertyKey("tran_amt").asDouble().ifNotExist().create();
schema.propertyKey("tran_date").asInt().ifNotExist().create();
schema.propertyKey("tran_cnt").asInt().ifNotExist().create();


schema.vertexLabel("cust").properties("id", "mob_phone", "birthday", "name", "cust_no", "cust_namespell", "address", "sex", "cust_certtype").primaryKeys("id").ifNotExist().create();

schema.indexLabel("custByName").onV("cust").by("name").secondary().ifNotExist().create();
schema.indexLabel("custByBirthday").onV("cust").by("birthday").range().ifNotExist().create();


schema.edgeLabel("tran").sourceLabel("cust").targetLabel("cust").properties("tran_amt", "tran_date", "tran_cnt").ifNotExist().create();

schema.indexLabel("tranByTran_amt").onE("tran").by("tran_amt").secondary().ifNotExist().create();
schema.indexLabel("tranByTran_date").onE("tran").by("tran_date").range().ifNotExist().create();
```

graph_struct.json 导入结构文件

(结构文件错误时,导入会出现奇怪报错,注意检查其中参数。存在多指定了headers导致报错Error: More than 1 vertices parsing error ... Stopping)

```json
{
  "vertices": [
    {
      "label": "cust",
      "input": {
        "type": "file",
        "path": "/data/test_data/graph_data/cust.csv",
        "format": "CSV",
        "charset": "UTF-8"
      },
      "mapping": {
        "mob_phone:string":"mob_phone",
        "birthday:int":"birthday",
        "name:string":"name",
        "cust_no:string":"cust_no",
        "cust_namespell:string":"cust_namespell",
        "address:string":"address",
        "sex:string":"sex",
        "id:ID":"id",
        "cust_certtype:string":"cust_certtype"
      }
    }
  ],
  "edges": [
    {
      "label": "tran",
      "source": [":START_ID"],
      "target": [":END_ID"],
      "input": {
        "type": "file",
        "path": "/data/test_data/graph_data/tran.csv",
        "format": "CSV",
        "charset": "UTF-8"
      },
      "mapping": {
        ":START_ID": "id",
        ":END_ID": "id",
        "tran_amt:float": "tran_amt",
        "tran_date:int": "tran_date",
        "tran_cnt:int": "tran_cnt"
      }
    }
  ]
}
```

导入命令 hugegraph-loader-0.9.0目录下执行

```bash
bin/hugegraph-loader -g hugegraph -f example/graph_struct.json -s example/graph_schema.groovy

(fenv) [fdm@neo4j hugegraph-loader-0.9.0]$ time bin/hugegraph-loader -g hugegraph -f example/graph_struct.json -s example/graph_schema.groovy 
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/home/fdm/software/hugegraph/hugegraph-loader-0.9.0/lib/log4j-slf4j-impl-2.8.2.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/home/fdm/software/hugegraph/hugegraph-loader-0.9.0/lib/slf4j-log4j12-1.7.10.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]
log4j:WARN No appenders could be found for logger (org.apache.http.client.protocol.RequestAddCookies).
log4j:WARN Please initialize the log4j system properly.
log4j:WARN See http://logging.apache.org/log4j/1.2/faq.html#noconfig for more info.
Vertices has been imported: 149299
Edges has been imported: 98812
---------------------------------------------
vertices results:
  parse failure vertices   :  0
  insert failure vertices  :  0
  insert success vertices  :  149299
---------------------------------------------
edges results:
  parse failure edges      :  0
  insert failure edges     :  0
  insert success edges     :  98812
---------------------------------------------
time results:
  vertices loading time    :  2
  edges loading time       :  1
  total loading time       :  4

real  0m9.967s
user  0m37.601s
sys  0m2.050s
```

### 使用代码样例

文件名称 hugegraph_tools.py

```python
#! -*- coding:utf-8 -*-
u"""HugeGraph 基础功能使用测试

基础功能

- CURL请求
- 最短路径
- 数据导入

支持说明
- 支持多图查询.支持分库查询 https://hugegraph.github.io/hugegraph-doc/config/config-guide.html
    - TODO 暂未发现,同时查询多库数据,目前只能指定单库数据查询
- Task支持
    - TODO 任务撤销

"""
import sys
import requests
import json
reload(sys)
sys.setdefaultencoding('UTF-8')

IP="192.168.100.162"
PORT=8080
base_url = "http://%s:%s"%(IP,str(PORT))
graph = 'hugegraph'


def requests_delete(url):
    reponse = requests.delete(url)
    return reponse

def requests_put(url,data={},timeout=10):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "PHPSESSID=m2hbrvp548cg6v4ssp0l35kcj7; _ga=GA1.2.2052701472.1532920469; _gid=GA1.2.1351314954.1532920469; __atuvc=3%7C31; __atuvs=5b5e9a0418f6420c001",
        "Host": "en.artprecium.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }
    # 构造form表单
    if not bool(data):
        response = requests.put(url=url, headers=headers, timeout=timeout)
    else:
        response = requests.put(url=url, json=data, headers=headers, timeout=timeout)
    print ">> put请求: ", response.text
    return response


def requests_get(url, params={}):
    u"""Get请求
    """
    print ">>>>>>>>> "
    print url
    response = requests.get(url=url, params=params)
    print(response)  
    print ">> 数据:", json.loads(response.text)
    return response

def requests_post(url,data,timeout=10):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "PHPSESSID=m2hbrvp548cg6v4ssp0l35kcj7; _ga=GA1.2.2052701472.1532920469; _gid=GA1.2.1351314954.1532920469; __atuvc=3%7C31; __atuvs=5b5e9a0418f6420c001",
        "Host": "en.artprecium.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }
    # 构造form表单
    response = requests.post(url=url, data=data, headers=headers, timeout=timeout)
    return response

def task_list(status=None,limit=None):
    u"""列出某个图中全部的异步任务

    status: 异步任务的状态
    limit：返回异步任务数目上限

    GET http://localhost:8080/graphs/hugegraph/tasks?status=success
    """
    defualt_status = ["UNKNOWN"," NEW"," QUEUED"," RESTORING"," RUNNING"," SUCCESS"," CANCELLED"," FAILED"]
    data = {
        'graph':graph,
        'base_url':base_url,
        'status':status,
        'limit':limit,
    }

    url = "{base_url}/graphs/{graph}/tasks".format(**data)
    reponse = requests_get(url)
    return reponse 

def task_info(task_id):
    u"""查看某个异步任务的信息

    http://localhost:8080/graphs/hugegraph/tasks/2
    #  curl -XGET "http://192.168.100.162:8080/graphs/hugegraph/tasks/1"
    """
    data = {
        'base_url':base_url,
        'graph':graph,
        'task_id':task_id,
    }
    url = """{base_url}/graphs/{graph}/tasks/{task_id}""".format(**data)
    reponse = requests_get(url)
    return reponse 


def task_del_taskinfo():
    u"""删除某个异步任务信息，不删除异步任务本身

    http://localhost:8080/graphs/hugegraph/tasks/2
    """
    data = {
        'base_url':base_url,
        'graph':graph,
        'task_id':task_id,
    }
    url = """{base_url}/graphs/{graph}/tasks/{task_id}""".format(**data)
    reponse = requests_delete(url)
    return reponse


def task_cancel(task_id):
    u"""取消某个异步任务，该异步任务必须具有处理中断的能力

    "for (int i = 0; i < 10; i++) {" +
        "hugegraph.addVertex(T.label, 'man');" +
        "hugegraph.tx().commit();" +
        "try {" +
            "sleep(1000);" +
        "} catch (InterruptedException e) {" +
            "break;" +
        "}" +
    "}"
    PUT http://localhost:8080/graphs/hugegraph/tasks/2?action=cancel
    请保证在10秒内发送该请求，如果超过10秒发送，任务可能已经执行完成，无法取消
    """
    pass

    # TODO 未测试
    data = {
        'graph':graph,
        'base_url':base_url,
        'task_id':task_id,
    }
    # UNKNOWN, NEW, QUEUED, RESTORING, RUNNING, SUCCESS, CANCELLED, FAILED
    url = "{base_url}/graphs/{graph}/tasks/{task_id}?action=cancel".format(**data)
    requests_put(url)


def traverser_k_neighbor():
    u"""根据起始顶点，查找N步以内可达的所有邻居

    GET http://localhost:8080/graphs/{graph}/traversers/kneighbor?source=“1:marko”&max_depth=2
    """
    data = {
        'base_url':base_url,
        'graph':graph
    }
    url = """{base_url}/graphs/{graph}/traversers/kneighbor?source="1:77"&max_depth=20""".format(**data)
    reponse = requests_get(url)

def traverser_paths():
    u"""根据起始顶点、目的顶点、方向、边的类型（可选）和最大深度等条件查找所有路径
    source: 起始顶点id，必填项
    target: 目的顶点id，必填项
    direction: 起始顶点向外发散的方向（OUT,IN,BOTH），选填项，默认是BOTH
    label: 边的类型，选填项，默认代表所有edge label
    max_depth: 步数，必填项
    max_degree: 查询过程中，单个顶点最大边数目，选填项，默认为10000
    capacity: 遍历过程中最大的访问的顶点数目，选填项，默认为10000000
    limit: 返回的路径的最大数目，选填项，默认为10
    """
    data = {
        'base_url':base_url,
        'graph':graph
    }
    url = """{base_url}/graphs/{graph}/traversers/paths?source="1:33"&target="1:55"&max_depth=10""".format(**data)
    reponse = requests_get(url)

def traverser_customized_paths():
    u"""根据一批起始顶点、边规则（包括方向、边的类型和属性过滤）和最大深度等条件查找符合条件的所有的路径
    """
    pass
    data = {
        'graph':graph,
        'base_url':base_url,
    }
    url = """{base_url}/graphs/{graph}/graph/traversers/customizedpaths""".format(**data)
    data = {
            "sources":{
                "ids":[
                    "1:10",
                    "1:11",
                    "1:12",
                    "1:13",
                    "1:14",
                    "1:15",
                ],
                "label":"person",
                "properties":{
                    "name":"birthday"
                }
            },
            "steps":[
                {
                    "direction":"BOTH",
                    "labels":[
                        "tran"
                    ],
                    "default_weight":8,
                    "degree":-1,
                    "sample":1
                }
            ],
            "sort_by":"INCR",
            "with_vertex":True,
            "capacity":-1,
            "limit":-1
        }
    requests_post(url,data)

def traverser_shortest(graph,source,target,max_depth,direction="BOTH",label=None,max_degree=10000,skip_degree=0,capacity=10000000):
    u""" 寻找最短路径

    @param graph: 图名称，必填项
    @param source: 起始顶点id，必填项
    @param target: 目的顶点id，必填项
    @param direction: 起始顶点向外发散的方向（OUT,IN,BOTH），选填项，默认是BOTH
    @param max_depth: 最大步数，必填项
    @param label: 边的类型，选填项，默认代表所有edge label
    @param max_degree: 查询过程中，单个顶点最大边数目，选填项，默认为10000
    @param skip_degree: 查询过程中需要跳过的顶点的最小的边数目，即当顶点的边数目大于 skip_degree 时，跳过该顶点，可用于规避超级点，选填项，默认为0，表示不跳过任何点
    @param capacity: 遍历过程中最大的访问的顶点数目，选填项，默认为10000000

    # 官网案列 
    # https://hugegraph.github.io/hugegraph-doc/clients/restful-api/traverser.html

    exp:
        http://localhost:8080/graphs/{graph}/traversers/shortestpath?source="1:marko"&target="2:ripple"&max_depth=3
    """
    data = {
        'graph':graph,
        'base_url':base_url,
        'source':source,
        'target':target,
        'direction':direction,
        'label':label,
        'max_depth':max_depth,
    }
    url = """{base_url}/graphs/{graph}/traversers/shortestpath?source="{source}"&target="{target}"&direction={direction}&label={label}&max_depth={max_depth}""".format(**data)
    requests_get(url)

    return url

def vertex_search(label,limit=100):
    u""" 指定条件查询顶点信息

    GET http://localhost:8080/graphs/hugegraph/graph/vertices?label=person&properties={"age":29}&limit=1
    """
    data = {
        'graph':graph,
        'base_url':base_url,
        'limit':limit,
        'label':label,
    }
    url = """{base_url}/graphs/{graph}/graph/vertices?label={label}&limit={limit}""".format(**data)
    requests_get(url)


def edge_search(vertex_id,direction,label):
    u"""
    GET http://127.0.0.1:8080/graphs/hugegraph/graph/edges?vertex_id="1:josh"&direction=BOTH&label=created&properties={}
    """
    data = {
        'graph':graph,
        'base_url':base_url,
        'vertex_id':vertex_id,
        'direction':direction,
        'label':label
    }
    url = """{base_url}/graphs/{graph}/graph/edges?vertex_id="{vertex_id}"&direction={direction}&label={label}""".format(**data)
    requests_get(url)


def muti_graphs():
    u""" 多库查询说明

    参考官方链接:
        https://hugegraph.github.io/hugegraph-doc/config/config-guide.html
    增加库操作流程说明:
        1. 复制配置文件  conf/hugegraph.properties 
        2. 修改配置文件  
            1. conf/gremlin-server.yaml 
            2. conf/rest-server.properties
        3. 重启服务
            1. bin/stop-hugegraph.sh
            2. bin/init-store.sh
            3. 关闭 hugegraph-studio
            4. bin/start-hugegraph.sh
            5. hugegraph-studio 不支持连接多库...每个库一个配置文件
        4. 使用说明
            1. 查询过程中可以指定图库
    """
    pass


if __name__ == '__main__':
    traverser_k_neighbor()
    traverser_paths()
    traverser_customized_paths()
    traverser_shortest(graph="hugegraph",source="1:10",target="1:95",max_depth=5,label='tran')

    task_list()
    task_info(task_id=2)
    task_cancel(task_id=2)

    edge_search("1:10","BOTH","tran")
    vertex_search('cust')
```

### 问题







