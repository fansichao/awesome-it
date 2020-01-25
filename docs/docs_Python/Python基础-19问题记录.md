# Python常见问题记录

记录一些python遇到的问题，或简或难，或提供一种思路。

类似于查询错误工具书。

## Python

### Attempted relative import in non-package

**错误信息:**
    - 包导入错误 ValueError: Attempted relative import in non-package
**问题原因：**
    - 1.由于不再程序当前目录执行，导致相对路径错误，无法运行程序。#导致存在的文件 找不到
    - 2.没有在外部运行 nosetests tests/app_test.py，而是在内部运行tests/nosetests app_test.py会导致这个错误。
    - 3.导入模块错误  from bin.app import app
    - 4.要么是你引用的路径不对，要么是没有创建 bin/__init__.py 文件,要么是没有配置 PYTHONPATH=.
**解决方法：**
    - 把主文件不断上移到顶层位置即可
    - 在上层运行命令 python -m src.task.main.xxxx
```python
from src.task.main import run
if __name__ == '__main__':
     run()
```

 
 ### 'ascii' codec can't decode byte 0xe6 in position 0: ordinal not in range(128)
**错误信息**
    - UnicodeDecodeError: 'ascii' codec can't decode byte 0xe6 in position 0: ordinal not in range(128)
    - 仅仅Python2可能存在此错误
**解决方法：**c
```python
import sys 
reload(sys)
sys.setdefaultencoding('utf8')    
```

## SqlAlchemy

### SqlAlchemy 查询错误

res = g.db_session.query(Table).filter(Table.col==u'是').all()   # 错误，数据库中的条件匹配不能加 u ，否则查无数据



