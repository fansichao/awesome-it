# /usr/bin/python3
#! -*- coding:utf-8 -*-

# 右键查看网页源码 得到 <文件2>
# 提示 find rare characters in the mess below 寻找出现次数最小的字符

def get_less_char():
    new_line = list()
    new_count = list()
    with open('2','rb') as f:
        data = f.read().replace('\n','')
        for i in list(data):
            if i not in new_line:
                new_line.append(i)
                new_count.append(1)
            else:
                new_count[new_line.index(i)] += 1
    return new_line,new_count

if __name__ == '__main__':
    new_line,new_count = get_less_char()
    print(new_line)
    # ['%', '$', '@', '_', '^', '#', ')', '&', '!', '+', ']', '*', '}', '[', '(', '{', '\n', 'e', 'q', 'u', 'a', 'l', 'i', 't', 'y']

    # TODO python2 可以 python3 不行？？？
    print(new_count)
    # [6104, 6046, 6157, 6112, 6030, 6115, 6186, 6043, 6079, 6066, 6152, 6034, 6105, 6108, 6154, 6046, 1220, 1, 1, 1, 1, 1, 1, 1, 1]
    print(''.join(['e', 'q', 'u', 'a', 'l', 'i', 't', 'y']))
    # 'equality'

