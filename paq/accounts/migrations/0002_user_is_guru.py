# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_guru',
            field=models.BooleanField(default=False, verbose_name='Active Status', help_text='Designates whether this user should be treated as guru or not.'),
        ),
    ]
