# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_auto_20151129_0429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='description',
        ),
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.TextField(null=True, blank=True, verbose_name='Comment Description'),
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.TextField(null=True, blank=True, verbose_name='Question Text'),
        ),
    ]
