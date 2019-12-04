#! -*- coding:utf-8 -*-
u"""

文件处理

"""


###############
#### file 处理
###############

def file_read(filename=None,encoding='utf-8'):
    u""" 读取文件
    """
    with open(filename, 'r', encoding=encoding) as f:
        yield f.read()
        print(f.read())
    
#read(),readline(),readlines()




###############
#### json 处理
###############
import json
def json_dumps(json_dict={"a":"v"}):
    u""" 将 字典 转换为 字符串 """
    json_str = json.dumps(json_dict)
    return json_str

def json_loads(json_str='{"a":"v"}'):
    u""" 将 字符串 转为 字典 """
    json_dict = json.loads(json_str)
    return json_dict
        
def json_dump(file_name, json_dict):
    u""" 将数据写入文件中"""
    with open(file_name,"w") as f:
        json.dump(json_dict,f)
        print("加载入文件完成...")

def json_load(file_name):
    u""" 读取文件中的json数据 """
    with open(file_name,'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict
    
def str2json(json_str, deep=None):
    u""" 将任意深度 字符串 转 json """
    pass



if __name__ == '__main__':
    pass
