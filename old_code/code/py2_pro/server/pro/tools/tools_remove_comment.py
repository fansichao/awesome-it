# -*- coding:utf-8 -*-
'''
去除C语言注释

0:初始状态
1:可能遇到注释
2：进入多行注释
03）状态1中遇到/，说明进入单行注释部分，则进入状态4　　　　　　　　　ex. int a = b; //

04）状态1中没有遇到*或/，说明/是路径符号或除号，则恢复状态0　　　　  ex. <secure/_stdio.h> or 5/3

05）状态2中遇到*，说明多行注释可能要结束，则进入状态3　　　　　　　　ex. int a = b; /*heh*

06）状态2中不是遇到*，说明多行注释还在继续，则维持状态2　　　　　　　ex. int a = b; /*hehe

07）状态3中遇到/，说明多行注释要结束，则恢复状态0　　　　　　　　　　ex. int a = b; /*hehe*/

08）状态3中不是遇到/，说明多行注释只是遇到*，还要继续，则恢复状态2 　ex. int a = b; /*hehe*h

09）状态4中遇到\，说明可能进入折行注释部分，则进入状态9　　　　　　　ex. int a = b; //hehe\

10）状态9中遇到\，说明可能进入折行注释部分，则维护状态9　　　　　　　ex. int a = b; //hehe\\\

11）状态9中遇到其它字符，则说明进入了折行注释部分，则恢复状态4　　　 ex. int a = b; // hehe\a or hehe\<enter>

12）状态4中遇到回车符\n，说明单行注释结束，则恢复状态0 　　　　　　　ex. int a = b; //hehe<enter>

13）状态0中遇到'，说明进入字符常量中，则进入状态5 　　　　　　　　　　ex. char a = '

14）状态5中遇到\，说明遇到转义字符，则进入状态6　　　　　　　　　　　ex. char a = '\

15）状态6中遇到任何字符，都恢复状态5 　　　　　　　　　　　　　　　　ex. char a = '\n 还有如'\t', '\'', '\\' 等 主要是防止'\''，误以为结束

16）状态5中遇到'，说明字符常量结束，则进入状态0　　　　 　　　　　　　ex. char a = '\n'

17）状态0中遇到"，说明进入字符串常量中，则进入状态7　　　　　　　　　ex. char s[] = "

18）状态7中遇到\，说明遇到转义字符，则进入状态8　　　　　　　　　　　ex. char s[] = "\

19）状态8中遇到任何字符，都恢复状态7　　　　　　　　　　　　　　　 　ex. char s[] = "\n 主要是防止"\"，误以为结束

20）状态7中遇到"字符，说明字符串常量结束，则恢复状态0　　　　　　　　ex. char s[] = "\"hehe"
'''
# from __future__ import unicode_literals
import string
import math
import sys
import traceback
f = 'test.cpp'
try:
    with open(f, 'r') as reader:
        data = reader.readlines()
except Exception as e:
    print ">>>> [%s]文件load失败" % f

def dfa(lines):
    # for i in lines:
    #     for char in i:
    #         print(char)
    state = 0
    cur_idx = 0
    # cur_line = 0
    length = len(lines)
    i = 0
    newlines = []
    tmpstr = ''
    while(1):
        if i == length:
            break
        if cur_idx >= len(lines[i]):
            newlines.append(tmpstr)
            tmpstr = ''
            cur_idx = 0
            i = i + 1
            continue
        cur_char = lines[i][cur_idx]

        if state == 0 and lines[i][cur_idx] == '/':
            state = 1
        elif state ==1 and lines[i][cur_idx] == '*':
            state = 2
        elif state == 1 and lines[i][cur_idx] == '/':
            state = 4
        elif state == 1:
            # print('/')
            tmpstr = tmpstr+'/'
            newlines
            state = 0

        elif state == 2 and cur_char == '*':
            state = 3
        elif state == 2:
            state = 2

        elif state == 3 and cur_char == '/':
            state = 0
        elif state == 3:
            state = 2

        elif state == 4 and cur_char == '\\':
            state = 9
        elif state == 9 and cur_char == '\\':
            state = 9
        elif state == 9:
            state = 4
        elif state == 4 and cur_char == '\n':
            state = 0


        elif state == 0 and cur_char == '\'':
            state = 5
        elif state == 5 and cur_char == '\\':
            state = 6
        elif state == 6:
            state = 5
        elif state == 5 and cur_char == '\'':
            state = 0

        elif state == 0 and cur_char == '\"':
            state = 7
        elif state == 7 and cur_char == '\\':
            state = 8
        elif state == 8:
            state = 7
        elif state == 7 and cur_char == '\"':
            state = 0

        if (state == 0 and cur_char != '/') or state ==5 or state ==6 or state == 7 or state == 8:
            # print(cur_char)
            tmpstr = tmpstr + cur_char
        cur_idx = cur_idx + 1
    print("finished")




dfa(data)
print("finished")
