# -*- set coding:utf-8 -*-
''' 一些工具


- check_ip 检测ip地址的合法性  https://www.jb51.net/article/135943.htm
'''

import re

def check_ip(ipAddr,method="re"):
    u""" 检测ip地址的合法性

    :param ipAddr: IP地址
    """
    import IPy 
    ip_ok = False

    # 正则
    if method == "re":
        compile_ip=re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
        ip_ok = True if compile_ip.match(ipAddr) else False
    else:
        # 引入IPy类库
        try: 
            IPy.IP(ipAddr) 
            ip_ok = True
        except Exception as e: 
            ip_ok = False
    return ip_ok


  
if __name__ == '__main__':
    # 检测ip地址的合法性
    ip="32.34.56.78"
    print check_ip(ip,method="re")
    print check_ip(ip,method="")

