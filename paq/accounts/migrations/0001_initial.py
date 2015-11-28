# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import accounts.models
import re
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password', blank=True)),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email Address', help_text='Should be valid email, e.g. john@example.com')),
                ('first_name', models.CharField(max_length=30, help_text='John', validators=[django.core.validators.RegexValidator(regex=re.compile("^[a-zA-Z][a-zA-Z-' ]*$", 32), message="Enter a valid name consisting of letters and spaces, which starts and ends with a letter or '", code='Invalid')], verbose_name='First Name', blank=True)),
                ('last_name', models.CharField(max_length=30, help_text='Doe', validators=[django.core.validators.RegexValidator(regex=re.compile("^[a-zA-Z][a-zA-Z-' ]*$", 32), message="Enter a valid name consisting of letters and spaces, which starts and ends with a letter or '", code='Invalid')], verbose_name='Last Name', blank=True)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into admin site.', verbose_name='Admin Status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active.', verbose_name='Active Status', default=False)),
                ('date_joined', models.DateTimeField(help_text='The date and time when user registered.', verbose_name='Date Joined', default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(verbose_name='groups', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', blank=True, to='auth.Group')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', related_name='user_set', help_text='Specific permissions for this user.', related_query_name='user', blank=True, to='auth.Permission')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
    ]
