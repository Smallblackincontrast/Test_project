# Generated by Django 3.0.8 on 2020-09-01 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tih_app', '0004_auto_20200901_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='burnin_result',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='时间戳'),
        ),
    ]