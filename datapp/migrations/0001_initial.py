# Generated by Django 4.2 on 2025-03-12 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('email', models.EmailField(max_length=64, verbose_name='邮箱')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='问卷标题')),
                ('description', models.TextField(blank=True, verbose_name='问卷描述')),
                ('dateceated', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('startdate', models.DateTimeField(blank=True, null=True, verbose_name='开始时间')),
                ('enddate', models.DateTimeField(blank=True, null=True, verbose_name='结束时间')),
                ('status', models.IntegerField(choices=[(0, '已发布'), (1, '已结束')], default=0, verbose_name='问卷状态')),
                ('participationcount', models.IntegerField(default=0, verbose_name='参与人数')),
                ('createby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datapp.user', verbose_name='创建者')),
            ],
            options={
                'verbose_name': '问卷',
                'verbose_name_plural': '问卷',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datesubmitted', models.DateTimeField(auto_now_add=True, verbose_name='提交时间')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datapp.survey', verbose_name='所属问卷')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datapp.user', verbose_name='所属用户')),
            ],
            options={
                'verbose_name': '用户提交',
                'verbose_name_plural': '用户提交',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=256, verbose_name='问题内容')),
                ('type', models.IntegerField(choices=[(0, '单选题'), (1, '多选题'), (2, '文本题')], default=0, verbose_name='问题类型')),
                ('order', models.IntegerField(default=0, verbose_name='选项序号')),
                ('isrequired', models.IntegerField(default=0, verbose_name='是否必答')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datapp.survey', verbose_name='所属问卷')),
            ],
            options={
                'verbose_name': '问题',
                'verbose_name_plural': '问题',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('optiontext', models.CharField(blank=True, max_length=100, null=True, verbose_name='选项内容')),
                ('order', models.IntegerField(default=0, verbose_name='选项序号')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datapp.question', verbose_name='所属问题')),
            ],
            options={
                'verbose_name': '选项',
                'verbose_name_plural': '选项',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answerertext', models.TextField(blank=True, null=True, verbose_name='答案内容')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datapp.question', verbose_name='所属问题')),
                ('response', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='datapp.response', verbose_name='所属用户提交')),
                ('selectedoption', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='datapp.option', verbose_name='所属选项')),
            ],
            options={
                'verbose_name': '回答',
                'verbose_name_plural': '回答',
            },
        ),
    ]
