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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, verbose_name='Description', null=True)),
                ('vote_count', models.IntegerField(default=0, help_text='Number of vote for post Optional will have.', verbose_name='Number of post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(blank=True, verbose_name='Comment Description', null=True)),
                ('comment_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comments', related_query_name='comment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(db_index=True, max_length=500, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Question Text', null=True)),
                ('type', models.IntegerField(default=1, choices=[(0, 'Private'), (1, 'Public')])),
                ('view_count', models.IntegerField(default=0, help_text='Number of vote for post Optional will have.', verbose_name='Number of post')),
                ('has_accepted', models.BooleanField(default=False, db_index=True)),
                ('vote_count', models.IntegerField(default=0, help_text='Number of vote for post Optional will have.', verbose_name='Number of post')),
                ('answers', models.ManyToManyField(to='post.Answer', blank=True, related_name='questions', related_query_name='question', null=True)),
                ('comment', models.ManyToManyField(to='post.Comment', blank=True, related_name='questions', related_query_name='question', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(db_index=True, max_length=500, verbose_name='Title')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserScore',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('voter_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='votes', related_query_name='vote')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='question',
            name='question_voter',
            field=models.ManyToManyField(related_query_name='question', related_name='questions', to='post.Vote'),
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(related_query_name='question', related_name='questions', to='post.Tag'),
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='questions', related_query_name='question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='comment',
            field=models.ManyToManyField(to='post.Comment', blank=True, related_name='answers', related_query_name='answer', null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='reply_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='answers', related_query_name='answer'),
        ),
    ]
