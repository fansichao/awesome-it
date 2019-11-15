# Python读写Conf配置文件

tags: Python ConfigParser 配置 conf ini 2019年 11月

环境说明: Python2.7.11 CentOS7.6

## 说明介绍

[Python3官方ConfigParser](https://docs.python.org/3/library/configparser.html?highlight=configparser)该模块提供了实现基本配置语言的类，该类提供的结构类似于Microsoft Windows INI文件中的结构。可以使用它来编写可由最终用户轻松定制的Python程序。

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

TODO 其他读写配置文件对比

## 术语说明

```bash
[user] # section 分组
username = tom # option 键值对
password = ***
email = test@host.com

[book]
bookname = python
bookprice = 25
```

## 附件

### 使用样例

配置文件 ```confi.ini```

```conf
[user] # section 分组
username = tom # option 键值对
password = ***
email = test@host.com

[book]
bookname = python
bookprice = 25
```

参考链接: [ConfigParser模块](https://www.cnblogs.com/lovychen/p/9431359.html)

样例代码

```python

# -* - coding: UTF-8 -* -
import ConfigParser
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

# 生成config对象
config = ConfigParser.ConfigParser()
# 用config对象读取配置文件
config.readfp(open(r'pro/tools/config.ini'))

# 以列表形式返回所有的section
sections = config.sections()
print 'sections:', sections   #sections: ['user', 'book']
# 得到指定section的所有option
options = config.options("user")
print 'options:', options  #options: ['username', 'password', 'email']
# 得到指定section的所有键值对
useritem = config.items("user")
print 'user:', useritem #user: [('username', 'tom'), ('password', '***'), ('email', 'test@host.com')]
# 指定section，option读取值
str_val = config.get("book", "bookname")
int_val = config.getint("book", "bookprice")

print "value for book's bookname:", str_val   #value for book's bookname: python
print "value for book's bookprice:", int_val   #value for book's bookprice: 25

# 写配置文件
# 更新指定section，option的值
config.set("book", "bookname", "python learning")
# 写入指定section增加新option和值
config.set("book", "bookpress", "人民邮电出版社")
# 增加新的section
config.add_section('purchasecar')
config.set('purchasecar', 'count', '1')
# 写回配置文件
config.write(open("config.ini", "w"))

class ConfigParser():
    config_dic = {}
    @classmethod
    def get_config(cls, sector, item):
        value = None
        try:
            value = cls.config_dic[sector][item]
        except KeyError:
            cf = configparser.ConfigParser()
            cf.read('settings.ini', encoding='utf8')  #注意setting.ini配置文件的路径
            value = cf.get(sector, item)
            cls.config_dic = value
        finally:
            return value
```

### 完整代码样例

file_config_tools.py

```python
# -* - coding: UTF-8 -* -
u""" Python2 ConfigParser 读写 配置文件

"""

import os
import ConfigParser
import sys
import traceback
import logging

reload(sys)
sys.setdefaultencoding("utf-8")


config_dic = {
    'sectionA':{
        'key1':'val1',
        'key2':'val2',
    },
    'sectionB':{
        'key11':'val11',
        'key21':'val21',
    },
}

def read_config(config_path):
    u""" 读取配置文件

    :param str config_path: 配置文件路径

    :return: dict config_dic
    """
    config_dic = {};
    if not config_path or not os.path.exists(config_path):
        logging.error("配置文件[%s]为空或不存在", config_path)
        return config_dic

    try:
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'%s'%config_path))
        for section in config.sections():
            config_dic[section] = {}
            for key, val in config.items(section):
                config_dic[section][key] = val
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error("配置文件[%s]无法正常解析,请检查!", config_path)
    return config_dic


def write_config(config_path, config_dic):
    u""" 写入配置文件

    :param str config_path: 配置文件
    :param dict config_dic: 配置字典
    """
    config = ConfigParser.ConfigParser()
    if not os.path.exists(config_path):
        new_config_dic = config_dic
    else:
        new_config_dic = read_config(config_path)
        # TODO 当配置文件已经存在时, 将会使用新的dic更新原有配置
        new_config_dic.update(config_dic)

    for section, section_vals in new_config_dic.items():
        config.add_section(section)
        for key, val in section_vals.items():
            config.set(section, key, val)
    config.write(open(config_path, "w"))
    logging.info("写入配置文件[%s]完成", config_path)
    return config

if __name__ == '__main__':
    config_path = "config.ini"
    config_dic = {
        'sectionA':{'a':'b','key1':123}
    }
    write_config(config_path, config_dic)
    read_config(config_path)
```

### 常用函数

读取配置文件

- read(filename) 直接读取ini文件内容
- sections() 得到所有的section，并以列表的形式返回
- options(section) 得到该section的所有option
- items(section) 得到该section的所有键值对
- get(section,option) 得到section中option的值，返回为string类型
- getint(section,option) 得到section中option的值，返回为int类型
- getfloat(section,option)得到section中option的值，返回为float类型
- getboolean(section, option)得到section中option的值，返回为boolean类型

写入配置文件

- add_section(section) 添加一个新的section
- has_section(section) 判断是否有section
- set(section, option, value) 对section中的option进行设置
- remove_setion(section)删除一个section
- remove_option(section, option)删除section中的option
- write(fileobject)将内容写入配置文件。

配置文件类型问题

- getint(section,option) 返回int类型
- getfloat(section, option)  返回float类型
- getboolean(section,option) 返回boolen类型
