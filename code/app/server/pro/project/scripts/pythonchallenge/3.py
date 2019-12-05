# /usr/bin/python3
#! -*- coding:utf-8 -*-

# 右键查看网页源码 得到 <文件2>
# One small letter, surrounded by EXACTLY three big bodyguards on each of its sides.
# 寻找 周围三个大小字母 XXXxXXX 格式的字母

import string

lower = list(string.ascii_lowercase)
upper = list(string.ascii_uppercase)

letter = list()
with open('3','rb') as f:
    data = f.read().replace(b'\n',b'')
    for i in list(data):
        flag = str('1') if chr(i) in upper else str('0')
        letter.append(flag)

xx = "1110111"
# print(''.join(letter))
print(''.join(letter).findall(xx))
# 51
print([chr(i) for i in data[45:58]])

# linkedlist
