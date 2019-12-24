# Pandas 命令大全

[toc]

## Pandas 简介

Pandas 是 python 的一个数据分析包，最初由 AQR Capital Management 于 2008 年 4 月开发，并于 2009 年底开源出来，目前由专注于 Python 数据包开发的 PyData 开发 team 继续开发和维护，属于 PyData 项目的一部分。Pandas 最初被作为金融数据分析工具而开发出来，因此，pandas 为时间序列分析提供了很好的支持。 Pandas 的名称来自于面板数据（panel data）和 python 数据分析（data analysis）。panel data 是经济学中关于多维数据集的一个术语，在 Pandas 中也提供了 panel 的数据类型。

1. Pandas 官网文档: [https://pandas.pydata.org/pandas-docs/stable/](https://pandas.pydata.org/pandas-docs/stable/)
2. Numpy 官方文档: [https://docs.scipy.org/doc/](https://docs.scipy.org/doc/)

### Pandas 数据类型

**Pandas 所支持的数据类型:**

1. float/float64
2. int/int64
3. bool
4. datetime64[ns]
5. datetime64[ns, tz]
6. timedelta[ns]
7. category
8. object

## Pandas 增加

**指定列名:**

```python
df.to_csv("cnn_predict_result.csv",encoding="utf_8_sig",index=False,columns=columns)
```

**数据汇总:**

```python
groupby_col = ["a","b","c"]
sum_col = "amount"
df_new = df.groupby(groupby_col)[[sum_col]].sum()
```

**DataFrame 转 list:**

```python
np.array(data_x).tolist()
```

**字符串按照 | 分割:**

```python
data['name'].str.split('|',expand=True)
```

**series 转 DataFrame 处理:**

```python
# data['xx'] = df.groupby(groupby_cols_li)[sum_col].count()
# pandas DataFrame groupby 之后转为 series 字段显示不容易处理
#                   _key
# cust_name  cust
# 吐尔逊姑   384    384
# 帕拉哈提   6203  6203
# 使用 reset_index() 重设索引 series,自动转DataFrame解决问题

a= df.groupby(groupby_col)[sum_col].sum()
In [169]: a.to_frame()
Out[169]:
                 _key
cust_name  cust
吐尔逊姑阿吾提    384    384
帕拉哈提       6203  6203
帕提古力·麦麦提赛来 6109  6109
海生林        1372  1372
In [185]: a.reset_index()
Out[185]:
    cust_name  cust  _key
0     吐尔逊姑阿吾提   384   384
1        帕拉哈提  6203  6203
2  帕提古力·麦麦提赛来  6109  6109
3         海生林  1372  1372
```

**按照数据类型区分:**

```python
# 将df按照指定字段值拆分成多个小df
In [73]: df
Out[73]:
  aa bb cc
0  a  b  c
1  1  2  3
2  2  3  4

In [71]:  df[df["aa"].isin([2])]
Out[71]:
  aa bb cc
2  2  3  4

In [72]:  df[df["aa"].isin(["a"])]
Out[72]:
  aa bb cc
0  a  b  c

set(list(df.agg("aa"))) # 获取单列的值种类
```

**判断空值:**

df['$open'].isnull().any() # 判断 open 这一列列是否有 NaN
df['$open'].isnull().all() # 判断 open 列是否全部为 NaN

**字符切割，切割中文:**

1. 必须要 utf-8 编码
2. 使用 slice 切割
3. 全空列先剔除

```python
df = pd.read_csv(file_path,sep='|',low_memory=False,encoding='utf-8')
if df[col].isnull().all():
    continue
df[col] = df[col].str.slice(start=0,stop=-2,step=None)
```

**low_memory:**

默认 low_memory=True,使用低内存加载数据，但是可能存在类型混淆的情况
需要 low_memory=False 或者指定字段类型

```python
df = pd.read_csv('somefile.csv', low_memory=False, dtype=str)
```

**pandas 转换为时间格式**
df = pd.read_csv(fp, dtype=str,sep='|')
df["JY_JYSJ"] = pd.to_datetime(df["JY_JYSJ"], format="%Y-%m-%d%H:%M:%S")
df.to_csv(fp, index=False,sep='|')

## Pandas 删除

**删除 指定列。含空数据的行:**

```python
可以通过subset参数来删除在age和sex中含有空数据的全部行
df4 = df4.dropna(subset=["age","sex"])
```

**删除 全空列:**

```python
df = df.dropna(axis=1,how='all')
axis参数说明axis = 1 行处理 默认axis = 1 列处理
```

删除含有空数据的全部行

```python
df4 = pd.read_csv('4.csv', encoding='utf-8')
df4 = df4.dropna()
```

删除含有空数据的全部列

```python
可以通过axis参数来删除含有空数据的全部列
df4 = df4.dropna(axis=1)
```

## Pandas 修改

**精度处理**
df.round({'A': 1, 'C': 2})

**字段重命名:**

`$a` 重命名为 a 无返回值 d

```python
df.rename(columns={'$a': 'a', '$b': 'b'}, inplace=True)
# inplace 直接修改，所以无返回值。 inplace=False 不直接修改，故有返回值
```

**指定列填充值:**

```python
col = "aaaaa"
df[col] = df[col].ffill(0)
```

**列函数处理:**

```python
# 整列每行采用同一个函数处理
c=c[["a","b"]].apply(foo,axis=1)
```

**数据去重 drop_duplicates:**

```python
df.drop_duplicates([cols],inplace=True)
df.drop_duplicates(subset='id:ID',keep='first',inplace=True)
```

**查看开头为 xxx 的字符 .str.startswith('0'):**

```python
df["JY_FROM_CERTID"] = df[df["JY_FROM_CERTID"].str.startswith('0')]
```

**去除指定左边开头的字符 str.lstrip("9"):**

```python
df["JY_FROM_CERTID"] =  df["JY_FROM_CERTID"].str.lstrip("9")
```

**pandas 列类型转换为 日期格式:**

```python
# # 方法1
df['date'] = pd.to_datetime(df['date'])df.set_index("date", inplace=True)
# 方法2
df2.index = pd.DatetimeIndex(df2["date"])
del df2["date"]
结论：.to_datetime仅转换格式，.DatetimeIndex还能设置为索引
```

**类型转换:**

```python
str float int datetime
df[col] = df[col].astype('str')
# 不能使用  df[col].astype('str',inplace=True)
```

**替换科学计数法:**

将字段类型转为 int64，即可去除科学计数法。
但是空值转换会报错，所以需要先填充空值

```python
data2[['col1','col2']] = data2[['col1','col2']].fillna(-1)
data2[['col1','col2']] = data2[['col1','col2']].astype('int64',errors='ignore')
```

当 int 类型进行 concat 合并的时候，有可能会出现科学计数法，需要先转为 object.

**Numpy 全局设置无科学计数法:**

```python
import numpy as np
np.set_printoptions(suppress=True, threshold=np.nan)
# suppress=True 取消科学记数法
# threshold=np.nan 完整输出（没有省略号）
```

**Pandas 全局设置完整输出:**

```python
import pandas as pd
pd.set_option('display.max_columns', 10000, 'display.max_rows', 10000)
# display.max_columns 显示最大列数
# display.max_rows 显示最大行数
```

**数据合并:**

参考链接：

- [pandas 的 concat 函数和 append 方法](http://www.cnblogs.com/wzdLY/p/9673767.html)
- [PANDAS 数据合并与重塑（join/merge 篇）](https://www.cnblogs.com/bigshow1949/p/7016235.html)

```python
concatdf_new = pd.concat([df1,df2])

```

## Pandas 查询

**列表查询 in 和 not in:**

方法 1: merge 实现

```python
df = pd.DataFrame({'countries':['US','UK','Germany','China']})
countries = pd.DataFrame({'countries':['UK','China'], 'matched':True})

# IN
df.merge(countries,how='inner',on='countries')

# NOT IN
not_in = df.merge(countries,how='left',on='countries')
not_in = not_in[pd.isnull(not_in['matched'])]
```

方法 2: apply

```python
criterion = lambda row: row['countries'] not in countries
not_in = df[df.apply(criterion, axis=1)]
```

**pandas 行列循环:**

```python
df.iterrows()
```

## Pandsa 注意事项

**replace 会导致空列类型变更，object->float:**

```python
tran_dfs[col] = tran_dfs[col].replace("nan",np.nan)
```

**astype(str)会导致空值变成字符串 nan:**

```python
tran_dfs[col] = tran_dfs[col].astype(str)



Pandas天坑：
1、replace，使用replace必须注意method参数，默认为"pad"及填充，会造成replace("", None) 用前值进行补充，必须改为method=None
2、pd.isnull  使用isnull判断时，空值string不认为是空，故需要同时判别数值空或字符空时，在这之前将整个df.replace("", np.nan, method=None)
3、groupby 若groupby字段中存在空置，会造成空置列数据不进入统计，故在group前转换为字符, df.replace(np.nan, "", method=None)
4、merge 若两列字符进行拼接，若列中存在空置，会报错提示无法处理object与float类型，故merge时同样需要将列进行replace为空字符

5、将列强制类型转换为str时，空值会变成'nan'字符

6. replace后，会造成列类型变更为float。 列全空时会存在此情况。列不为全空时，类型不会变更。
replace后会对列类型进行重新检查。从而导致列类型变更。


In [32]: import numpy as np;df = pd.DataFrame([[np.nan,np.nan],[np.nan,4],[np.nan,np.nan]],columns=['a',"b"],dtype=str)
In [33]: df.dtypes
Out[33]:
a    object
b    object
dtype: object

In [34]:  df['a'] = df['a'].replace('1',"11111", method=None);df.dtypes
Out[34]:
a    float64
b     object
dtype: object



```

## Pandas 功能模块

### 取出重复数据

drop_duplicates 为我们提供了数据去重的方法,那怎么得到哪些数据有重复呢?
实现步骤：

采用 drop_duplicates 对数据去两次重，一次将重复数据全部去除（keep=False）记为 data1,另一次将重复数据保留一个（keep='first）记为 data2;
求 data1 和 data2 的差集即可:data2.append(data1).drop_duplicates(keep=False)

### 两列转为字典格式

使用 set_index 将 key 变更为索引列。
使用 to_dict 生成 索引-value 的字典

```python
In [30]: print df[['col','name']][0:2]
             col    name
2    ACCT_NATURE    账户属性
3  ACCT_NET_CITY  开户网点_市

In [29]: df[['col','name']].set_index('col').to_dict()['name'] 
Out[29]:
{'ACCT_CLASS': '\xe8\xb4\xa6\xe6\x88\xb7\xe7\xb1\xbb\xe5\x88\xab',
 'ACCT_CLOSE_DATE': '\xe9\x94\x80\xe6\x88\xb7\xe6\x97\xa5\xe6\x9c\x9f',
}
```

### 中文切割

dtype=unicode

Pandas 对中文进行切割时，必须使用 unicode

```python
        df['CERT_LEFT_2'] = df['CUST_CERTNO'].str.slice(0, 2)
        df['CERT_LEFT_4'] = df['CUST_CERTNO'].str.slice(0, 4)

```

### 日期-最大最小值

```python
df['JY_JYSJ'].astype('datetime64').max()
```

### 统计出现频次

### 新加一行

df3.loc['new'] = ['a','a','a','a']

### 设置空列 reindex

```python
In [20]: df
Out[20]:
   a
0  1
1  2
In [21]: df.reindex(columns=['a','b'])
Out[21]:
   a   b
0  1 NaN
1  2 NaN
In [27]: df.dtypes
Out[27]: 
a    object
dtype: object

In [28]: df.reindex(columns=['a','b']).dtypes
Out[28]: 
a     object
b    float64
dtype: object

# 注意类型问题

# 没有inplace参数
df = df.reindex(columns=['a','b'])
```

### 忽略大小写替换字符
```python
# df.astype(str).apply(lambda x: re.sub('nan', 'sss', x, flags=re.IGNORECASE)) 忽略大小写替换字符
```


### 读取时指定类型和字段名称

```python
    cust_df = pd.read_csv(nj_config['cust']['filepath'], dtype=str, sep='|', names=nj_config['cust']['name_code_dic'].keys()).dropna(how="all")

```


### 判断列空

```python
df['$open'].isnull().any() # 判断open这一列列是否有 NaN

df['$open'].isnull().all()  # 判断open列是否全部为NaN

df.isnull().all()  # 判断某列是否全部为NaN
```
### 数据类型转换


```python


_STRICT_MODE = "raise"
_MIDDLE_MODE = "coerce"
_EASY_MODE = "ignore"

        acct_df[curr] = pd.to_numeric(acct_df[curr].astype(str).\
            str.replace(",", "").replace("nan", "0"), errors=VERIFY_MODE,downcast='float')


end_date = pd.to_datetime(df_tranjrnl['TRAN_DATE'], errors='coerce').dt.date.max()
```

### Pandas bool值取反

```python
In [16]: a =np.array([True,False,True,True,False])

In [17]: c = (1-a).astype(np.bool)

In [18]: c

Out[18]: array([False,  True, False, False,  True])

```


### Pandas   groupby + apply + sortValues


```python
来个例子， groupby + apply + sortValues的例子
data.groupby('customer_id')['repayment_date'].apply(lambda x:x.sort_values(ascending=False)).reset_index()
```