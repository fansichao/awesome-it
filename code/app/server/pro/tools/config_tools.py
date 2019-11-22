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
- *.yaml yaml
- *.properties Pproperties


语法等说明
- ConfigParser
- yaml
- properties

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
import re
from collections import OrderedDict
import tempfile

import yaml
import sh

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


class Properties:
    u""" 读写 *.properties 文件

    https://www.cnblogs.com/momoyan/p/9145531.html
    """

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
    if file_name and not os.path.exists(file_name):
        sh.touch(file_name)

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
        print("file %s not found" % file_name)


if __name__ == '__main__':
    # yaml
    config_path = "/home/fdm/software/hugegraph/hugegraph-0.9.2/conf/gremlin-server.yaml"
    config_path = "test.yaml"
    config_data = read_config(config_path)
    write_config('test2.yaml', config_data=config_data, mode='a')

    # ini
    config_path = "config.ini"
    config_data = {
        'sectionA': {'a': 'b', 'key1': 123}
    }
    write_config('config2.ini', config_data=config_data, mode='a')
    read_config(config_path)

    # properties
    file_path = 'xxx.properties'
    props = parse(file_path)  # 读取文件
    props.put('key_a', 'value_a')  # 修改/添加key=value
    print(props.get('key_a'))  # 根据key读取value
    print("props.has_key('key_a')=" + str(props.has_key('key_a')))  # 判断是否包含该key
    print(props.properties)
