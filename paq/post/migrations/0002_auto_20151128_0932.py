# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=500, db_index=True, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('vote_count', models.PositiveSmallIntegerField(blank=True, help_text='Number of vote for post Optional will have.', db_index=True, null=True, verbose_name='Number of post')),
                ('reply_count', models.PositiveSmallIntegerField(blank=True, help_text='Number of reply will have. Optional.', db_index=True, null=True, verbose_name='Number of reply')),
                ('type', models.IntegerField(choices=[(0, 'Private'), (1, 'Public')], default=1)),
                ('has_accepted', models.BooleanField(db_index=True, default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('like_count', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Number of likes for reply')),
                ('reply_user', models.ForeignKey(related_name='replies', related_query_name='reply', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='post',
            name='reply',
            field=models.ManyToManyField(related_query_name='post', to='post.Reply', related_name='posts'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_query_name='post', to='post.Tag', related_name='posts'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(related_name='posts', related_query_name='post', to=settings.AUTH_USER_MODEL),
        ),
    ]
