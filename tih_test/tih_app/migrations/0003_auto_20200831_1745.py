# Generated by Django 3.0.8 on 2020-08-31 09:45

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('tih_app', '0002_burnin_result'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='burnin_result',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='burnin_result',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='时间戳'),
        ),
    ]
