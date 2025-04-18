# Generated by Django 2.2 on 2025-03-19 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datapp', '0002_alter_response_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='option',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='question',
            name='isrequired',
            field=models.IntegerField(default=0, verbose_name='Required'),
        ),
        migrations.AlterField(
            model_name='question',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Option Order'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=256, verbose_name='Question Content'),
        ),
        migrations.AlterField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datapp.Survey', verbose_name='Survey'),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.IntegerField(choices=[(0, 'Single Choice'), (1, 'Multiple Choice'), (2, 'Text Question')], default=0, verbose_name='Question Type'),
        ),
        migrations.AlterField(
            model_name='response',
            name='datesubmitted',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Submission Time'),
        ),
        migrations.AlterField(
            model_name='response',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='response',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datapp.Survey', verbose_name='Survey'),
        ),
        migrations.AlterField(
            model_name='response',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='datapp.User', verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='createby',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datapp.User', verbose_name='Creator'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='dateceated',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation Time'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='enddate',
            field=models.DateTimeField(blank=True, null=True, verbose_name='End Time'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='participationcount',
            field=models.IntegerField(default=0, verbose_name='Participation Count'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='startdate',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Start Time'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='status',
            field=models.IntegerField(choices=[(0, 'Published'), (1, 'Ended')], default=0, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
