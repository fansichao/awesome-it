&& Python_SqlAlchemy

[toc]

&& 00 简介说明

SQLAlchemy 是 Python 编程语言下的一款 ORM 框架，该框架建立在数据库 API 之上，使用关系对象映射进行数据库操作，
简言之便是：将对象转换成 SQL，然后使用数据 API 执行 SQL 并获取执行结果。

SQLAlchemy SQL Toolkit 和 Object Relational Mapper 是一套用于处理数据库和 Python 的综合工具。
它具有几个不同的功能区域，可以单独使用或组合使用。其主要组件如下所示，组件依赖关系按层组织：

![](https://docs.sqlalchemy.org/en/latest/_images/sqla_arch_small.png)

上面，SQLAlchemy 的两个最重要的前端部分是**Object Relational Mapper**和 **SQL Expression Language**。
SQL 表达式可以独立于 ORM 使用。使用 ORM 时，SQL 表达式语言仍然是面向公众的 API 的一部分，因为它在对象关系配置和查询中使用。

$$$ 文档概述

文档分为三个部分：SQLAlchemy ORM， SQLAlchemy Core 和 Dialects。

在 SQLAlchemy ORM 中，引入并完整描述了对象关系映射器。新用户应该从对象关系教程开始。如果您想使用为您自动构建的更高级别的 SQL，以及 Python 对象的管理，请继续阅读本教程。

在 SQLAlchemy Core 中，记录了 SQLAlchemy 的 SQL 和数据库集成和描述服务的广度，其核心是 SQL 表达式语言。
SQL 表达式语言是一个独立于 ORM 包的工具包，它可用于构造可操作的 SQL 表达式，可以通过编程方式构造，修改和执行，返回类似游标的结果集。
与 ORM 以域为中心的使用模式相反，表达式语言提供了以模式为中心的使用范例。
新用户应该从这里开始使用 SQL Expression Language Tutorial。SQLAlchemy 引擎，连接和池服务也在 SQLAlchemy Core 中描述 。

在 Dialects 中，提供了所有提供的数据库和 DBAPI 后端的参考文档。

$$$ 框架说明

官网链接： http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
不同 ORM 框架对比说明
https://www.oschina.net/translate/sqlalchemy-vs-orms
常见命令
https://www.imooc.com/article/details/id/22343
常见命令 2
https://www.cnblogs.com/booolee/archive/2009/08/26/1554525.html
sqlalchemy 框架说明
https://nettee.github.io/posts/2016/SQLAlchemy-Translation/

$$$ 框架对比

```python
sqlalchemy的使用
1.sqlalchemy的使用
数据库表结构
[
    ('1', 'Michael'),
    ('2', 'Bob'),
    ('3', 'Adam')
]
ORM技术
ORM技术：Object-Relational Mapping，把关系数据库的表结构映射到对象上
在Python中，最有名的ORM框架是SQLAlchemy
用法setp1：第一步，导入SQLAlchemy，并初始化DBSession：
&& 导入:
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


&& 创建对象的基类:
Base = declarative_base()

&& 定义User对象:
class User(Base):
    && 表的名字:
    __tablename__ = 'user'

    && 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))

&& 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')
&& 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
create_engine()用来初始化数据库连接。SQLAlchemy用一个字符串表示连接信息：
'数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
setp2:使用session对象  --  Session对象可视为当前数据库连接。
&& 创建session对象:
session = DBSession()
&& 创建新User对象:
new_user = User(id='5', name='Bob')
&& 添加到session:
session.add(new_user)
&& 提交即保存到数据库:
session.commit()
&& 关闭session:
session.close()
step3:查询数据库表
如何从数据库表中查询数据呢？有了ORM，查询出来的可以不再是tuple，而是User对象。SQLAlchemy提供的查询接口如下
&& 创建Session:
session = DBSession()
&& 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
user = session.query(User).filter(User.id=='5').one()
&& 打印类型和对象的name属性:print 'type:', type(user)
print 'name:', user.name
&& 关闭Session:
session.close()


运行结果如下：
type: <class '__main__.User'>
name: Bob
可见，ORM就是把数据库表的行与相应的对象建立关联，互相转换。
setp4：ORM的外键关联 -- relationship(向外连接), ForeignKey(连接主键)
由于关系数据库的多个表还可以用外键实现一对多、多对多等关联，相应地，ORM框架也可以提供两个对象之间的一对多、多对多等功能。
例如，如果一个User拥有多个Book，就可以定义一对多关系如下：
class User(Base):
  __tablename__ = 'user'
  id = Column(String(20), primary_key=True)
  name = Column(String(20))
  && 一对多:
  books = relationship('Book')
class Book(Base):
  __tablename__ = 'book'
  id = Column(String(20), primary_key=True)
  name = Column(String(20))
  && “多”的一方的book表是通过外键关联到user表的:
  user_id = Column(String(20), ForeignKey('user.id'))
当我们查询一个User对象时，该对象的books属性将返回一个包含若干个Book对象的list。
小结
ORM框架的作用就是把数据库表的一行记录与一个对象互相做自动转换。
正确使用ORM的前提是了解关系数据库的原理
```

!!!! 为什么用 SQLAlchemy

用 SQLAlchemy 的主要原因是，把你从底层的数据库和 SQL 奇葩语法中解放出来。SQLAlchemy 将常用语句和类型和 SQL 语句对应起
来，让你可以更容易地理解数据库类型，而不需要担心太多细节。这样在处理像 Oracle 到 PostgreSQL 数据库这类的迁移工作，或从一个应用数据库
到数据仓库时，事情就简单了。它还能确保数据在增加到数据库之前是经过安全的，适当转义处理的。这样可以避免 SQL 注入之类的事情发生。

SQLAlchemy 通过两个主要的模型来实现灵活的操作：SQL 表达式语言（通常也叫 Core）和 ORM（Object-relational mapping，对象关系映射）。这两个模型可以根据你的需要独立使用，也可以合在一起使用。

**SQLAlchemy Core 和 SQL 表达式语言**

SQL 表达式语言是用 Pythonic 方式的来表达 SQL 语句和表达式，只是对传统的 SQL 语言的轻微抽象。它侧重于实用数据库的模式
（schema，其实是具体到一个 Tabel 和 View 等），但是它实现了不同数据库之间标准化的接口。SQL 表达式语言也是 SQLAlchemy
ORM 的基础。

**ORM**

SQLAlchemy ORM 与你在其他语言里遇到的 ORM 类似。它侧重于应用的 Domain
Model（一种将数据与其行为集成在一起的模式），借助工作单元的模式来维护对象状态。它还在 SQL 表达式语言之上增加了一层抽象，让用户可以更容易的
操作数据库。你可以把 ORM 和 SQL 表达式语言结合起来构建强大的应用。ORM 构建了一个声明式的系统，与许多其他 ORM 模型（如 Ruby on
Rails）使用的 active-record systems 类似。

虽然 ORM 非常有用，但是你要注意，类的很多用法与数据库的工作方式是不一样的。我们将在后面的章节介绍这些差异。

!!!! Core 和 ORM 的选择

究竟是选择 Core 还是 ORM 作为应用的数据链接层呢？除了个人喜好，理由可以归结为一些影响因素。这两种模式的语法不太一样，但 Core 和 ORM 最大的差异是 Core 对数据模式和业务对象（business objects）的不同处理方式。

SQLAlchemy Core 是以模式为中心，和普通 SQL 一样有表，键和索引等。SQLAlchemy
Core 最擅长的时数据仓库，报表分析，以及其他使用数据查询和其他操作可以牢牢掌控的地方。它拥有强大的数据库连接池（ connection
pool）和数据结果集（ResultSet）优化，非常适合处理大量数据，甚至多数据库也适用。

但是，如果你更侧重于领域驱动设计(domain driven design)，
那么 ORM 就可以将原数据和业务对象的底层的模式和结构大部分细节都封装起来。这样封装让数据库连接更简单，更像 Python 代码。大多数应用都更适合按
照这种方法建模。ORM 可以用一种非常高效的方法把领域驱动设计方法导入传统应用，或者改造原来带有原始 SQL 语句的应用。还有一个好处就是，通过对底层
数据库的合理抽象，ORM 让开发者把精力更多地集中在业务流程的实现上。

不过，ORM 是建立在 SQLAlchemy Core 基础之上的，你可以把处理 MySQL 的同样方式用于 Oracle 的数据仓库和 Amazon Redshift 数据库。当你需要业务对象和仓库数据时，ORM 可以无缝的衔接每个环节。

如果你的应用框架已经使用了 ORM，但是想要更强大的报表功能，使用 Core

如果你不想像普通 SQL 一样以模式为中心，用 ORM

如果你的数据不需要业务对象，用 Core

如果你把数据看成业务对象，用 ORM

如果要建立快速原型，用 ORM

如果你既要业务对象，又要其他数据无关的功能（报表，数据分析等等），两个都用。

&& 01 基础使用

$$$ 数据库连接

以 MySQL 为例，

- URL 格式 `mysql+{driver}://{username}:{password}@{host}:{port}/{name}，`
- driver 是 Python 的数据库驱动，比如 MySQL 官方的数据库驱动 mysql-connector-python，driver 是 mysqlconnector；
- username 是数据库用户名；
- password 是密码；
- host 是数据库主机；
- port 是数据库端口；
- name 是数据库名。

DB2 的 URL 格式： `URL ='ibm_db_sa://lqr:qwe123@155.104.1.141:50000/lqr'`

ORACLE 的 URL 格式： `"oracle://$DB_USER:$DB_PASSWD@$DB_HOST:$DB_PORT/$DB_INSTANCE"`

$$$ 连接代码

```python
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

db_url = "mysql+mysqlconnector://root:@localhost:3306/test"

&& 通过数据库连接url创建数据库引擎
&& 如果想回显SQLAlchemy操作数据库的日志，设置echo=True
engine = create_engine(db_url, echo=True)

&& 通过数据库引擎绑定元信息
metadata = MetaData(engine)

&& 通过绑定数据库引擎获取数据库会话类
Session = sessionmaker(bind=engine)

&& 获取数据库会话
session = Session()
```

$$$ 数据准备

以 ORM 方式来对数据库中的数据做增删查改操作是通过 Session 实例来完成的，
在学习了解如何以 ORM 方式操作数据之前首先我们要对数据的状态有个基本的了解。

首先在 ORM 中，数据库中的数据表对应于 Python 中的类，而数据表中的记录对应于类的实例对象。
因此，对数据表中的记录进行增删查改在 Python 中实际上就是对实例对象的操作。
数据实例对象有四种状态，分别是

Transient - （瞬时的）

表示该实例对象不在 session 中，当然也没有保存到数据库中，
主键一般情况下为 None（如果一个 Persistent 状态的对象进行事务回滚后虽然主键有值，但却是 Transient 状态）。

Pending - （挂起的）

调用 session.add()后，Transient 状态的对象就会变成 Pending 状态的对象，这个时候它只是在 session 中，
并没有保存到数据库，因此主键依旧为 None。
只有触发了 session.flush()操作才会保存到数据库使得主键有值，比如查询操作就会触发 flush。

Persistent - （持久的）
session 和数据库中都有对应的记录存在，为持久状态。

Detached - （游离的）
数据库中可能有记录，但是 session 中不存在。对这种对象的操作不会触发任何 SQL 语句。
要查看数据对象的状态可以用如下方式

```
>>> from sqlalchemy import inspect
>>> status = inspect(data_object)
>>> status.persistent
True
```

&& 02 命令大全

[toc]

$$$ ORM 框架命令

!!!! 常用数据类型和参数

数据库的数据类型和常用参数示例

```python
import sqlalchemy
from datetime import datetime
from sqlalchemy import create_engine,Column,Integer,String,Text,Boolean,Date,DateTime,Float
from sqlalchemy.ext.declarative import declarative_base
&& ======================================================================================================================

&& 数据库的数据类型和常用参数示例

&& 1. Integer：整形，映射到数据库中的int类型。
&& 2. String：字符类型，映射到数据库中的varchar类型，使用时，需要提供一个字符长度。
&& 3. Text：文本类型，映射到数据库中的text类型。
&& 4. Boolean：布尔类型，映射到数据库中的bool类型，在使用的时候，传递`True/False`进去。
&& 5. Date：日期类型，没有时间。映射到数据库中是`date`类型，在使用的时候，传递`datetime.date()`进去。
&& 6. DateTime：日期时间类型。映射到数据库中的是`datetime`类型，在使用的时候，传递`datetime.datetime()`进去。
&& 7. Float：浮点类型。

&& 1. `primary_key`：主键，True和False。
&& 2. `autoincrement`：是否自动增长，True和False。
&& 3. `unique`：是否唯一。
&& 4. `nullable`：是否可空，默认是True。
&& 5. `default`：默认值。
&& 6. `onupdate`：在更新的时候，一般用在时间上面。
```

!!!! 常用接口/包导入

记录`sqlalchemy`的 API 导入

```python
&& 常用包引入
from sqlalchemy import and_, func, or_

```

!!!! 详细接口/包导入

Sqlchemy 常用 API 接口、参数。

@@@@@ Sqlchemy 接口/包导入

```python
import sqlalchemy
print dir(sqlalchemy)
In [2]: print dir(sqlalchemy)
['ARRAY', 'BIGINT', 'BINARY', 'BLANK_SCHEMA', 'BLOB', 'BOOLEAN', 'BigInteger', 'Binary', 'Boolean', 'CHAR', 'CLOB', 'CheckConstraint', 'Column', 'ColumnDefault', 'Constraint', 'DATE', 'DATETIME', 'DDL', 'DECIMAL', 'Date', 'DateTime', 'DefaultClause', 'Enum', 'FLOAT', 'FetchedValue', 'Float', 'ForeignKey', 'ForeignKeyConstraint', 'INT', 'INTEGER', 'Index', 'Integer', 'Interval', 'JSON', 'LargeBinary', 'MetaData', 'NCHAR', 'NUMERIC', 'NVARCHAR', 'Numeric', 'PassiveDefault', 'PickleType', 'PrimaryKeyConstraint', 'REAL', 'SMALLINT', 'Sequence', 'SmallInteger', 'String', 'TEXT', 'TIME', 'TIMESTAMP', 'Table', 'Text', 'ThreadLocalMetaData', 'Time', 'TypeDecorator', 'Unicode', 'UnicodeText', 'UniqueConstraint', 'VARBINARY', 'VARCHAR', '__all__', '__builtins__', '__doc__', '__file__', '__go', '__name__', '__package__', '__path__', '__version__', 'alias', 'all_', 'and_', 'any_', 'asc', 'between', 'bindparam', 'case', 'cast', 'collate', 'column', 'cprocessors', 'create_engine', 'cresultproxy', 'cutils', 'delete', 'desc', 'dialects', 'distinct', 'engine', 'engine_from_config', 'event', 'events', 'exc', 'except_', 'except_all', 'exists', 'extract', 'false', 'func', 'funcfilter', 'insert', 'inspect', 'inspection', 'interfaces', 'intersect', 'intersect_all', 'join', 'lateral', 'literal', 'literal_column', 'log', 'modifier', 'not_', 'null', 'nullsfirst', 'nullslast', 'or_', 'outerjoin', 'outparam', 'over', 'pool', 'processors', 'schema', 'select', 'sql', 'subquery', 'table', 'tablesample', 'text', 'true', 'tuple_', 'type_coerce', 'types', 'union', 'union_all', 'update', 'util', 'within_group']
```

$$$ 增删改查

!!!! 查询-query

```python
&& 查询去重
session.query(Phone.brand).distinct().all()
&& 查询数据是否存在
session.query(User).filter(exists().where(Address.user_id == User.id))
session.query(User).filter(User.addresses.any())
&& 查询数据条数
sessino.query(User).all().count()

&& 查询模糊匹配
session.query(User).filter(User.code.like('%'+code.strip().upper()+'%')).all()
```

**查询-func 函数**

```python
from sqlalchemy import func
&& 忽略大小写
session.query(User).filter(func.upper(User.code)=='AAA').all()
session.query(User).filter(func.lower(User.code)=='aaa').all()
&& 日期格式转字符
session.query(User).filter(func.to_char(User.code)=='2018-01-01').all()
&& 列表查询 + 倒序/顺序查询
from sqlalchemy import asc, desc
User.query.filter(User.id.in_((1, 2, 3))).order_by(desc(User.datetime)).all()
&&
```

**简单查询**

```python
session.query(User).all()
session.query(User.name, User.fullname).all()
session.query(User, User.name).all()
```

**带条件查询** filter_by filter like

```
session.query(User).filter_by(name='user1').all())
session.query(User).filter(User.name == "user").all())
print(session.query(User).filter(User.name.like("user%")).all()
```

**多条件查询** and* or* like ilike

```python
print(session.query(User).filter(and_(User.name.like("user%"), User.fullname.like("first%"))).all())
print(session.query(User).filter(or_(User.name.like("user%"), User.password != None)).all())
```

**sql 过滤** filter params

```python
session.query(User).filter("id>:id").params(id=1).all()
```

**关联查询** join outerjoin innerjoin

```python
session.query(User, Address).filter(User.id == Address.user_id).all()
session.query(User).join(User.addresses).all()
session.query(User).outerjoin(User.addresses).all()
```

**聚合查询** func.count func.sum group_by label

```python
session.query(User.name, func.count('*').label("user_count")).group_by(User.name).all()
session.query(User.name, func.sum(User.id).label("user_id_sum")).group_by(User.name).all()
```

**子查询** subquery()

```python
stmt = session.query(Address.user_id, func.count('*').label("address_count")).group_by(Address.user_id).subquery()
print(session.query(User, stmt.c.address_count).outerjoin((stmt, User.id == stmt.c.user_id)).order_by(User.id).all())
```

```python
限制返回字段查询
person = session.query(Person.name, Person.created_at,Person.updated_at).filter_by(name="zhongwei").order_by(Person.created_at).first()
```

!!!! 更新-update

!!!! 增加-add

count User records, without
using a subquery.
session.query(func.count(User.id))

return count of user "id" grouped
by "name"
session.query(func.count(User.id)).\
 group_by(User.name)

from sqlalchemy import distinct
count distinct "name" values
session.query(func.count(distinct(User.name)))

&& 03 模块说明

$$$ 查询限制条数

共有如下几种

**one()**
如果只能查询到一个结果，返回它，否则抛出异常。
没有结果时抛 sqlalchemy.orm.exc.NoResultFound，有超过一个结果时抛 sqlalchemy.orm.exc.MultipleResultsFound。

**all()**
查询所有结果。返回列表，无结果返回空列表。大数据时全部加载内存中 ，需要限制或分页。

**first()**
返回查询到的第一个结果，如果没有查询到结果，返回 None。

**.scalar() one_or_none()**
和.one_or_none()的效果一样。
如果查询到很多结果，抛出 sqlalchemy.orm.exc.MultipleResultsFound 异常。
如果只有一个结果，返回它，没有结果返回 None。
.one_or_none()比起.one()来，区别只是查询不到任何结果时不再抛出异常而是返回 None。

**.get()**
这是个比较特殊的方法。它用于根据主键来返回查询结果，因此它有个参数就是要查询的对象的主键。
如果没有该主键的结果返回 None，否则返回这个结果。

&& SqlAlchemy 官方文档-ORM 框架

$$$ 文档说明

[SqlAlchemy 官方文档-ORM 框架 版本 1.2.12](https://docs.sqlalchemy.org/en/latest/orm/index.html)

$$$ 关系对象教程

!!!! 检查版本

查看 sqlalchemy 版本

```python
In [7]: print(sqlalchemy.__version__)
1.2.10
```

!!!! 数据库连接

```python
In [3]: from sqlalchemy import create_engine
&& 连接到 Sqlite
In [4]: engine = create_engine('sqlite:///:memory:', echo=True)
&& echo 是否生成日志。True 生成所有Sql日志，False 不生成
&& 连接到 其他数据库
engine = create_engine('postgresql://scott:tiger@localhost:5432/mydatabase')
```

![create_engine视图](https://docs.sqlalchemy.org/en/latest/_images/sqla_engine_arch.png)

!!!! 声明映射

```python
>>> from sqlalchemy.ext.declarative import declarative_base
>>> Base = declarative_base()
```

使用 ORM 时，配置过程首先描述我们将要处理的数据库表，然后定义我们自己的类，这些类将映射到这些表。在现代 SQLAlchemy 中，这两个任务通常使用称为 Declarative 的系统一起执行，这允许我们创建包含指令的类，以描述它们将映射到的实际数据库表。

使用 Declarative 系统映射的类是根据基类定义的，该基类维护相对于该基类的类和表的目录 - 这称为声明性基类。我们的应用程序通常在一个常用的模块中只有一个这个基础的实例。我们使用 declarative_base() 函数创建基类，如下所示：

```python
>>> from sqlalchemy.ext.declarative import declarative_base

>>> Base = declarative_base()
```

现在我们有了一个“基础”，我们可以根据它定义任意数量的映射类。我们将从一个名为的表开始 users，它将使用我们的应用程序为最终用户存储记录。
调用的新类 User 将是我们映射此表的类。在类中，我们定义了有关我们将要映射的表的详细信息，主要是表名，以及列的名称和数据类型：

```python
>>> from sqlalchemy import Column, Integer, String
>>> class User(Base):
...     __tablename__ = 'users'
...
...     id = Column(Integer, primary_key=True)
...     name = Column(String)
...     fullname = Column(String)
...     password = Column(String)
...
...     def __repr__(self):
...        return "<User(name='%s', fullname='%s', password='%s')>" % (
...                             self.name, self.fullname, self.password)
```

定义一个`__repr__()`方法，是可选的，以便我们的示例显示格式良好的 User 对象。

使用 Declarative 的类至少需要一个**tablename**属性，并且至少有一个 Column 属于主键[1]的一部分。SQLAlchemy 从不对类引用的表做任何假设，包括它没有名称，数据类型或约束的内置约定。但这并不意味着需要样板; 相反，我们鼓励您使用辅助函数和 mixin 类创建自己的自动约定，这在 Mixin 和 Custom Base Classes 中有详细描述。

构造我们的类时，Declarative 将所有 Column 对象替换为称为描述符的特殊 Python 访问器;
这是一个称为仪器的过程。“instrumented”映射类将为我们提供在 SQL 上下文中引用表的方法，以及从数据库中持久保存和加载列的值。

除了映射过程对我们的类所做的之外，该类仍然主要是一个普通的 Python 类，我们可以定义我们的应用程序所需的任意数量的普通属性和方法。

!!!! 创建架构

User 通过声明系统构建我们的类，我们定义了有关表的信息，称为表元数据。SQLAlchemy 用于表示特定表的此信息的 Table 对象称为对象，这里 Declarative 为我们创建了一个对象。我们可以通过检查**table**属性来看到这个对象：

```python
>>> User.__table__
Table('users', MetaData(bind=None),
            Column('id', Integer(), table=<users>, primary_key=True, nullable=False),
            Column('name', String(), table=<users>),
            Column('fullname', String(), table=<users>),
            Column('password', String(), table=<users>), schema=None)
```

古典映射

虽然强烈建议使用 Declarative 系统，但不需要使用 SQLAlchemy 的 ORM。在 Declarative 之外，任何普通的 Python 类都可以直接映射到 Table 使用该 mapper()函数的任何类; 这种不太常见的用法在 Classical Mappings 中有所描述。

当我们声明我们的类时，Declarative 使用 Python 元类，以便在类声明完成后执行其他活动; 在此阶段，它 Table 根据我们的规范创建了一个对象，并通过构造一个 Mapper 对象将其与类相关联。这个对象是我们通常不需要直接处理的幕后对象（尽管它可以在我们需要时提供有关我们的映射的大量信息）。

该 Table 对象是一个更大的集合的成员，称为 MetaData。使用 Declarative 时，可以使用.metadata 声明性基类的属性来使用此对象。

这 MetaData 是一个注册表，包括向数据库发出一组有限的模式生成命令的功能。由于我们的 SQLite 数据库实际上没有 users 表，我们可以使用 MetaData 为所有尚不存在的表向数据库发出 CREATE TABLE 语句。下面，我们调用该 MetaData.create_all()方法，将我们 Engine 作为数据库连接源传递。我们将看到首先发出特殊命令以检查 users 表的存在，然后是实际的语句：CREATE TABLE

```python
>>> Base.metadata.create_all(engine)
SELECT ...
PRAGMA table_info("users")
()
CREATE TABLE users (
    id INTEGER NOT NULL, name VARCHAR,
    fullname VARCHAR,
    password VARCHAR,
    PRIMARY KEY (id)
)
()
COMMIT
```

**最小表格描述与完整描述**

熟悉 CREATE TABLE 语法的用户可能会注意到 VARCHAR 列的生成没有长度; 在 SQLite 和 PostgreSQL 上，这是一种有效的数据类型，但在其他情况下，它是不允许的。因此，如果在其中一个数据库上运行本教程，并且您希望使用 SQLAlchemy 发出 CREATE TABLE，则可以向该 String 类型提供“length” ，如下所示：

Column(String(50))
在长度字段 String，以及关于可用类似精度/规模字段 Integer，Numeric 等不会被其他的 SQLAlchemy 创建表时比引用。

此外，Firebird 和 Oracle 需要序列来生成新的主键标识符，而 SQLAlchemy 不会在未经指示的情况下生成或假设这些标识符。为此，您使用 Sequence 构造：

```python
from sqlalchemy import Sequence
Column(Integer, Sequence('user_id_seq'), primary_key=True)
Table因此，通过我们的声明性映射生成的完整，万无一失的因素是：

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                                self.name, self.fullname, self.password)
```

我们分别包含这个更详细的表定义，以突出主要针对 Python 内使用的最小构造与将用于在具有更严格要求的特定后端集上发出 CREATE TABLE 语句之间的区别。

!!!! 创建映射类的实例

完成映射后，现在让我们创建并检查一个 User 对象：

```python
>>> ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
>>> ed_user.name
'ed'
>>> ed_user.password
'edspassword'
>>> str(ed_user.id)
'None'
```

该**init**()方法

我们的 User 类（使用 Declarative 系统定义）提供了一个构造函数（例如**init**()方法），它自动接受与我们映射的列匹配的关键字名称。我们可以自由地**init**()在我们的类上定义我们喜欢的任何显式方法，它将覆盖 Declarative 提供的默认方法。

尽管我们没有在构造函数中指定它，但是当我们访问它时，该 id 属性仍会产生一个值 None（而不是 Python 通常的提升 AttributeError 未定义属性的行为）。SQLAlchemy 的检测通常在首次访问时为列映射属性生成此默认值。对于我们实际分配了值的那些属性，检测系统正在跟踪这些分配，以便在最终的 INSERT 语句中使用以发送到数据库。

!!!! 创建会话

我们现在准备开始与数据库交谈了。ORM 对数据库的“处理”是 Session。当我们第一次设置应用程序时，在与 create_engine() 语句相同的级别上，我们定义一个 Session 类，它将作为新 Session 对象的工厂：

```python
>>> from sqlalchemy.orm import sessionmaker
>>> Session = sessionmaker(bind=engine)
如果您的应用程序尚未 Engine定义模块级对象，请将其设置为：

>>> Session = sessionmaker()
稍后，当您使用创建引擎时create_engine()，将其连接到Session使用 configure()：

>>> Session.configure(bind=engine)  && once engine is available
会话生命周期模式
```

何时制作 a 的问题在 Session 很大程度上取决于正在构建的应用程序类型。请记住，Session 它只是对象的工作空间，是特定数据库连接的本地工作空间 - 如果您将应用程序线程视为晚宴 Session 上的访客，则是客人的盘子，它所拥有的对象是食物（和数据库......厨房？）！有关此主题的更多信息，请参阅何时构建会话，何时提交会话以及何时关闭会话？。

这个定制 Session 类将创建 Session 绑定到我们数据库的新对象。调用时也可以定义其他事务特征 sessionmaker; 这些将在后面的章节中描述。然后，只要您需要与数据库进行对话，就可以实例化 Session：

> > > session = Session()
> > > 以上 Session 内容与我们的 SQLite 相关联 Engine，但尚未打开任何连接。当它第一次使用时，它从由 Engine 它维护的连接池中检索连接 ，并保持它，直到我们提交所有更改和/或关闭会话对象。

!!!! 添加和更新对象

为了坚持我们的 User 目标，我们 add()对我们 Session：

```python
>>> ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
>>> session.add(ed_user)
```

此时，我们说该实例正在等待 ; 尚未发布任何 SQL，并且该对象尚未由数据库中的行表示。该 Session 会发出 SQL 坚持，只要需要，使用被称为一个过程冲洗。如果我们查询数据库，则首先刷新所有待处理信息，然后立即发出查询。Ed JonesEd Jones

例如，下面我们创建一个 Query 加载实例的新对象 User。我们“过滤” name 属性 ed，并表示我们只想要完整行列表中的第一个结果。User 返回一个实例，它等同于我们添加的实例：

SQL>>> our_user = session.query(User).filter_by(name='ed').first()

> > > our_user
> > > <User(name='ed', fullname='Ed Jones', password='edspassword')>
> > > 实际上，Session 已经确定返回的行与在其内部对象映射中已经表示的行相同，因此我们实际上得到了与我们刚刚添加的实例相同的实例：

> > > ed_user is our_user
> > > True
> > > 这里工作的 ORM 概念称为身份映射， 并确保在一个特定行上的所有操作都在 Session 同一组数据上运行。一旦具有特定主键的对象存在于其中 Session，则所有 SQL 查询 Session 将始终返回该特定主键的相同 Python 对象; 如果尝试在会话中放置具有相同主键的第二个已经持久化的对象，它也会引发错误。

我们可以 User 一次添加更多对象 add_all()：

> > > session.add_all([
> > > ... User(name='wendy', fullname='Wendy Williams', password='foobar'),
> > > ... User(name='mary', fullname='Mary Contrary', password='xxg527'),
> > > ... User(name='fred', fullname='Fred Flinstone', password='blah')])
> > > 此外，我们已经确定 Ed 的密码不太安全，所以我们改变它：

> > > ed_user.password = 'f8s7ccs'
> > > 该 Session 被关注。例如，它知道已被修改：Ed Jones

> > > session.dirty
> > > IdentitySet([<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>])
> > > 并且有三个新 User 对象待定：

> > > session.new  
> > > IdentitySet([<User(name='wendy', fullname='Wendy Williams', password='foobar')>,
> > > <User(name='mary', fullname='Mary Contrary', password='xxg527')>,
> > > <User(name='fred', fullname='Fred Flinstone', password='blah')>])
> > > 我们告诉我们 Session，我们想要对数据库发出所有剩余的更改并提交事务，该事务一直在进行中。我们通过这样做 commit()。在 Session 发出 UPDATE 关于“ED”的密码更改，以及声明 INSERT 三个新语句 User 我们添加的对象：

SQL>>> session.commit()
commit()刷新对数据库的剩余更改，并提交事务。会话引用的连接资源现在返回到连接池。此会话的后续操作将在新事务中进行，该事务将在首次需要时再次重新获取连接资源。

如果我们看看之前的 Ed id 属性 None，它现在有一个值：

SQL>>> ed_user.id
1
在 Session 数据库中插入新行后，所有新生成的标识符和数据库生成的默认值都可以立即在实例上使用，也可以通过首次访问加载来实现。在这种情况下，整个行在访问时被重新加载，因为在我们发布之后开始了新的事务 commit()。默认情况下，SQLAlchemy 会在第一次在新事务中访问时刷新先前事务中的数据，以便最新状态可用。重新加载的级别是可配置的，如使用会话中所述。

会话对象状态

当我们的 User 对象从外部移动 Session 到 Session 没有主键的内部，实际被插入时，它在四个可用的“对象状态”中的三个之间移动 - 瞬态，待定和持久。了解这些状态及其含义总是一个好主意 - 请务必阅读 Quickie Intro to Object States 以获得快速概述。

!!!! 回滚

由于 Session 交易中的工作，我们也可以回滚所做的更改。让我们做两个我们将要改变的变化; ed_user 的用户名设置为 Edwardo：

> > > ed_user.name = 'Edwardo'
> > > 我们将添加另一个错误的用户，fake_user：

> > > fake_user = User(name='fakeuser', fullname='Invalid', password='12345')
> > > session.add(fake_user)
> > > 查询会话，我们可以看到它们被刷新到当前事务中：

SQL>>> session.query(User).filter(User.name.in\_(['Edwardo', 'fakeuser'])).all()
[<User(name='Edwardo', fullname='Ed Jones', password='f8s7ccs')>, <User(name='fakeuser', fullname='Invalid', password='12345')>]
回滚过去，我们可以看到这个 ed_user 名字又回来了 ed，并且 fake_user 已经被踢出了会议：

SQL>>> session.rollback()

SQL>>> ed_user.name
u'ed'

> > > fake_user in session
> > > False
> > > 发出 SELECT 说明了对数据库所做的更改：

SQL>>> session.query(User).filter(User.name.in\_(['ed', 'fakeuser'])).all()
[<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>]

!!!! Querying

甲 Query 对象使用所创建的 query()上方法 Session。此函数采用可变数量的参数，可以是类和类检测描述符的任意组合。下面，我们指出 Query 哪个加载 User 实例。在迭代上下文中计算时，将 User 返回存在的对象列表：

SQL>>> for instance in session.query(User).order_by(User.id):
... print(instance.name, instance.fullname)
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flinstone
该 Query 还接受 ORM，仪表描述作为参数。每当多个类实体或基于列的实体表示为函数的参数时 query()，返回结果表示为元组：

SQL>>> for name, fullname in session.query(User.name, User.fullname):
... print(name, fullname)
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flinstone
返回的元组 Query 被命名为 元组，由 KeyedTuple 类提供，并且可以像普通的 Python 对象一样对待。名称与属性的属性名称以及类的类名称相同：

SQL>>> for row in session.query(User, User.name).all():
... print(row.User, row.name)
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')> ed
<User(name='wendy', fullname='Wendy Williams', password='foobar')> wendy
<User(name='mary', fullname='Mary Contrary', password='xxg527')> mary
<User(name='fred', fullname='Fred Flinstone', password='blah')> fred
您可以使用 label()构造控制单个列表达式的名称，该 构造可从任何 ColumnElement 派生对象获得，以及映射到其中的任何类属性（例如 User.name）：

SQL>>> for row in session.query(User.name.label('name_label')).all():
... print(row.name_label)
ed
wendy
mary
fred
给予完整实体的名称，例如 User，假设调用中存在多个实体 query()，可以使用 aliased()以下方法控制 ：

> > > from sqlalchemy.orm import aliased
> > > user_alias = aliased(User, name='user_alias')

SQL>>> for row in session.query(user_alias, user_alias.name).all():
... print(row.user_alias)
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>
<User(name='wendy', fullname='Wendy Williams', password='foobar')>
<User(name='mary', fullname='Mary Contrary', password='xxg527')>
<User(name='fred', fullname='Fred Flinstone', password='blah')>
基本操作 Query 包括发出 LIMIT 和 OFFSET，最方便的是使用 Python 数组切片，通常与 ORDER BY 结合使用：

SQL>>> for u in session.query(User).order_by(User.id)[1:3]:
... print(u)
<User(name='wendy', fullname='Wendy Williams', password='foobar')>
<User(name='mary', fullname='Mary Contrary', password='xxg527')>
和过滤结果，使用 filter_by()，使用关键字参数完成：

SQL>>> for name, in session.query(User.name).\
... filter_by(fullname='Ed Jones'):
... print(name)
ed
...或者 filter()，它使用更灵活的 SQL 表达式语言结构。这些允许您使用常规 Python 运算符和映射类的类级属性：

SQL>>> for name, in session.query(User.name).\
... filter(User.fullname=='Ed Jones'):
... print(name)
ed
该 Query 对象是完全生成的，这意味着大多数方法调用返回一个新 Query 对象，可以在其上添加进一步的标准。例如，要查询名为“ed”且名称为“Ed Jones”的用户，可以调用 filter()两次，使用 AND 以下命令连接条件 ：

SQL>>> for user in session.query(User).\
... filter(User.name=='ed').\
... filter(User.fullname=='Ed Jones'):
... print(user)
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>

@@@@@ 通用过滤器运算符

以下是一些最常用的运算符的概述 filter()：

- 等于

```python
query.filter(User.name == 'ed')
```

- 不等于

```python
query.filter(User.name != 'ed')
```

- 模糊匹配 like **区分大小写**

```python
query.filter(User.name.like('%ed%'))
ColumnOperators.like()呈现LIKE运算符，对某些后端不区分大小写，对其他后端区分大小写。对于保证不区分大小写的比较，请使用 ColumnOperators.ilike()。
```

- 模糊匹配 ilike **不区分大小写**

```python
query.filter(User.name.ilike('%ed%'))
注意

大多数后端不直接支持ILIKE。对于那些，ColumnOperators.ilike()运算符呈现一个表达式，将LIKE与应用于每个操作数的LOWER SQL函数相结合。
```

- 在什么之内 in

```python
query.filter(User.name.in_(['ed', 'wendy', 'jack']))

&&works with query objects too:
query.filter(User.name.in_(
    session.query(User.name).filter(User.name.like('%ed%'))
))
```

- 不在什么之内 not in

```python
query.filter(~User.name.in_(['ed', 'wendy', 'jack']))
```

- 为空 is null

```python
query.filter(User.name == None)
&& alternatively, if pep8/linters are a concern
query.filter(User.name.is_(None))
```

- 非空 IS NOT NULL:

```python
query.filter(User.name != None)
&& alternatively, if pep8/linters are a concern
query.filter(User.name.isnot(None))
```

- 且 and

```python
&& use and_()
from sqlalchemy import and_
query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))
&& or send multiple expressions to .filter()
query.filter(User.name == 'ed', User.fullname == 'Ed Jones')
&& or chain multiple filter()/filter_by() calls
query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')
```

- 或 OR:

```python
from sqlalchemy import or_
query.filter(or_(User.name == 'ed', User.name == 'wendy'))
```

- 精准匹配 MATCH:

```python
query.filter(User.name.match('wendy'))
```

注意

match()使用特定于数据库 MATCH 或 CONTAINS 函数; 它的行为会因后端而异，并且在某些后端（例如 SQLite）上不可用。

@@@@@ 返回列表和标量

有许多方法可以 Query 立即发出 SQL 并返回包含已加载数据库结果的值。这是一个简短的旅游：

all() 返回一个列表：

```python
>>> query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
SQL>>> query.all()
[<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>,
      <User(name='fred', fullname='Fred Flinstone', password='blah')>]
first() 应用限制为1并将第一个结果作为标量返回：

SQL>>> query.first()
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>
one()完全提取所有行，如果结果中不存在一个对象标识或复合行，则会引发错误。找到多行：

>>> user = query.one()
Traceback (most recent call last):
...
MultipleResultsFound: Multiple rows were found for one()
没有找到行：

>>> user = query.filter(User.id == 99).one()
Traceback (most recent call last):
...
NoResultFound: No row was found for one()
该one()方法非常适用于希望处理“找不到物品”而不是“找到多件物品”的系统; 例如RESTful Web服务，可能希望在找不到结果时引发“未找到404”，但在找到多个结果时引发应用程序错误。

one_or_none()就像one()，除非没有找到结果，它不会引起错误; 它只是回来了None。像 one()，但是，它如果有多个结果发现引发错误。

scalar()调用该one()方法，并在成功时返回该行的第一列：

>>> query = session.query(User.id).filter(User.name == 'ed').\
...    order_by(User.id)
SQL>>> query.scalar()
1
```

@@@@@ 使用文本

Query 通过指定它们对 text()构造的使用，可以灵活地使用文字字符串 ，这是大多数适用方法所接受的。例如， filter()和 order_by()：

```python
>>> from sqlalchemy import text
SQL>>> for user in session.query(User).\
...             filter(text("id<224")).\
...             order_by(text("id")).all():
...     print(user.name)
ed
wendy
mary
fred
可以使用冒号使用基于字符串的SQL指定绑定参数。要指定值，请使用以下params() 方法：

SQL>>> session.query(User).filter(text("id<:value and name=:name")).\
...     params(value=224, name='fred').order_by(User.id).one()
<User(name='fred', fullname='Fred Flinstone', password='blah')>
要使用完全基于字符串的语句，text()可以将表示完整语句的构造传递给 from_statement()。如果没有其他说明符，字符串SQL中的列将根据名称与模型列匹配，例如下面我们只使用星号表示加载所有列：

SQL>>> session.query(User).from_statement(
...                     text("SELECT * FROM users where name=:name")).\
...                     params(name='ed').all()
[<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>]
匹配名称上的列适用于简单的情况，但在处理包含重复列名的复杂语句或使用不易与特定名称匹配的匿名ORM构造时可能会变得难以处理。此外，在处理结果行时，我们可能会发现在映射列中存在键入行为。对于这些情况，text()构造允许我们在位置上将其文本SQL链接到Core或ORM映射的列表达式; 我们可以通过将列表达式作为位置参数传递给TextClause.columns()方法来实现这一点 ：

>>> stmt = text("SELECT name, id, fullname, password "
...             "FROM users where name=:name")
>>> stmt = stmt.columns(User.name, User.id, User.fullname, User.password)
SQL>>> session.query(User).from_statement(stmt).params(name='ed').all()
[<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>]
版本1.1中的新增功能：该TextClause.columns()方法现在接受列表达式，这些列表达式将与纯文本SQL结果集进行位置匹配，从而无需在SQL语句中匹配甚至是唯一的列名。

从text()构造中进行选择时，Query 仍然可以指定要返回的列和实体; 而不是 query(User)我们也可以单独要求列，如在任何其他情况下：

>>> stmt = text("SELECT name, id FROM users where name=:name")
>>> stmt = stmt.columns(User.name, User.id)
SQL>>> session.query(User.id, User.name).\
...          from_statement(stmt).params(name='ed').all()
[(1, u'ed')]
也可以看看

使用Textual SQL -text()从仅核心查询的角度解释构造。
```

@@@@@ Counting 计数

Query 包括一种方便的计数方法 count()：

```python
SQL>>> session.query(User).filter(User.name.like('%ed')).count()
2
指望 count()

Query.count()曾经是一个非常复杂的方法，当它试图猜测现有查询周围是否需要子查询时，在某些奇特的情况下它不会做正确的事情。现在它每次都使用一个简单的子查询，它只有两行长并且总是返回正确的答案。使用func.count()如果一个特定的语句绝对不能容忍的子查询存在。

该count()方法用于确定SQL语句将返回多少行。查看上面生成的SQL，SQLAlchemy总是将我们查询的任何内容放入子查询中，然后从中计算行数。在某些情况下，这可以简化为更简单，但SQLAlchemy的现代版本不会尝试猜测何时合适，因为可以使用更明确的方法发出确切的SQL。SELECT count(*) FROM table

对于需要具体指出“要计数的东西”的情况，我们可以直接使用构造中func.count()可用 的表达式指定“计数”函数func。下面我们用它来返回每个不同用户名的计数：

>>> from sqlalchemy import func
SQL>>> session.query(func.count(User.name), User.name).group_by(User.name).all()
[(1, u'ed'), (1, u'fred'), (1, u'mary'), (1, u'wendy')]
为了实现我们的简单，我们可以将其应用为：SELECT count(*) FROM table

SQL>>> session.query(func.count('*')).select_from(User).scalar()
4
select_from()如果我们User直接用主键表示计数，则可以删除用法：

SQL>>> session.query(func.count(User.id)).scalar()
4
```

!!!! 建立关系

让我们考虑如何 User 映射和查询与之相关的第二个表。我们系统中的用户可以存储与其用户名关联的任意数量的电子邮件地址。这意味着从 users 存储电子邮件地址的新表到基本的一对多关联，我们将调用它 addresses。使用声明，我们将此表及其映射类定义为 Address：

```python
>>> from sqlalchemy import ForeignKey
>>> from sqlalchemy.orm import relationship

>>> class Address(Base):
...     __tablename__ = 'addresses'
...     id = Column(Integer, primary_key=True)
...     email_address = Column(String, nullable=False)
...     user_id = Column(Integer, ForeignKey('users.id'))
...
...     user = relationship("User", back_populates="addresses")
...
...     def __repr__(self):
...         return "<Address(email_address='%s')>" % self.email_address

>>> User.addresses = relationship(
...     "Address", order_by=Address.id, back_populates="user")
上面的类介绍了ForeignKey构造，它是一个应用于的指令，Column它指示此列中的值应该被约束为指定的远程列中存在的值。这是关系数据库的核心功能，并且是“粘合剂”，它将未连接的表集合转换为具有丰富的重叠关系。的ForeignKey是，在以上的值表示addresses.user_id列应被约束在这些值users.id列中，即它的主键。

第二个指令，称为relationship()ORM ，使用该属性告诉ORM Address类本身应该链接到User类Address.user。 relationship()使用两个表之间的外键关系来确定此链接的性质，确定Address.user将是多对一。另一个relationship()指令放在 User属性下的映射类中User.addresses。在两个 relationship()指令中，relationship.back_populates分配参数 以引用补充属性名称; 通过这样做，每个人都relationship() 可以做出与反向表达的相同关系的智能决策; 一方面，Address.user指的是一个User实例，另一方面User.addresses指的是一个列表 Address 实例。

注意

该relationship.back_populates参数是一个非常常见的SQLAlchemy功能的较新版本 relationship.backref。该relationship.backref 参数还没有到哪里去了，永远保持可用！这relationship.back_populates是一回事，除了更冗长，更容易操纵。有关整个主题的概述，请参阅使用Backref链接关系部分。

多对一关系的反面总是一对多。基本关系模式的完整可用relationship()配置目录。

两个互补关系Address.user并且User.addresses 被称为一个双向关系，并且是SQLAlchemy的ORM的一个关键特征。Linking Relationships with Backref部分详细 讨论了“backref”功能。

relationship()假设声明系统正在使用中，可以使用字符串指定远程类所关注的参数。一旦所有映射完成，这些字符串将被计算为Python表达式，以便生成实际参数，在上面的例子中是User类。在此评估期间允许使用的名称包括根据声明的基础创建的所有类的名称。

有关relationship()参数样式的更多详细信息，请参阅docstring 。

你知道吗 ？

大多数（尽管不是全部）关系数据库中的FOREIGN KEY约束只能链接到主键列或具有UNIQUE约束的列。
引用多列主键的FOREIGN KEY约束，本身有多列，称为“复合外键”。它还可以引用这些列的子集。
FOREIGN KEY列可以自动更新，以响应引用的列或行的更改。这称为CASCADE 引用操作，是关系数据库的内置函数。
FOREIGN KEY可以参考自己的表。这被称为“自引用”外键。
在外键- 维基百科上阅读更多关于外键的信息。
我们需要addresses在数据库中创建表，因此我们将从元数据中发出另一个CREATE，它将跳过已经创建的表：

SQL>>> Base.metadata.create_all(engine)
```

!!!! 使用相关对象

现在，当我们创建一个 User 空白 addresses 集合时，将会出现。此处可以使用各种集合类型（例如集和字典）（有关详细信息，请参阅自定义集合访问），但默认情况下，集合是 Python 列表。

```python
>>> jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
>>> jack.addresses
[]
我们可以自由地在Address对象上添加User对象。在这种情况下，我们只是直接指定一个完整列表：

>>> jack.addresses = [
...                 Address(email_address='jack@google.com'),
...                 Address(email_address='j25@yahoo.com')]
使用双向关系时，在一个方向上添加的元素会自动在另一个方向上可见。此行为基于属性on-change事件发生，并在Python中进行评估，而不使用任何SQL：

>>> jack.addresses[1]
<Address(email_address='j25@yahoo.com')>

>>> jack.addresses[1].user
<User(name='jack', fullname='Jack Bean', password='gjffdd')>
让我们添加并提交到数据库。以及相应 集合中的两个成员都使用称为级联的过程一次添加到会话中：Jack BeanjackAddressaddresses

>>> session.add(jack)
SQL>>> session.commit()
查询杰克，我们得到杰克回来。尚未为Jack的地址发布SQL：

SQL>>> jack = session.query(User).\
... filter_by(name='jack').one()
>>> jack
<User(name='jack', fullname='Jack Bean', password='gjffdd')>
我们来看看这个addresses系列吧。观看SQL：

SQL>>> jack.addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]
当我们访问addresses集合时，突然发出了SQL。这是延迟加载关系的一个例子。该addresses集合现在已加载，其行为就像普通列表一样。我们将介绍一些优化加载这个集合的方法。
```

!!!! 用连接查询

现在我们有两个表，我们可以显示更多的功能 Query，特别是如何创建同时处理这两个表的查询。SQL JOIN 上的 Wikipedia 页面提供了对连接技术的一个很好的介绍，其中几个我们将在这里说明。

要在 User 和之间构造一个简单的隐式连接 Address，我们可以使用 Query.filter()它们将它们的相关列等同起来。下面我们使用这个方法一次加载 User 和 Address 实体：

```python
SQL>>> for u, a in session.query(User, Address).\
...                     filter(User.id==Address.user_id).\
...                     filter(Address.email_address=='jack@google.com').\
...                     all():
...     print(u)
...     print(a)
<User(name='jack', fullname='Jack Bean', password='gjffdd')>
<Address(email_address='jack@google.com')>
另一方面，实际的SQL JOIN语法最容易使用以下Query.join()方法实现：

SQL>>> session.query(User).join(Address).\
...         filter(Address.email_address=='jack@google.com').\
...         all()
[<User(name='jack', fullname='Jack Bean', password='gjffdd')>]
Query.join()知道如何加入User ，Address因为它们之间只有一个外键。如果没有外键或多个外键，Query.join() 则在使用以下表单之一时效果更好：

query.join(Address, User.id==Address.user_id)    && explicit condition
query.join(User.addresses)                       && specify relationship from left to right
query.join(Address, User.addresses)              && same, with explicit target
query.join('addresses')                          && same, using a string
正如您所期望的那样，使用以下outerjoin()函数将相同的想法用于“外部”连接 ：

query.outerjoin(User.addresses)   && LEFT OUTER JOIN
参考文档join()包含此方法接受的调用样式的详细信息和示例; join() 对于任何SQL-fluent应用程序而言，它是使用中心的重要方法。

Query如果有多个实体，可以选择什么？

当省略ON子句或ON子句是纯SQL表达式时，该Query.join()方法通常从实体列表中最左边的项加入。要控制JOIN列表中的第一个实体，请使用以下Query.select_from()方法：

query = session.query(User, Address).select_from(Address).join(User)
@@@@@ 使用别名
在跨多个表进行查询时，如果需要多次引用同一个表，则SQL通常要求使用其他名称对该表进行别名，以便可以将该表与该表的其他实例区分开来。Query最明确使用aliased构造的支持。下面我们Address 两次加入实体，找到同时拥有两个不同电子邮件地址的用户：

>>> from sqlalchemy.orm import aliased
>>> adalias1 = aliased(Address)
>>> adalias2 = aliased(Address)
SQL>>> for username, email1, email2 in \
...     session.query(User.name, adalias1.email_address, adalias2.email_address).\
...     join(adalias1, User.addresses).\
...     join(adalias2, User.addresses).\
...     filter(adalias1.email_address=='jack@google.com').\
...     filter(adalias2.email_address=='j25@yahoo.com'):
...     print(username, email1, email2)
jack jack@google.com j25@yahoo.com
```

@@@@@ 使用子查询

的 Query 是适合于产生其可以被用作子查询语句。
假设我们想要加载 User 对象以及 Address 每个用户拥有多少条记录的计数。
生成这样的 SQL 的最佳方法是获取按用户 ID 分组的地址计数，并将 JOIN 连接到父级。
在这种情况下，我们使用 LEFT OUTER JOIN，以便为没有任何地址的用户返回行，例如：

```python
SELECT users.*, adr_count.address_count FROM users LEFT OUTER JOIN
    (SELECT user_id, count(*) AS address_count
        FROM addresses GROUP BY user_id) AS adr_count
    ON users.id=adr_count.user_id
使用Query，我们从内到外构建一个这样的语句。的statement存取器返回一个表示由特定生成的声明SQL表达式 Query-这是一个实例select() 构建体，其中描述了SQL表达式语言教程：

>>> from sqlalchemy.sql import func
>>> stmt = session.query(Address.user_id, func.count('*').\
...         label('address_count')).\
...         group_by(Address.user_id).subquery()
所述func关键字生成SQL函数，以及subquery()关于方法 Query产生表示嵌入的别名内SELECT语句中的SQL表达构建体（它实际上是简写query.statement.alias()）。

一旦我们得到了语句，它就像一个Table构造，比如我们在users本教程开始时创建的 构造 。语句中的列可通过以下属性访问c：

SQL>>> for u, count in session.query(User, stmt.c.address_count).\
...     outerjoin(stmt, User.id==stmt.c.user_id).order_by(User.id):
...     print(u, count)
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')> None
<User(name='wendy', fullname='Wendy Williams', password='foobar')> None
<User(name='mary', fullname='Mary Contrary', password='xxg527')> None
<User(name='fred', fullname='Fred Flinstone', password='blah')> None
<User(name='jack', fullname='Jack Bean', password='gjffdd')> 2
@@@@@ 从子查询中选择实体
上面，我们刚刚选择了一个包含子查询列的结果。如果我们希望子查询映射到实体怎么办？为此，我们使用aliased() 将映射类的“别名”与子查询相关联：

SQL>>> stmt = session.query(Address).\
...                 filter(Address.email_address != 'j25@yahoo.com').\
...                 subquery()
>>> adalias = aliased(Address, stmt)
>>> for user, address in session.query(User, adalias).\
...         join(adalias, User.addresses):
...     print(user)
...     print(address)
<User(name='jack', fullname='Jack Bean', password='gjffdd')>
<Address(email_address='jack@google.com')>
```

@@@@@ 使用 Exists 存在

SQL 中的 EXISTS 关键字是一个布尔运算符，如果给定的表达式包含任何行，则返回 True。它可以在许多场景中用于代替连接，也可用于定位在相关表中没有相应行的行。

有一个显式的 EXISTS 结构，如下所示：

```python
>>> from sqlalchemy.sql import exists
>>> stmt = exists().where(Address.user_id==User.id)
SQL>>> for name, in session.query(User.name).filter(stmt):
...     print(name)
jack
该Query功能几家运营商，这使得使用情况自动存在。上面，声明可以User.addresses使用any()以下关系表达 ：

SQL>>> for name, in session.query(User.name).\
...         filter(User.addresses.any()):
...     print(name)
jack
any() 采用标准，限制匹配的行：

SQL>>> for name, in session.query(User.name).\
...     filter(User.addresses.any(Address.email_address.like('%google%'))):
...     print(name)
jack
has()与any()多对一关系是同一个运算符 （请注意~这里的运算符，这意味着“NOT”）：

SQL>>> session.query(Address).\
...         filter(~Address.user.has(User.name=='jack')).all()
[]
```

@@@@@ 公共关系运算符

以下是构建关系的所有运算符 - 每个运算符都链接到其 API 文档，其中包含有关使用和行为的完整详细信息：

**eq**() （多对一“等于”比较）：

query.filter(Address.user == someuser)
**ne**() （多对一“不等于”比较）：

query.filter(Address.user != someuser)
IS NULL（多对一比较，也使用**eq**()）：

query.filter(Address.user == None)
contains() （用于一对多收藏）：

query.filter(User.addresses.contains(someaddress))
any() （用于收藏）：

```python
query.filter(User.addresses.any(Address.email_address == 'bar'))

&& also takes keyword arguments:
query.filter(User.addresses.any(email_address='bar'))
```

- has() （用于标量引用）：

```python
query.filter(Address.user.has(name='ed'))
Query.with_parent() （用于任何关系）：

session.query(Address).with_parent(someuser, 'addresses')
```

!!!! 渴望加载

回想一下，当我们访问 a 的集合并发出 SQL 时，我们说明了一个延迟加载操作。如果您想减少查询数量（在很多情况下显着），我们可以对查询操作应用急切加载。SQLAlchemy 提供三种类型的预先加载，其中两种是自动加载，第三种涉及自定义标准。所有这三个通常都是通过称为查询选项的函数调用的，这些函数通过该方法为我们希望如何加载各种属性提供了额外的指令。User.addressesUserQueryQuery.options()

@@@@@ 子查询加载

在这种情况下，我们想表明 User.addresses 应该急切加载。加载一组对象及其相关集合的一个很好的选择是 orm.subqueryload()选项，它会发出第二个 SELECT 语句，该语句完全加载与刚刚加载的结果相关联的集合。名称“子查询”源于这样一个事实，即直接通过它构造的 SELECT 语句 Query 被重新使用，作为子查询嵌入到相关表的 SELECT 中。这有点精心但很容易使用：

> > > from sqlalchemy.orm import subqueryload
> > > SQL>>> jack = session.query(User).\
> > > ... options(subqueryload(User.addresses)).\
> > > ... filter_by(name='jack').one()
> > > jack
> > > <User(name='jack', fullname='Jack Bean', password='gjffdd')>

> > > jack.addresses
> > > [<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]
> > > 注意

subqueryload()当与限制一起使用时 Query.first()，Query.limit()或者 Query.offset() 还应包括 Query.order_by()在一个独特的列上，以确保正确的结果。请参阅订购的重要性。

@@@@@ 加入加载

另一种自动急切加载功能更为人所知并被称为 orm.joinedload()。这种加载方式发出 JOIN，默认情况下为 LEFT OUTER JOIN，因此只需一步加载主对象以及相关对象或集合。我们 addresses 以这种方式说明加载相同的 集合 - 请注意，即使实际上正在填充 User.addresses 集合 jack，查询也会发出额外的连接，无论如何：

```python
>>> from sqlalchemy.orm import joinedload

SQL>>> jack = session.query(User).\
...                        options(joinedload(User.addresses)).\
...                        filter_by(name='jack').one()
>>> jack
<User(name='jack', fullname='Jack Bean', password='gjffdd')>

>>> jack.addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]
请注意，即使OUTER JOIN导致两行，我们仍然只有一个User返回实例。这是因为Query基于对象标识将“uniquing”策略应用于返回的实体。具体来说，可以应用联合的预先加载而不会影响查询结果。

虽然joinedload()已经存在了很长时间，但是subqueryload() 是一种新形式的渴望加载。 subqueryload()往往更适合加载相关集合，而joinedload()往往更适合多对一关系，因为只有一行加载了潜在客户和相关对象。

joinedload() 不是替代品 join()
```

创建的 joinedload()联接是匿名别名，因此不会影响查询结果。一个 Query.order_by() 或 Query.filter()电话无法引用这些别名表-所谓的“用户空间”连接被利用人工 Query.join()。其基本原理 joinedload()是仅应用于影响相关对象或集合作为优化细节的加载方式 - 可以添加或删除它，而不会影响实际结果。有关如何使用它的详细说明，请参阅“ 加入的渴望加载的禅 ”一节。

@@@@@ 明确加入+ Eagerload

第三种类型的热切加载是当我们显式构造 JOIN 以便定位主行时，并且还想将额外的表应用于主对象上的相关对象或集合。此功能是通过该 orm.contains_eager()函数提供的，最常用于在需要对同一对象进行过滤的查询上预加载多对一对象。下面我们说明加载 Address 一行以及相关 User 对象，过滤 User 命名的“jack”并使用 orm.contains_eager()“user”列应用于 Address.user 属性：

```python
>>> from sqlalchemy.orm import contains_eager
SQL>>> jacks_addresses = session.query(Address).\
...                             join(Address.user).\
...                             filter(User.name=='jack').\
...                             options(contains_eager(Address.user)).\
...                             all()
>>> jacks_addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]

>>> jacks_addresses[0].user
<User(name='jack', fullname='Jack Bean', password='gjffdd')>
有关预先加载的更多信息，包括默认情况下如何配置各种加载形式，请参阅关系加载技术一节。
```

!!!! Deleting

让我们尝试删除 jack，看看情况如何。我们将会话中的对象标记为已删除，然后我们将发出 count 查询以查看没有行保留：

```python
>>> session.delete(jack)
SQL>>> session.query(User).filter_by(name='jack').count()
0
到现在为止还挺好。杰克的Address物品怎么样？

SQL>>> session.query(Address).filter(
...     Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
...  ).count()
2
哦，他们还在那里！分析刷新SQL，我们可以看到user_id每个地址的 列都设置为NULL，但是没有删除行。SQLAlchemy并不认为删除级联，你必须告诉它这样做。
```

@@@@@ 配置 delete / delete-

我们将在关系上配置级联选项 User.addresses 以更改行为。虽然 SQLAlchemy 允许您在任何时间点向映射添加新属性和关系，但在这种情况下需要删除现有关系，因此我们需要完全拆除映射并重新开始 - 我们将关闭 Session：

```python
>>> session.close()
ROLLBACK
并使用新的declarative_base()：

>>> Base = declarative_base()
接下来我们将声明User该类，添加addresses包括级联配置的关系（我们也将构造函数保留在外）：

>>> class User(Base):
...     __tablename__ = 'users'
...
...     id = Column(Integer, primary_key=True)
...     name = Column(String)
...     fullname = Column(String)
...     password = Column(String)
...
...     addresses = relationship("Address", back_populates='user',
...                     cascade="all, delete, delete-orphan")
...
...     def __repr__(self):
...        return "<User(name='%s', fullname='%s', password='%s')>" % (
...                                self.name, self.fullname, self.password)
然后我们重新创建Address，注意到在这种情况下我们已经Address.user通过User类创建了关系：

>>> class Address(Base):
...     __tablename__ = 'addresses'
...     id = Column(Integer, primary_key=True)
...     email_address = Column(String, nullable=False)
...     user_id = Column(Integer, ForeignKey('users.id'))
...     user = relationship("User", back_populates="addresses")
...
...     def __repr__(self):
...         return "<Address(email_address='%s')>" % self.email_address
```

现在，当我们加载用户时 jack（下面使用 get()，按主键加载），从相应的 addresses 集合中删除地址将导致 Address 删除：

```python
&& load Jack by primary key
SQL>>> jack = session.query(User).get(5)

&& remove one Address (lazy load fires off)
SQL>>> del jack.addresses[1]

&& only one address remains
SQL>>> session.query(Address).filter(
...     Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
... ).count()
1
```

删除 Jack 将删除 Jack 以及 Address 与用户关联的其余内容：

```python
>>> session.delete(jack)

SQL>>> session.query(User).filter_by(name='jack').count()
0

SQL>>> session.query(Address).filter(
...    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
... ).count()
0
更多关于瀑布
```

有关级联配置的更多详细信息，请参见 Cascades。级联功能还可以平滑地与关系数据库的功能集成。有关详细信息，请参阅使用被动删除。ON DELETE CASCADE

!!!! 建立多对多的关系

我们在这里进入奖金回合，但是让我们展示一个多对多的关系。我们也会潜入其他一些功能，只是为了参观。我们将使我们的应用程序成为博客应用程序，用户可以在其中编写 BlogPost 包含 Keyword 与之关联的项目的项目。

对于普通的多对多，我们需要创建一个未映射的 Table 构造作为关联表。这看起来如下：

```python
>>> from sqlalchemy import Table, Text
>>> && association table
>>> post_keywords = Table('post_keywords', Base.metadata,
...     Column('post_id', ForeignKey('posts.id'), primary_key=True),
...     Column('keyword_id', ForeignKey('keywords.id'), primary_key=True)
... )
在上面，我们可以看到声明a Table直接与声明映射类有点不同。 Table是构造函数，因此每个单独的Column参数用逗号分隔。该 Column对象也明确地赋予其名称，而不是从指定的属性名称中获取。

接下来，我们定义BlogPost并Keyword使用互补 relationship()结构，每个引用post_keywords 表作为关联表：

>>> class BlogPost(Base):
...     __tablename__ = 'posts'
...
...     id = Column(Integer, primary_key=True)
...     user_id = Column(Integer, ForeignKey('users.id'))
...     headline = Column(String(255), nullable=False)
...     body = Column(Text)
...
...     && many to many BlogPost<->Keyword
...     keywords = relationship('Keyword',
...                             secondary=post_keywords,
...                             back_populates='posts')
...
...     def __init__(self, headline, body, author):
...         self.author = author
...         self.headline = headline
...         self.body = body
...
...     def __repr__(self):
...         return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)


>>> class Keyword(Base):
...     __tablename__ = 'keywords'
...
...     id = Column(Integer, primary_key=True)
...     keyword = Column(String(50), nullable=False, unique=True)
...     posts = relationship('BlogPost',
...                          secondary=post_keywords,
...                          back_populates='keywords')
...
...     def __init__(self, keyword):
...         self.keyword = keyword
注意
```

上面的类声明说明了显式**init**()方法。请记住，使用 Declarative 时，它是可选的！

以上，多对多关系是 BlogPost.keywords。多对多关系的定义特征是 secondary 关键字参数，它引用 Table 表示关联表的对象。该表仅包含引用关系两边的列; 如果它有任何其他列，例如它自己的主键，或其他表的外键，SQLAlchemy 需要一个不同的使用模式，称为“关联对象”，在关联对象中描述 。

我们也希望我们的 BlogPost 班级有一个 author 领域。我们将此添加为另一个双向关系，除了我们将遇到的一个问题是单个用户可能有很多博客帖子。当我们访问时 User.posts，我们希望能够进一步过滤结果，以免加载整个集合。为此，我们使用被 relationship()调用接受的设置 lazy='dynamic'，该设置 在属性上配置备用加载器策略：

```python
>>> BlogPost.author = relationship(User, back_populates="posts")
>>> User.posts = relationship(BlogPost, back_populates="author", lazy="dynamic")
创建新表：

SQL>>> Base.metadata.create_all(engine)
用法与我们一直在做的不同。让我们给Wendy一些博文：

SQL>>> wendy = session.query(User).\
...                 filter_by(name='wendy').\
...                 one()
>>> post = BlogPost("Wendy's Blog Post", "This is a test", wendy)
>>> session.add(post)
我们将关键字唯一地存储在数据库中，但我们知道我们还没有，所以我们可以创建它们：

>>> post.keywords.append(Keyword('wendy'))
>>> post.keywords.append(Keyword('firstpost'))
我们现在可以使用关键字“firstpost”查找所有博文。我们将使用 any运算符来查找“其中任何关键字都包含关键字字符串'firstpost'的博客帖子”：

SQL>>> session.query(BlogPost).\
...             filter(BlogPost.keywords.any(keyword='firstpost')).\
...             all()
[BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', password='foobar')>)]
如果我们想要查找用户拥有的帖子wendy，我们可以告诉查询缩小到该User对象作为父对象：

SQL>>> session.query(BlogPost).\
...             filter(BlogPost.author==wendy).\
...             filter(BlogPost.keywords.any(keyword='firstpost')).\
...             all()
[BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', password='foobar')>)]
或者我们可以使用Wendy自己的posts关系，这是一种“动态”关系，直接从那里查询：

SQL>>> wendy.posts.\
...         filter(BlogPost.keywords.any(keyword='firstpost')).\
...         all()
[BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', password='foobar')>)]

```

$$$ 映射器配置

本节介绍可与映射器一起使用的各种配置模式。它假设您已经完成了对象关系教程，并且知道如何构建和使用基本的映射器和关系。

!!!! 映射的类型

现代 SQLAlchemy 具有两种不同的映射器配置样式。“Classical”风格是 SQLAlchemy 的原始映射 API，而“Declarative”是建立在“Classical”之上的更丰富，更简洁的系统。两种样式可以互换使用，因为每种样式的最终结果完全相同 - 由 mapper()函数映射到可选单元的用户定义类 ，通常为 a Table。

@@@@@ 声明性映射

该声明映射是映射在现代 SQLAlchemy 的构造的典型方式。利用 Declarative 系统，可以立即定义用户定义类的组件以及 Table 类映射到的 元数据：

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
上面是一个包含四列的基本单表映射。其他属性（例如与其他映射类的关系）也在类定义中内联声明：

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    addresses = relationship("Address", backref="user", order_by="Address.id")

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'))
    email_address = Column(String)
声明映射系统在Object Relational Tutorial中引入 。有关此系统如何工作的其他详细信息，请参阅声明。
```

@@@@@ 经典映射

甲古典映射是指使用一个映射类的构造 mapper()函数，而无需使用声明性系统。这是 SQLAlchemy 的原始类映射 API，仍然是 ORM 提供的基本映射系统。

在“经典”形式中，表元数据与 Table 构造分别创建 ，然后 User 通过 mapper()函数与类关联：

```python
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper

metadata = MetaData()

user = Table('user', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50)),
            Column('fullname', String(50)),
            Column('password', String(12))
        )

class User(object):
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

mapper(User, user)
通过properties字典提供有关映射属性的信息，例如与其他类的关系。下面的示例说明了第二个Table 对象，映射到一个名为的类Address，然后链接到Uservia relationship()：

address = Table('address', metadata,
            Column('id', Integer, primary_key=True),
            Column('user_id', Integer, ForeignKey('user.id')),
            Column('email_address', String(50))
            )

mapper(User, user, properties={
    'addresses' : relationship(Address, backref='user', order_by=address.c.id)
})

mapper(Address, address)
使用经典映射时，必须直接提供类，而不必使用Declarative提供的“字符串查找”系统。SQL表达式通常根据Table对象来指定，即address.c.id上面是Address关系，而不是Address.id，因为Address可能尚未链接到表元数据，也不能在此处指定字符串。

文档中的一些示例仍然使用经典方法，但请注意，经典方法和声明方法是完全可互换的。两个系统最终都创建了相同的配置，由一个Table用户定义的类组成，并与一个链接在一起mapper()。当我们谈论“行为mapper()”时，这包括使用声明系统时 - 它仍然在幕后使用。
```

@@@@@ 映射，对象的运行时自省

Mapper 无论使用何种方法，都可以使用 Runtime Inspection API 系统从任何映射类获取该对象。使用该 inspect()函数，可以 Mapper 从映射的类中获取：

```python
>>> from sqlalchemy import inspect
>>> insp = inspect(User)
提供详细信息，包括Mapper.columns：

>>> insp.columns
<sqlalchemy.util._collections.OrderedProperties object at 0x102f407f8>
这是一个名称空间，可以以列表格式或通过单个名称查看：

>>> list(insp.columns)
[Column('id', Integer(), table=<user>, primary_key=True, nullable=False), Column('name', String(length=50), table=<user>), Column('fullname', String(length=50), table=<user>), Column('password', String(length=12), table=<user>)]
>>> insp.columns.name
Column('name', String(length=50), table=<user>)
其他名称空间包括Mapper.all_orm_descriptors，包括所有映射属性以及混合，关联代理：

>>> insp.all_orm_descriptors
<sqlalchemy.util._collections.ImmutableProperties object at 0x1040e2c68>
>>> insp.all_orm_descriptors.keys()
['fullname', 'password', 'name', 'id']
以及Mapper.column_attrs：

>>> list(insp.column_attrs)
[<ColumnProperty at 0x10403fde0; id>, <ColumnProperty at 0x10403fce8; name>, <ColumnProperty at 0x1040e9050; fullname>, <ColumnProperty at 0x1040e9148; password>]
>>> insp.column_attrs.name
<ColumnProperty at 0x10403fce8; name>
>>> insp.column_attrs.name.expression
Column('name', String(length=50), table=<user>)
```

!!!! 映射列和表达式

!!!! 映射类继承层次结构

!!!! 非传统映射

!!!! 配置版本计数器

!!!! 类映射 API

$$$ 关系配置

本节介绍**relationship()**其用法的功能和深入讨论。有关关系的介绍，请从对象关系教程开始， 然后进入构建关系。

!!!! 基本关系模式

关系相关导入

```python
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
```

@@@@@ 一对多

一对多关系将外键放在引用父对象的子表上。 relationship()然后在父项上指定，作为引用子项表示的项集合：

```python
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
要在一对多中建立双向关系，其中“反向”是多对一，请指定一个附加relationship()并使用以下relationship.back_populates参数连接两者：

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent", back_populates="children")
Child将获得parent具有多对一语义的属性。

或者，该backref选项可用于单个relationship()而不是使用 back_populates：

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", backref="parent")
```

@@@@@ 多对一

多对一将外键放在引用该子对象的父表中。 relationship()在父级上声明，将创建一个新的标量持有属性：

```python
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
通过添加秒relationship() 并relationship.back_populates在两个方向上应用参数来实现双向行为：

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child", back_populates="parents")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parents = relationship("Parent", back_populates="child")
或者，backref参数可以应用于单个relationship()，例如Parent.child：

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child", backref="parents")
```

@@@@@ 一对一

One To One 本质上是双向关系，双方都有标量属性。为实现此目的，该 uselist 标志指示在关系的“多”侧放置标量属性而不是集合。将一对多转换为一对一：

class Parent(Base):
**tablename** = 'parent'
id = Column(Integer, primary_key=True)
child = relationship("Child", uselist=False, back_populates="parent")

class Child(Base):
**tablename** = 'child'
id = Column(Integer, primary_key=True)
parent_id = Column(Integer, ForeignKey('parent.id'))
parent = relationship("Parent", back_populates="child")
或多对一：

class Parent(Base):
**tablename** = 'parent'
id = Column(Integer, primary_key=True)
child_id = Column(Integer, ForeignKey('child.id'))
child = relationship("Child", back_populates="parent")

class Child(Base):
**tablename** = 'child'
id = Column(Integer, primary_key=True)
parent = relationship("Parent", back_populates="child", uselist=False)
与往常一样，可以使用 relationship.backref 和 backref()函数来代替 relationship.back_populates 方法; 要 uselist 在 backref 上指定，请使用以下 backref()函数：

from sqlalchemy.orm import backref

class Parent(Base):
**tablename** = 'parent'
id = Column(Integer, primary_key=True)
child_id = Column(Integer, ForeignKey('child.id'))
child = relationship("Child", backref=backref("parent", uselist=False))

@@@@@ 多对多

Many to Many 在两个类之间添加了一个关联表。关联表由 secondary 参数表示 relationship()。通常，Table 使用 MetaData 与声明性基类关联的对象，以便 ForeignKey 指令可以找到要链接的远程表：

association_table = Table('association', Base.metadata,
Column('left_id', Integer, ForeignKey('left.id')),
Column('right_id', Integer, ForeignKey('right.id'))
)

class Parent(Base):
**tablename** = 'left'
id = Column(Integer, primary_key=True)
children = relationship("Child",
secondary=association_table)

class Child(Base):
**tablename** = 'right'
id = Column(Integer, primary_key=True)
对于双向关系，关系的两侧都包含一个集合。指定 using relationship.back_populates，并为每个 relationship()指定公共关联表：

association_table = Table('association', Base.metadata,
Column('left_id', Integer, ForeignKey('left.id')),
Column('right_id', Integer, ForeignKey('right.id'))
)

class Parent(Base):
**tablename** = 'left'
id = Column(Integer, primary_key=True)
children = relationship(
"Child",
secondary=association_table,
back_populates="parents")

class Child(Base):
**tablename** = 'right'
id = Column(Integer, primary_key=True)
parents = relationship(
"Parent",
secondary=association_table,
back_populates="children")
当使用 backref 参数代替时 relationship.back_populates，backref 将自动使用相同的 secondary 参数作为反向关系：

association_table = Table('association', Base.metadata,
Column('left_id', Integer, ForeignKey('left.id')),
Column('right_id', Integer, ForeignKey('right.id'))
)

class Parent(Base):
**tablename** = 'left'
id = Column(Integer, primary_key=True)
children = relationship("Child",
secondary=association_table,
backref="parents")

class Child(Base):
**tablename** = 'right'
id = Column(Integer, primary_key=True)
所述 secondary 的论点 relationship()也接受返回最终的说法，当第一次使用映射器，其仅被评估一个可调用。使用它，我们可以 association_table 在以后定义，只要在所有模块初始化完成后它可用于 callable：

class Parent(Base):
**tablename** = 'left'
id = Column(Integer, primary_key=True)
children = relationship("Child",
secondary=lambda: association_table,
backref="parents")
使用声明性扩展时，也接受传统的“表的字符串名称”，匹配存储在 Base.metadata.tables 以下表中的表的名称：

class Parent(Base):
**tablename** = 'left'
id = Column(Integer, primary_key=True)
children = relationship("Child",
secondary="association",
backref="parents")

@@@@@ 删除多个表中的行

这是唯一的一个行为 secondary 参数 relationship() 是，Table 它在这里指定为自动受 INSERT 和 DELETE 语句，如对象添加或从集合中删除。有没有必要从该表中手动删除。从集合中删除记录的行为将具有在 flush 上删除行的效果：

```python
&& row will be deleted from the "secondary" table
&& automatically
myparent.children.remove(somechild)
经常出现的一个问题是当子对象直接递送到“辅助”表中的行时如何删除Session.delete()：

session.delete(somechild)
这里有几种可能性：

如果存在relationship()from Parentto Child，但 没有将特定链接Child到每个的反向关系Parent，则SQLAlchemy将不会意识到在删除此特定 Child对象时，它需要维护将其链接到的“辅助”表Parent。不会删除“辅助”表。
如果存在将特定链接Child到每个特定的关系Parent，假设它被调用Child.parents，默认情况下SQLAlchemy将加载到Child.parents集合中以查找所有Parent对象，并从建立此链接的“辅助”表中删除每一行。请注意，此关系不需要是bidrectional; SQLAlchemy严格查看relationship()与Child被删除对象相关的每个内容。
这里性能更高的选项是使用ON DELETE CASCADE指令和数据库使用的外键。假设数据库支持此功能，则可以使数据库本身自动删除“辅助”表中的行，因为删除了“child”中的引用行。Child.parents 在这种情况下，可以指示SQLAlchemy 使用passive_deletes 指令on 来放弃在集合中的主动加载relationship(); 有关详细信息，请参阅使用被动删除。
请再次注意，这些行为仅与使用的secondary选项相关relationship()。如果处理显式映射且不存在于secondary相关选项中的关联表，则relationship()可以使用级联规则来自动删除实体以响应被删除的相关实体 - 有关此功能的信息，请参阅级联。
```

@@@@@ 关联对象

关联对象模式是多对多的变体：当关联表包含除左表和右表外键之外的其他列时，它会被使用。secondary 您可以将新类直接映射到关联表，而不是使用参数。关系的左侧通过一对多引用关联对象，关联类通过多对一引用右侧。下面我们说明映射到的关联表 Association，其包括称为柱类 extra_data，它是与之间每个关联一起存储的字符串值 Parent 和 Child：

class Association(Base):
**tablename** = 'association'
left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
extra_data = Column(String(50))
child = relationship("Child")

class Parent(Base):
**tablename** = 'left'
id = Column(Integer, primary_key=True)
children = relationship("Association")

class Child(Base):
**tablename** = 'right'
id = Column(Integer, primary_key=True)
与往常一样，双向版本使用 relationship.back_populates 或 relationship.backref：

class Association(Base):
**tablename** = 'association'
left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
extra_data = Column(String(50))
child = relationship("Child", back_populates="parents")
parent = relationship("Parent", back_populates="children")

class Parent(Base):
**tablename** = 'left'
id = Column(Integer, primary_key=True)
children = relationship("Association", back_populates="parent")

class Child(Base):
**tablename** = 'right'
id = Column(Integer, primary_key=True)
parents = relationship("Association", back_populates="child")
以直接形式使用关联模式要求子对象在被附加到父对象之前与关联实例相关联; 类似地，从父级到子级的访问通过关联对象：

```python
&& create parent, append a child via association
p = Parent()
a = Association(extra_data="some data")
a.child = Child()
p.children.append(a)

&& iterate through child objects via association, including association
&& attributes
for assoc in p.children:
    print(assoc.extra_data)
    print(assoc.child)
为了增强关联对象模式以便直接访问Association对象是可选的，SQLAlchemy提供了关联代理扩展。此扩展允许配置属性，这些属性将通过单个访问访问两个“跳”，一个“跳”到关联对象，第二个跳转到目标属性。
```

!!!! 邻接列表关系

!!!! 将关系与 Backref 联系起来

!!!! 配置关系如何连接

!!!! 集合配置和技术

!!!! 特殊关系持久性模式

!!!! 关系 API

$$$ 加载对象

!!!! 加载列

!!!! 关系加载技术

!!!! 加载继承层次结构

!!!! 构造函数和对象初始化

!!!! 查询 API

$$$ 使用会话

orm.mapper()和 declareative 扩展主要用于 ORM 接口，配置映射后。

使用 Session 进行持久化操作。

!!!! 会话基础

!!!! 国家管理

!!!! 瀑布

!!!! 交易和连接管理

!!!! 额外的持久性技术

!!!! 上下文/线程本地会话

!!!! 使用事件跟踪对象和会话更改

!!!! 会话 API

$$$ 事件和内部

!!!! ORM 活动

!!!! ORM 内部

!!!! ORM 例外

!!!! 不推荐使用的 ORM 事件接口

$$$ ORM 扩展

!!!! 关联代理

!!!! 自动地图

!!!! 烤查询

!!!! 陈述

!!!! 变异追踪

!!!! 订购清单

!!!! 水平分片

!!!! 混合属性

!!!! 可转位

!!!! 替代级仪表

$$$ ORM 示例

!!!! 映射食谱

!!!! 继承映射食谱

!!!! 特殊 API

!!!! 扩展 ORM

&& SqlAlchemy 官方文档-核心

&& SqlAlchemy 官方文档-数据库 API

&& 04 功能脚本

$$$ 重建表

```python
&& -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
from sqlalchemy.orm import aliased
from ..model.report import *

def re_create_table(ORM):
    try:
        ORM.__table__.drop(current_engine)
    except Exception ,e:
        print u"表不存在"
        &&print Exception ,e
    ORM.__table__.create(current_engine)

def re_create_tables(ORMS):
    for orm in ORMS:
        try:
            orm.__table__.drop(current_engine)
        except Exception ,e:
            print u"表不存在"
            &&print Exception ,e
    ORMS.reverse()
    for orm in ORMS:
        orm.__table__.create(current_engine)

if __name__ == '__main__':
    re_create_tables([Interest_Summary_test,FtpAcct_test,FTPAdj_test])
    re_create_table(SearchDataset)

```

$$$ 对象转 Dict

**方法一**
会存在额外无用 Key,需要删除

```python
res = session.query(User).first()
res.__dict__
```

**方法二**
to_dict()，配置在 Base 中即可。

```python
Base = sqlalchemy.ext.declarative.declarative_base()

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String)

&& 在基类中添加to_dict方法
def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict

p = session.query(Post).first()
p.to_dict()

&& to_dict代码样例
def to_dict(self):
    attrlist = [a for a in self.__dict__.keys() if not a.startswith('_')]
    data = {}
    for name in attrlist:
        d = getattr(self, name, None)
        if isinstance(d, datetime.datetime):
            d = d.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(d, datetime.date):
            d = d.strftime('%Y-%m-%d')
        elif isinstance(d, datetime.time):
            d =  d.strftime('%H:%M:%S')
        data[name] = d
    return data

setattr(Base, 'to_dict', to_dict)
```

&& 05 常见问题
