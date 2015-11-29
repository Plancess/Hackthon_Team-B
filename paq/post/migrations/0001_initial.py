# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(verbose_name='Description', blank=True, null=True)),
                ('like_count', models.PositiveSmallIntegerField(default=0, verbose_name='Number of likes for reply')),
                ('reply_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='answers', related_query_name='answer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(verbose_name='Comment Description', blank=True, null=True)),
                ('answer', models.ForeignKey(blank=True, null=True, related_name='comments', to='post.Answer', related_query_name='comment')),
                ('comment_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comments', related_query_name='comment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=500, db_index=True, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Question Text', blank=True, null=True)),
                ('type', models.IntegerField(default=1, choices=[(0, 'Private'), (1, 'Public')])),
                ('has_accepted', models.BooleanField(default=False, db_index=True)),
                ('answers', models.ManyToManyField(to='post.Answer', blank=True, related_query_name='question', null=True, related_name='questions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=500, db_index=True, verbose_name='Title')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserScore',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('score', models.IntegerField(default=0, verbose_name='User Score')),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('vote_count', models.IntegerField(default=0, verbose_name='Number of post', help_text='Number of vote for post Optional will have.')),
                ('voter_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='votes', related_query_name='vote')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='post.Tag', related_query_name='question', related_name='questions'),
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='questions', related_query_name='question'),
        ),
        migrations.AddField(
            model_name='question',
            name='vote',
            field=models.ManyToManyField(to='post.Vote', related_query_name='question', related_name='questions'),
        ),
        migrations.AddField(
            model_name='comment',
            name='question',
            field=models.ForeignKey(blank=True, null=True, related_name='comments', to='post.Question', related_query_name='comment'),
        ),
    ]
