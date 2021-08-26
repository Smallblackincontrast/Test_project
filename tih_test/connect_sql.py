# -*- coding:utf-8 -*-
import pymysql

# 清华大学 https://pypi.tuna.tsinghua.edu.cn/simple/


def connect():
    global data
    db = pymysql.connect(
        host="192.168.100.99",
        user="test",
        password="test",
        port=3306,
        db="autotest",
        charset="utf8"
    )
    try:
        # 创建游标
        cursor = db.cursor()
        try:
            sql = "SELECT * FROM tih_app_users"
            # sql = "SELECT * FROM tih_app_users WHERE department='测试部'"
            cursor.execute(sql)
            # data = list(cursor.fetchall())
            data = list(cursor.fetchall())
            # 执行语句
            # db.commit()
        except Exception as e:
            db.close()
    except Exception as e:
        db.close()
    finally:
        db.close()
    return data


if __name__ == "__main__":
    connect()

