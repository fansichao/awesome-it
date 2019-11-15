# -* - coding: UTF-8 -* -
u""" Python 读写 配置文件


支持以下配置文件读写

- *.ini ConfigParser
- *.yaml pyyaml TODO



# 配置文件使用样例 ConfigParser
https://www.cnblogs.com/klb561/p/10085328.html

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

