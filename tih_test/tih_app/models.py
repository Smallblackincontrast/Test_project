from django.db import models


# Create your models here.


class Users(models.Model):
    account = models.CharField(max_length=32, blank=False, verbose_name="用户名")
    password = models.CharField(max_length=32, blank=False, verbose_name="密码")
    name = models.CharField(max_length=32, blank=False, verbose_name="名字")
    sex = models.CharField(max_length=32, blank=True, verbose_name="性别")
    department = models.CharField(max_length=32, blank=True, verbose_name="部门")
    email = models.CharField(max_length=32, blank=True, verbose_name="邮箱")
    remark = models.CharField(max_length=32, blank=True, verbose_name="评分", default=0.0)
    objects = models.Manager()


class Burnin_Result(models.Model):
    ip = models.CharField(max_length=32, blank=False, verbose_name='ip地址')
    disk = models.CharField(max_length=32, blank=False, verbose_name='盘符')
    runtime = models.CharField(max_length=32, blank=False, verbose_name='运行时长')
    state = models.CharField(max_length=32, blank=False, verbose_name='运行状态')
    result = models.CharField(max_length=128, blank=False, verbose_name='运行结果')
    timestamp = models.DateTimeField(verbose_name='时间戳', auto_now_add=True)
    object = models.Manager()
