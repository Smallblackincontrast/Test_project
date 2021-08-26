# import datetime
import time
import os
from django.utils import timezone as datetime

from django.shortcuts import render, redirect
from . import models
from django.http import HttpResponse
import connect_sql
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# 引入发送邮件的模块
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.


def home(request):
    return render(request, "home.html")


def data_increase(request):
    data = ""
    if request.method == "POST":
        account = request.POST.get("account")
        password = request.POST.get("password")
        name = request.POST.get("name")
        sex = request.POST.get('sex')
        department = request.POST.get('department')
        email = request.POST.get('email')
        remark = request.POST.get("remark")
        userInfo_save = models.Users(account=account,
                                     password=password,
                                     name=name,
                                     sex=sex,
                                     department=department,
                                     email=email,
                                     remark=remark,
                                     )
        userInfo_save.save()
        return redirect('/display/')
    return render(request, 'data_increase.html')


def data_display(request):
    error_msg = ""
    data_list = []
    # = datas_dict = models.Users.objects.all()
    datas = connect_sql.connect()
    for data in datas:
        user_info = list(data)
        data_list.append(user_info)

    # try:
    #     if request.method == "POST":
    #         content = "message"
    #         send_mail(subject='Send email test', message=content, from_email='sibo.guo@tihchip.com',
    #                   recipient_list=['sibo.guo@tihchip.com'], fail_silently=False)
    # except:
    #     print("失败")
    return render(request, 'data_display.html', {"data_list": data_list, "len": len(data_list)})


def delete_user(request):
    pk = request.GET.get('id')
    if pk:
        obj = models.Users.objects.filter(id=pk)
        obj.delete()
        return redirect('/display/')


def data_update(request):
    err_msg = ""
    pk = request.GET.get('id')
    object_pk = models.Users.objects.filter(pk=pk).first()  # 获得的对应id的数据
    date_list = [object_pk.id, object_pk.account, object_pk.password, object_pk.name, object_pk.sex,
                 object_pk.department, object_pk.email, object_pk.remark]
    if request.method == "POST":
        account = request.POST.get('account')
        password = request.POST.get('password')
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        department = request.POST.get('department')
        email = request.POST.get('email')
        remark = request.POST.get('remark')
        if sex == '':
            sex = request.POST.get('sex_null')

        if department == '':
            department = request.POST.get('depart_null')

        userInfo_save = models.Users(pk=object_pk.id,
                                     account=account,
                                     password=password,
                                     name=name,
                                     sex=sex,
                                     department=department,
                                     email=email,
                                     remark=remark,
                                     )
        userInfo_save.save()
        return redirect('/display/')
    return render(request, 'update.html', {"date_list": date_list})


def date_check(request):
    if request.method == "POST":
        depart_date = request.POST.get('department')
        sex_date = request.POST.get('sex')
        if sex_date == '':
            # 表示只输入了部门
            depart_all = models.Users.objects.filter(department=depart_date).all()
            return render(request, 'date_check.html', {"date_all": depart_all})

        if depart_date == '':
            # 表示只输入了性别
            sex_all = models.Users.objects.filter(sex=sex_date).all()
            return render(request, 'date_check.html', {"date_all": sex_all})

        if (depart_date != '') and (sex_date != ''):
            # 表示都输入了
            date_all = models.Users.objects.filter(department=depart_date, sex=sex_date).all()
            return render(request, 'date_check.html', {"date_all": date_all})


def burnin_data_display(request, pindex=1):
    """
    burnin结果展示
    :param request:
    :param pindex:
    :return:
    """
    time_stamp = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")  # 获取当天零点日期
    result_list = models.Burnin_Result.object.filter(timestamp__gte=time_stamp).all().values_list('ip', 'disk',
                                                                                                  'runtime', 'state',
                                                                                                  'result',
                                                                                                  'timestamp')
    paginator = Paginator(result_list, 15)
    if paginator.count == 0:
        total_results_counts = 0
    else:
        total_results_counts = paginator.count
    if pindex == None:  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    send_burnin_html(request, result_list)
    return render(request, 'burnin_result.html',
                  {'page': page, "pindex": pindex, " total_results_counts": total_results_counts})


def burnin_data_search(request, pindex=1):
    """
    burnin结果查询
    :param request:
    :param pindex:
    :return:
    """
    # if request.method == 'POST':  # 当提交表单时
    time_stamp = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"),
                                            "%Y-%m-%d")  # 获取当天零点日期
    null = ''
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    state = request.GET.get('state')
    # 接收存储查询条件
    mywhere = []
    url_add = ''
    if state == null:
        if start_date == null:
            # state & start_date & end_date is null
            if end_date == null:
                mywhere.append("start_date=" + '')
                mywhere.append("end_date=" + '')
                mywhere.append("state=" + '')
                burnin_result = list(models.Burnin_Result.object.all().values_list('ip',
                                                                                   'disk',
                                                                                   'runtime',
                                                                                   'state',
                                                                                   'result',
                                                                                   'timestamp'))
            # state & start_date is null;end_date is not null
            else:
                mywhere.append("start_date=" + '')
                mywhere.append("end_date=" + end_date)
                mywhere.append("state=" + '')
                data_to = datetime.datetime(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:]), 0, 0)
                burnin_result = list(models.Burnin_Result.object.filter(timestamp__lte=data_to).all().values_list(
                    'ip', 'disk',
                    'runtime',
                    'state',
                    'result',
                    'timestamp'))

        # state is null;start date is not null
        else:
            # state & end_date is null;start date is not null;
            mywhere.append("start_date=" + start_date)
            mywhere.append("end_date=" + '')
            mywhere.append("state=" + '')
            if end_date == null:
                data_from = datetime.datetime(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:]), 0,
                                              0)
                burnin_result = list(models.Burnin_Result.object.filter(timestamp__gte=data_from).all().values_list(
                    'ip', 'disk', 'runtime', 'state', 'result', 'timestamp'))

            # state is null;start date & end_date is not null;
            else:
                mywhere.append("start_date=" + start_date)
                mywhere.append("end_date=" + end_date)
                mywhere.append("state=" + '')
                data_from = datetime.datetime(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:]), 0, 0)
                data_to = datetime.datetime(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:]), 0, 0)
                burnin_result = list(models.Burnin_Result.object.filter(
                    timestamp__range=(data_from, data_to)).all().values_list('ip', 'disk', 'runtime', 'state',
                                                                             'result', 'timestamp'))
    # state is not null
    else:
        if start_date == null:
            # start_date & end_date is null;state is not null
            if end_date == null:
                mywhere.append("start_date=" + '')
                mywhere.append("end_date=" + '')
                mywhere.append("state=" + state)
                burnin_result = list(models.Burnin_Result.object.filter(state=state).all().values_list('ip', 'disk',
                                                                                                       'runtime',
                                                                                                       'state',
                                                                                                       'result',
                                                                                                       'timestamp'))
            # state & end_date is not null;start_date is null
            else:
                mywhere.append("start_date=" + '')
                mywhere.append("end_date=" + end_date)
                mywhere.append("state=" + state)
                data_to = datetime.datetime(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:]), 0, 0)
                burnin_result = list(models.Burnin_Result.object.filter(timestamp__lte=data_to,
                                                                        state=state).all().values_list('ip', 'disk',
                                                                                                       'runtime',
                                                                                                       'state',
                                                                                                       'result',
                                                                                                       'timestamp'))
        # state & start_date is not null
        else:
            # state & start_date is not null;end_date is null
            if end_date == null:
                mywhere.append("start_date=" + start_date)
                mywhere.append("end_date=" + '')
                mywhere.append("state=" + state)
                data_from = datetime.datetime(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:]), 0,
                                              0)
                burnin_result = list(models.Burnin_Result.object.filter(timestamp__gte=data_from,
                                                                        state=state).all().values_list('ip',
                                                                                                       'disk',
                                                                                                       'runtime',
                                                                                                       'state',
                                                                                                       'result',
                                                                                                       'timestamp'))
            # state & start_date & end_date is not null
            else:
                mywhere.append("start_date=" + start_date)
                mywhere.append("end_date=" + end_date)
                mywhere.append("state=" + state)
                data_from = datetime.datetime(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:]), 0, 0)
                data_to = datetime.datetime(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:]), 0, 0)
                burnin_result = list(models.Burnin_Result.object.filter(timestamp__range=(data_from, data_to),
                                                                        state=state).all().values_list('ip', 'disk',
                                                                                                       'runtime',
                                                                                                       'state',
                                                                                                       'result',
                                                                                                       'timestamp'))

    paginator = Paginator(burnin_result, 15)
    # 判断总数
    if paginator.count == 0:
        total_results_counts = 0
    else:
        total_results_counts = paginator.count
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    for i in mywhere:
        url_add += i
        url_add += '&'

    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    send_burnin_html(request, burnin_result)

    return render(request, 'burnin_result_check.html',
                  {'page': page, "pindex": pindex, "url_add": url_add, "total_results_counts": total_results_counts})


def send_burnin_html(request, burnin_result):
    """
    处理BurnIn结果，发送html样式邮件
    :param request:
    :param burnin_result:
    :return:
    """
    table_message = ''
    result_list = []
    result_counts = 0
    fail_counts = 0
    success_counts = 0
    time_stamp = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    GEN_HTML = time_stamp + '_' + 'result.html'

    """处理查询返回的结果"""
    for i in burnin_result:
        data = []  # 初始化列表，用于接收元组
        result_counts += 1
        for j in i:
            data.append(j)
        result_list.append(data)  # 将data列表加入列表

    if result_list:
        for i in result_list:  # 遍历总列表
            message = """
                                  <tr>
                              <td>%s</td>
                              <td>%s</td>
                              <td>%s</td>
                              <td>%s</td>
                              <td>%s</td>
                              <td>%s</td>
                          </tr>
                                  """ % (
                str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5].strftime('%Y-%m-%d')))
            table_message += message
            if i[3] == "PASS":
                success_counts += 1
            else:
                fail_counts += 1

        head_message = """
                              <html>
                              <head></head>
                              <body>
                              <p>共%s条统计数据，其中成功%s条，失败%s条</p>
                              <table border="1">
                                  <tr>
                                      <th>ip地址</th>
                                      <th>盘符</th>
                                      <th>运行时长</th>
                                      <th>运行状态</th>
                                      <th>运行结果</th>
                                      <th>日期</th>
                                  </tr>
                                                  """ % (result_counts, success_counts, fail_counts)
        foot_message = """
                              </table>
                              </body>
                              </html>"""
        try:
            f = open('report/' + GEN_HTML, 'w')
            f.write(head_message)
            f.write(table_message)
            f.write(foot_message)
            f.close()
        except:
            print('文件创建失败！')

    """发送邮件"""
    try:
        if request.method == "POST":
            burnin_table = head_message + table_message + foot_message
            # 邮件主题
            subject = 'Send email test'
            # 邮件内容
            content = 'Test Report'
            # 发件人
            from_email = 'sibo.guo@tihchip.com'
            # 收件人列表
            to = ['ruanzhe@tihchip.com', 'chunhui.zheng@tihchip.com']
            msg = EmailMultiAlternatives(subject=subject, body=content, from_email=from_email, to=to)
            # 设置为html格式
            msg.content_subtype = 'plain'

            msg.attach_file('report/' + GEN_HTML)
            # 发送邮件
            msg.send()
    except:
        print("邮件发送失败")


def login(request):
    error_msg = ""
    if request.method == "POST":
        account = request.POST.get("account", None)
        pwd = request.POST.get("pwd", None)
        print(account, pwd)
        if account == 'test' and pwd == 'test':
            return redirect("http://192.168.100.122:8000/home/")
        else:
            error_msg = "账号或密码错误"
    return render(request, "login.html", {"error": error_msg})


"""    if request.method == "POST":
        account = request.POST.get('account')
        id_a = request.POST.get('id_a')
        print("id_a: %s" % id_a)
        password = request.POST.get('password')
        name = request.POST.get('name')
        print("name: %s" % name)
        sex = request.POST.get('sex')
        department = request.POST.get('department')
        email = request.POST.get('email')
        remark = request.POST.get('remark')
        user_up = models.Users.objects.filter(name=name).first()
        if user_up:
            print("user_up: %s" % user_up)
            # update(sex=sex, department=department, email=email)
            user_up.account = account
            user_up.password = password
            user_up.sex = sex
            user_up.department = department
            user_up.email = email
            user_up.remark = remark
            user_up.save()
        else:
            # 表示名字写错了或者没这个人
            error_msg = "名字写错了或没有此人"
            return render(request, 'data_display.html', {"error1": error_msg})"""

# def delete_user(request):
#     error_msg = ""
#     if request.method == "POST":
#         delete_u = request.POST.get("delete_u")
#         if delete_u:
#             datas = connect_sql.connect()
#             for data in datas:
#                 if delete_u == list(data)[0]:
#                     # 有一样的就删掉
#                     user_del = models.Users.objects.filter(account=delete_u).delete()    # 这里需要再看下
#                 else:
#                     continue
#             error_msg = "数据库没有这个账号"
#             return render(request, 'delete_user.html', {"error": error_msg})
#         else:
#             error_msg = "输入不能为空"
#             return render(request, 'delete_user.html', {"error": error_msg})
#     return render(request, 'delete_user.html')


# def data_display(request):
#     global field
#     if request.method == "POST":
#         field = request.POST.get('name')
#         if field:
#             datas = connect_sql.connect()
#             for data in datas:
#                 # 表字段的位置是不能存错的
#                 if field == list(data)[3]:
#                     user_info = list(data)[:8]
#                     return render(request, 'data_display.html', {"user_info": user_info})
#                 else:
#                     continue
#                     # return render(request, 'select.html', {"user_info": "没有这个人"})
#         else:
#             return render(request, 'data_display.html', {"user_info": "此人不在数据库或输入有误"})
#         return render(request, 'data_display.html', {"user_info": "此人不在数据库或输入有误"})
#     return render(request, 'data_display.html')
