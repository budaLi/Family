# Generated by Django 2.1.5 on 2019-01-19 11:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='F_Admin',
            fields=[
                ('uniqueid', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('pwd', models.CharField(max_length=20, verbose_name='密码')),
                ('ip', models.CharField(max_length=100, verbose_name='ip')),
                ('register_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='注册时间')),
            ],
            options={
                'verbose_name': '管理员信息',
            },
        ),
        migrations.CreateModel(
            name='F_Admin_Oplog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=200, verbose_name='操作原因')),
                ('optime', models.DateTimeField(default=datetime.datetime.now, verbose_name='操作时间')),
                ('op_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.F_Admin')),
            ],
            options={
                'verbose_name': '管理员操作日志',
            },
        ),
        migrations.CreateModel(
            name='F_AdminLoginlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=20, verbose_name='登陆IP')),
                ('logintime', models.DateTimeField(default=datetime.datetime.now, verbose_name='登陆时间')),
                ('login_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.F_Admin')),
            ],
            options={
                'verbose_name': '管理员登陆日志',
            },
        ),
        migrations.CreateModel(
            name='F_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniqueid', models.CharField(max_length=200, unique=True, verbose_name='唯一ID')),
                ('name', models.CharField(max_length=50, verbose_name='真实姓名')),
                ('nickname', models.CharField(max_length=50, verbose_name='昵称')),
                ('xingshi', models.CharField(default=models.CharField(max_length=50, verbose_name='真实姓名'), max_length=20, verbose_name='姓氏')),
                ('pwd', models.CharField(max_length=20, verbose_name='密码')),
                ('sex', models.CharField(choices=[('0', '男'), ('1', '女'), ('3', '不详')], default='男', max_length=20, verbose_name='性别')),
                ('birthday', models.DateField(max_length=20, verbose_name='出生日期')),
                ('phone', models.CharField(max_length=20, verbose_name='手机号码')),
                ('email', models.CharField(max_length=30, verbose_name='邮箱')),
                ('image', models.CharField(default='', max_length=200, verbose_name='头像')),
                ('jiguan', models.CharField(max_length=200, verbose_name='籍贯')),
                ('register_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='注册时间')),
                ('info', models.TextField(verbose_name='个人介绍')),
            ],
            options={
                'verbose_name': '用户信息',
            },
        ),
        migrations.CreateModel(
            name='F_UserOptionlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('op_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='操作时间')),
                ('reason', models.CharField(max_length=200, verbose_name='事件')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.F_User')),
            ],
        ),
        migrations.CreateModel(
            name='F_Userphote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_path', models.CharField(max_length=200, verbose_name='图片地址')),
                ('photo_info', models.CharField(max_length=200, verbose_name='图片介绍')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('vedio_path', models.CharField(max_length=200, verbose_name='视频地址')),
                ('vedio_info', models.CharField(max_length=200, verbose_name='视频介绍')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.F_User')),
            ],
            options={
                'verbose_name': '个人信息墙',
            },
        ),
        migrations.CreateModel(
            name='F_UserRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other_user', models.IntegerField(verbose_name='个人')),
                ('relation', models.CharField(max_length=20, verbose_name='关系')),
                ('story', models.TextField(verbose_name='两者之间事件')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='增加时间')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.F_User')),
            ],
            options={
                'verbose_name': '关系',
            },
        ),
    ]
