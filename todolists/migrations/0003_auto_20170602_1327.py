# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-02 10:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todolists', '0002_auto_20170529_1241'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='tasklist',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='todolists.Tasklist'),
            preserve_default=False,
        ),
    ]
