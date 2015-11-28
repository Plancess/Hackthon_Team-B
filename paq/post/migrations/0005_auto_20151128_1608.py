# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20151128_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='like_count',
            field=models.PositiveSmallIntegerField(verbose_name='Number of likes for reply', default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='ans_count',
            field=models.PositiveSmallIntegerField(help_text='Number of reply will have. Optional.', verbose_name='Number of reply', default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='vote_count',
            field=models.PositiveSmallIntegerField(help_text='Number of vote for post Optional will have.', verbose_name='Number of post', default=0),
        ),
    ]
