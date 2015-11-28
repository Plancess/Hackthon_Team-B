# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20151128_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='reply',
            field=models.ManyToManyField(related_query_name='post', null=True, to='post.Reply', related_name='posts', blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='reply_count',
            field=models.PositiveSmallIntegerField(verbose_name='Number of reply', null=True, help_text='Number of reply will have. Optional.', blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='vote_count',
            field=models.PositiveSmallIntegerField(verbose_name='Number of post', null=True, help_text='Number of vote for post Optional will have.', blank=True),
        ),
    ]
