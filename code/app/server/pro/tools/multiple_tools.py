#! -*- coding:utf-8 -*-
from multiprocessing import Process
import os
import time
def info(name):
    print("name:",name)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    print("------------------")
    time.sleep(1)

def foo(name):
    info(name)

if __name__ == '__main__':

    info('main process line')
    
    
    p1 = Process(target=info, args=('alvin',))
    p2 = Process(target=foo, args=('egon',))
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    print("ending")
