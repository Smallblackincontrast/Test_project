# -*- coding:utf-8 -*-
import multiprocessing
from multiprocessing import Process, Lock
import os
import time
import os


def info():
    # local_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # file_name = r"E:\testbig\bigfile" + "\\" + str(local_time) + '.txt'
    # bigFile= open(file_name, "w", encoding="utf-8")
    # bigFile.seek(1024*1024*1024*1)
    # bigFile.write("test")
    # bigFile.flush()
    # bigFile.close()
    print("PID %s" % os.getpid())


def f(name):
    info()
    print(multiprocessing.cpu_count())


def prc():
    i = 0
    while i <= 5:
        p = Process(target=f, args=("66",))
        p.start()
        # p.join()
        # time.sleep(1)
        i += 1


if __name__ == '__main__':
    # info()
    print("开始")
    prc()
