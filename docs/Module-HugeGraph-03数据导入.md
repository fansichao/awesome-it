# HugeGraph 数据导入

tags: HugeGraph 图库 2019 年 11 月

## 导入案例

hugegraph-loader-0.9.0 目录结构

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

数据文件 支持 csv/text/json 等(详情见官网)

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

graph_schema.groovy(指定 Schema 文件)

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

(结构文件错误时,导入会出现奇怪报错,注意检查其中参数。存在多指定了 headers 导致报错 Error: More than 1 vertices parsing error ... Stopping)

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
        "mob_phone:string": "mob_phone",
        "birthday:int": "birthday",
        "name:string": "name",
        "cust_no:string": "cust_no",
        "cust_namespell:string": "cust_namespell",
        "address:string": "address",
        "sex:string": "sex",
        "id:ID": "id",
        "cust_certtype:string": "cust_certtype"
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

导入命令 hugegraph-loader-0.9.0 目录下执行

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
