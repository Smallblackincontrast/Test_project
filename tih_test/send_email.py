# -*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime
from email.mime.application import MIMEApplication


my_sender = 'sibo.guo@tihchip.com'  # 发件人邮箱账号
my_pass = '19960220Guo@'  # 发件人邮箱密码,如果是qq邮箱要加授权码不是登录密码
my_user = 'sibo.guo@tihchip.com'  # 收件人邮箱账号，我这边发送给自己
user_1 = 'ruanzhe@tihchip.com'    # 第二个账号,可以添加多个，在sendmail列表中添加


def mail():
    ret = True
    try:
        message = MIMEMultipart()
        message['From'] = formataddr(("郭泗博", my_sender))  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        # message['To'] = formataddr(("郭", my_user))  # 括号里的对应收件人邮箱昵称、收件人邮箱账号，可以跳过此步骤，直接在sendmail加入列表中

        # 邮件的主题，也可以说是标题
        message['Subject'] = "群发邮件测试"

        "发送正文"
        message.attach(MIMEText('这里写正文', 'plain', 'utf-8'))

        "发送附件txt格式"
        msg_enclosure_txt = MIMEText(open(r'E:\key.txt', mode='r').read(), 'base64', 'utf-8')
        msg_enclosure_txt["Content-Type"] = 'application/octet-stream'

        # filename 写成什么，附件的名字就是什么，好像也可以该后缀
        msg_enclosure_txt["Content-Disposition"] = 'attachment; filename="key.txt"'
        message.attach(msg_enclosure_txt)

        "发送附件excel表格"
        data = open(r'E:\XLS.csv', mode='r')
        content = data.read()
        print()
        data.close()
        msg_enclosure_excel = MIMEApplication(open(r'E:\XLS.csv', mode='r').read(), 'gbk')
        msg_enclosure_excel["Content-Type"] = 'application/x-www-form-urlencoded'
        msg_enclosure_excel["Content-Disposition"] = 'attachment; filename="XLS.csv"'
        message.attach(msg_enclosure_excel)



        "发件人邮箱中的SMTP服务器，端口默认25"
        server = smtplib.SMTP_SSL("smtp.tihchip.com", 465)

        # 括号中对应的是发件人邮箱账号、邮箱密码
        server.login(my_sender, my_pass)

        # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.sendmail(my_sender, [my_user], message.as_string())

        # 关闭连接
        server.quit()
    except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print(e)
        ret = False
    return ret


def main():
    ret = mail()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")


if __name__ == "__main__":
    main()