# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0003_auto_20151128_1113'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, verbose_name='Description', null=True)),
                ('like_count', models.PositiveSmallIntegerField(blank=True, verbose_name='Number of likes for reply', null=True)),
                ('reply_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_query_name='answer', related_name='answers')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=500, verbose_name='Title', db_index=True)),
                ('description', models.TextField(blank=True, verbose_name='Description', null=True)),
                ('vote_count', models.PositiveSmallIntegerField(blank=True, help_text='Number of vote for post Optional will have.', verbose_name='Number of post', null=True)),
                ('ans_count', models.PositiveSmallIntegerField(blank=True, help_text='Number of reply will have. Optional.', verbose_name='Number of reply', null=True)),
                ('type', models.IntegerField(choices=[(0, 'Private'), (1, 'Public')], default=1)),
                ('has_accepted', models.BooleanField(default=False, db_index=True)),
                ('answers', models.ManyToManyField(blank=True, to='post.Answer', related_name='questions', null=True, related_query_name='question')),
                ('tags', models.ManyToManyField(to='post.Tag', related_name='questions', related_query_name='question')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_query_name='question', related_name='questions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='post',
            name='reply',
        ),
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.RemoveField(
            model_name='reply',
            name='reply_user',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Reply',
        ),
    ]
