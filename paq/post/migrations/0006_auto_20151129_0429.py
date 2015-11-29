# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0005_auto_20151128_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(verbose_name='Description', blank=True, null=True)),
                ('answer', models.ForeignKey(to='post.Answer', null=True, related_name='comments', blank=True, related_query_name='comment')),
                ('comment_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comments', related_query_name='comment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('score', models.IntegerField(verbose_name='User Score', default=0)),
                ('num_question', models.IntegerField(default=0)),
                ('num_answer', models.IntegerField(default=0)),
                ('num_vote', models.IntegerField(default=0)),
                ('num_comments', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='userscores', related_query_name='userscore')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('vote_count', models.IntegerField(verbose_name='Number of post', default=0, help_text='Number of vote for post Optional will have.')),
                ('voter_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='votes', related_query_name='vote')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='question',
            name='ans_count',
        ),
        migrations.RemoveField(
            model_name='question',
            name='vote_count',
        ),
        migrations.AddField(
            model_name='comment',
            name='question',
            field=models.ForeignKey(to='post.Question', null=True, related_name='comments', blank=True, related_query_name='comment'),
        ),
        migrations.AddField(
            model_name='question',
            name='vote',
            field=models.ManyToManyField(to='post.Vote', related_query_name='question', related_name='questions'),
        ),
    ]
