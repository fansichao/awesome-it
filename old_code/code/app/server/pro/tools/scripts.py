#! -*- coding:utf-8 -*-
u"""  脚本/工具 整理



*   sh：一个完备的 subprocess 替代库。[官网](https://github.com/amoffat/sh)


"""

def script_sh():
    u""" subprocess 替代库. 使用Python操作Bash
    """
    import sh
    print sh.ifconfig("eth0")
    print sh.ls("-lsrt", ".", color="never")
    print dir(sh)

def scripts():
    script_sh()



if __name__ == '__main__':
    scripts()
    pass
