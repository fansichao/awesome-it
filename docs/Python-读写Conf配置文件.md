# Python 读写 Conf 配置文件

tags: Python ConfigParser 配置 conf ini yaml properties 2019 年 11 月

环境说明: Python2.7.11 CentOS7.6

TODO 不同种类配置文件对比

## .yaml

### yaml 说明介绍

YAML 是专门用来写配置文件的语言，非常简洁和强大，远比 JSON 格式方便。

YAML 在 python 语言中有 PyYAML 安装包。

YAML 语言（发音 /ˈjæməl/ ）的设计目标，就是方便人类读写。它实质上是一种通用的数据串行化格式。

### yaml 语法规则

它的基本语法规则如下：
1、大小写敏感
2、使用缩进表示层级关系
3、缩进时不允许使用 Tab 键，只允许使用空格。
4、缩进的空格数目不重要，只要相同层级的元素左侧对齐即可
5、# 表示注释，从这个字符一直到行尾，都会被解析器忽略，这个和 python 的注释一样

YAML 支持的数据结构有三种：
1、对象：键值对的集合，又称为映射（mapping）/ 哈希（hashes） / 字典（dictionary）
2、数组：一组按次序排列的值，又称为序列（sequence） / 列表（list）
3、纯量（scalars）：单个的、不可再分的值。字符串、布尔值、整数、浮点数、Null、时间、日期

### yaml 文件样例

```yaml
channelizer: org.apache.tinkerpop.gremlin.server.channel.HttpChannelizer
graphs:
  {
    hugegraph: conf/hugegraph.properties,
    hugegraph1: conf/hugegraph1.properties,
    hugegraph2: conf/hugegraph2.properties,
    test01: conf/hugegraphtest01.properties,
  }
maxAccumulationBufferComponents: 1024
maxChunkSize: 8192
maxContentLength: 65536
maxHeaderSize: 8192
maxInitialLineLength: 4096
metrics:
  consoleReporter: { enabled: false, interval: 180000 }
  csvReporter:
    {
      enabled: true,
      fileName: /tmp/gremlin-server-metrics.csv,
      interval: 180000,
    }
  gangliaReporter:
    { addressingMode: MULTICAST, enabled: false, interval: 180000 }
  graphiteReporter: { enabled: false, interval: 180000 }
  jmxReporter: { enabled: false }
  slf4jReporter: { enabled: false, interval: 180000 }
plugins: [com.baidu.hugegraph]
```

### yaml 参考链接

- [博客-python 中读取 yaml](https://www.cnblogs.com/klb561/p/10085328.html)

## .ini 文件

### ini 说明介绍

[Python3 官方 ConfigParser](https://docs.python.org/3/library/configparser.html?highlight=configparser)该模块提供了实现基本配置语言的类，该类提供的结构类似于 Microsoft Windows INI 文件中的结构。可以使用它来编写可由最终用户轻松定制的 Python 程序。

### ini 语法规则

ConfigParser 的一些问题：

- 不能区分大小写。
- 重新写入的配置文件不能保留原有配置文件的注释。
- 重新写入的配置文件不能保持原有的顺序。
- 不支持嵌套。
- 不支持格式校验。
- 易用性

注意事项

- 配置参数读出来都是字符串类型， 参数运算时，注意类型转换，另外，对于字符型参数，不需要加""
- 只要注意配置文件的参数尽量使用小写/大写,统一即可

### ini 常用函数

读取配置文件

- read(filename) 直接读取 ini 文件内容
- sections() 得到所有的 section，并以列表的形式返回
- options(section) 得到该 section 的所有 option
- items(section) 得到该 section 的所有键值对
- get(section,option) 得到 section 中 option 的值，返回为 string 类型
- getint(section,option) 得到 section 中 option 的值，返回为 int 类型
- getfloat(section,option)得到 section 中 option 的值，返回为 float 类型
- getboolean(section, option)得到 section 中 option 的值，返回为 boolean 类型

写入配置文件

- add_section(section) 添加一个新的 section
- has_section(section) 判断是否有 section
- set(section, option, value) 对 section 中的 option 进行设置
- remove_setion(section)删除一个 section
- remove_option(section, option)删除 section 中的 option
- write(fileobject)将内容写入配置文件。

配置文件类型问题

- getint(section,option) 返回 int 类型
- getfloat(section, option) 返回 float 类型
- getboolean(section,option) 返回 boolen 类型

### ini 文件样例

```ini
[user] # section
username = tom # key = val 或 key: val
password = ***
email = test@host.com

[book]
bookname = python
bookprice = 25
```

### ini 参考链接

- [Python3 官方 ConfigParser](https://docs.python.org/3/library/configparser.html?highlight=configparser)
- [ConfigParser 模块](https://www.cnblogs.com/lovychen/p/9431359.html)

## .properties 文件

Python 中正好没有解析 properties 文件的现成模块,所以单独编写了一个脚本用于读写 \*.properties 文件

### properties 文件样例

```properties
restserver.url=http://0.0.0.0:8080

# graphs list with pair NAME:CONF_PATH
graphs=[test01:conf/hugegraphtest01.properties,hugegraph:conf/hugegraph.properties,hugegraph1:conf/hugegraph1.properties,hugegraph2:conf/hugegraph2.properties]

# authentication
#auth.require_authentication=
#auth.admin_token=
#auth.user_tokens=[]
```

### properties 参考链接

- [Python：解析 properties 文件](https://www.cnblogs.com/momoyan/p/9145531.html)

## 附件

### 读写 _.ini/_.yaml 文件 完整代码

```python

# -* - coding: UTF-8 -* -
u""" Python 读写 配置文件

逻辑说明:
- read_config           读取配置文件入口函数
    - read_config_ini
    - read_config_yaml
- write_config          写入配置文件入口函数
    - write_config_ini
    - write_config_yaml
- 函数配置调用
    - 根据 postfix_func_dict 指定文件后缀调用函数
    - 单独指定读取某类文件时,直接传入参数 filename_postfix 即可


支持以下配置文件读写
- *.ini ConfigParser
- *.yaml yaml TODO


语法等说明
- ConfigParser
- yaml

# 配置文件使用样例 ConfigParser
https://www.cnblogs.com/klb561/p/10085328.html


# *.yaml pyyaml
pip  install pyyaml
"""

import os
import ConfigParser
import sys
import traceback
import logging

import yaml

reload(sys)
sys.setdefaultencoding("utf-8")

# 指定 不同后缀调用不同方法
postfix_func_dict = {
    '.ini': 'ini',
    '.yaml': 'yaml',
}
# 默认配置后缀
default_filename_postfix = '.ini'

ini_config_data = [
    {'section': 'scetionA', 'section_vals': [
        {'key': '', 'val': '', 'dtype': ''},
        {'key': '', 'val': '', 'dtype': ''},
    ]}
]

ini_config_data = {
    'sectionA': {
        'key1': 'val1',
        'key2': 'val2',
    },
    'sectionB': {
        'key11': 'val11',
        'key21': 'val21',
    },
}

from collections import OrderedDict


def read_config(config_path, filename_postfix=None):
    u""" 读取配置文件

    :param str config_path: 配置文件路径
    :param str filename_postfix: 配置文件类型 ini / yaml
    """
    config_data = OrderedDict(dict())
    if not config_path or not os.path.exists(config_path):
        logging.error("配置文件[%s]为空或不存在", config_path)
        return config_data

    filename_postfix = filename_postfix if filename_postfix else os.path.splitext(config_path)[1]
    # TODO 动态 根据字符串 调用函数
    config_data = globals().get('read_config_%s' % postfix_func_dict.get(filename_postfix, default_filename_postfix))(
        config_path)

    logging.info("读取配置文件[%s]成功,配置信息[%s]", config_path, config_data)
    return config_data


def read_config_yaml(config_path):
    u""" 读取配置文件

    :param str config_path: 配置文件路径

    :return: dict config_data
    """
    # 加上 ,encoding='utf-8'，处理配置文件中含中文出现乱码的情况。
    config_data = OrderedDict(dict())
    try:
        # f = open(config_path, 'r', encoding='utf-8')
        f = open(config_path, 'r')
        config = f.read()
        if float(yaml.__version__) <= 5.1:
            config_data = yaml.load(config)
        else:
            # 5.1版本后 使用 FullLoader 更加安全
            config_data = yaml.load(config, Loader=yaml.FullLoader)
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error("配置文件[%s]无法正常解析,请检查!", config_path)
    return config_data


def read_config_ini(config_path):
    u""" 读取配置文件

    :param str config_path: 配置文件路径

    :return: dict config_data
    """
    config_data = OrderedDict(dict())
    if not config_path or not os.path.exists(config_path):
        logging.error("配置文件[%s]为空或不存在", config_path)
        return config_data

    try:
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'%s' % config_path))
        for section in config.sections():
            config_data[section] = OrderedDict(dict())
            for key, val in config.items(section):
                config_data[section][key] = val
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error("配置文件[%s]无法正常解析,请检查!", config_path)
    return config_data


def write_config(config_path, config_data, filename_postfix=None, mode='a', funcname=None):
    u""" 写入配置文件

    :param str config_path: 配置文件
    :param dict config_data: 配置字典
    :param str filename_postfix: 配置文件类型 ini / yaml . 为空时自动读取文件名称后缀,根据不同后缀调用不同函数
    :param str mode: 数据时 追加写入还是覆盖等 a w
    """

    filename_postfix = filename_postfix if filename_postfix else os.path.splitext(config_path)[1]
    mode = mode if mode and mode in ['a', 'w'] else 'a'

    # TODO 动态 根据字符串 调用函数
    config_data = globals().get('write_config_%s' % postfix_func_dict.get(filename_postfix, default_filename_postfix)) \
        (config_path, config_data, mode)

    logging.info("读取配置文件[%s]成功,配置信息[%s]", config_path, config_data)


def write_config_yaml(config_path, config_data, mode):
    u""" 写入配置文件

    :param str config_path: 配置文件
    :param dict config_data: 配置字典
    :param str mode: 数据时 追加写入还是覆盖等 a w
    """
    # fw = open(yamlPath, 'a', encoding='utf-8')
    fw = open(config_path, mode)  # a 追加写入，w,覆盖写入
    yaml.dump(config_data, fw)
    return config_data


def write_config_ini(config_path, config_data, mode):
    u""" 写入配置文件

    :param str config_path: 配置文件
    :param dict config_data: 配置字典
    :param str mode: 数据时 追加写入还是覆盖等 a w
    """

    config = ConfigParser.ConfigParser()
    if not os.path.exists(config_path):
        new_config_dic = config_data
    else:
        new_config_dic = read_config(config_path)
        # 当配置文件已经存在时, 将会使用新的dic更新原有配置
        if mode == 'a':
            new_config_dic.update(config_data)

    for section, section_vals in config_data.items():
        config.add_section(section)
        for key, val in section_vals.items():
            config.set(section, key, val)
    config.write(open(config_path, "w"))
    logging.info("写入配置文件[%s]完成", config_path)
    return config_data


if __name__ == '__main__':
    # yaml
    config_path = "test.yaml"
    config_path = "/home/fdm/software/hugegraph/hugegraph-0.9.2/conf/gremlin-server.yaml"
    config_data = read_config(config_path)
    write_config('test2.yaml', config_data=config_data, mode='a')
    exit()

    # ini
    config_path = "config.ini"
    config_data = {
        'sectionA': {'a': 'b', 'key1': 123}
    }
    write_config('config2.ini', config_data=config_data, mode='a')
    read_config(config_path)
```

### 读写 .properties 文件 完整代码

```python
#! -*- coding:utf-8
u""" Config
    读写 *.properties 文件
https://www.cnblogs.com/momoyan/p/9145531.html
"""
import re
import os
import tempfile
from collections import OrderedDict


class Properties:

    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = OrderedDict({})
        try:
            fopen = open(self.file_name, 'r')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except Exception, e:
            raise e
        else:
            fopen.close()

    def has_key(self, key):
        return key in self.properties

    def get(self, key, default_value=''):
        if key in self.properties:
            return self.properties[key]
        return default_value

    def put(self, key, value):
        self.properties[key] = value
        replace_property(self.file_name, key + '=.*', key + '=' + value, True)


def parse(file_name):
    return Properties(file_name)


def replace_property(file_name, from_regex, to_str, append_on_not_exists=True):
    tmpfile = tempfile.TemporaryFile()

    if os.path.exists(file_name):
        r_open = open(file_name, 'r')
        pattern = re.compile(r'' + from_regex)
        found = None
        for line in r_open:
            if pattern.search(line) and not line.strip().startswith('#'):
                found = True
                line = re.sub(from_regex, to_str, line)
            tmpfile.write(line)
        if not found and append_on_not_exists:
            tmpfile.write('\n' + to_str)
        r_open.close()
        tmpfile.seek(0)

        content = tmpfile.read()

        if os.path.exists(file_name):
            os.remove(file_name)

        w_open = open(file_name, 'w')
        w_open.write(content)
        w_open.close()

        tmpfile.close()
    else:
        print "file %s not found" % file_name



if __name__ == '__main__':
    file_path = 'xxx.properties'
    props = parse(file_path)   #读取文件
    props.put('key_a', 'value_a')       #修改/添加key=value
    print props.get('key_a')            #根据key读取value
    print "props.has_key('key_a')=" + str(props.has_key('key_a'))   #判断是否包含该key
    print props.properties()
```
