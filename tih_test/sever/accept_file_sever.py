#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/8/31 13:42
# @Author : Ruanzhe
# @File : accept_file_sever.py
# @Software: PyCharm
import socket
import os
import hashlib
import time
from threading import Thread


if __name__ == '__main__':
    filename = "test.txt"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket
    server.bind(('127.0.0.1', 8096))
    server.listen(5)  # 最大等待数
    print("服务端已启动，等待客户端连接...")

    while True:
        conn, addr = server.accept()

        print('接受来自{}：{}的连接'.format(conn, addr))

        while True:

            # 接收机器号
            receive_cpn = conn.recv(1024)
            computer_number = receive_cpn.decode()
            try:
                data = conn.recv(1024)
            except ConnectionResetError:
                print("客户端断开连接")
            if not data:
                print('客户端断开连接')
                break

            # 打印文件名
            print('接收到的文件名为：' + filename)

            # 接受文件大小
            response = conn.recv(1024)

            # 发送确认信息
            conn.send(b'ok')

            # 时间戳
            time_stamp = str(int(round(time.time() * 1000)))

            # 新建文件名称’文件名+时间戳.后缀‘
            new_filename = str(computer_number) + '_' + str(filename).split('.')[0] + time_stamp + '.' + \
                           str(filename).split('.')[1]

            # 转整形，方便下面大小判断
            file_size = int(response.decode())

            # 赋值方便最后打印大小
            new_file_size = file_size

            # 写模式创建文件
            f = open(new_filename, 'wb')

            # 生成md5对象
            m = hashlib.md5()

            # 进入循环判断收文件
            while new_file_size > 0:
                data = conn.recv(1024)

                # 收多少减多少
                new_file_size -= len(data)

                # 同步服务器端，收一次更新一次md5
                m.update(data)

                # 写入数据
                f.write(data)
            else:

                # 得到下载完的文件的md5
                new_file_md5 = m.hexdigest()

                # 打印下载文件大小
                print('接收到文件大小为:' + str(file_size) + '字节')
                f.close()

            # 接收客户端的文件的md5
            server_file_md5 = conn.recv(1024).decode()

            # 打印两端的md5值，看是否相同
            print('server file md5:', server_file_md5 - receive_cpn)
            print('recv file md5:', new_file_md5)
            if server_file_md5[:-3] == new_file_md5:
                print('传输完成！')
            else:
                print('传输失败！')

        else:
            continue
