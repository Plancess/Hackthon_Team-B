from django.db import models
from utils.mixins import CommonFieldsMixin
from accounts.models import User


class Tag(CommonFieldsMixin):
    title = models.CharField(max_length=500, db_index=True, verbose_name='Title')


class Answer(CommonFieldsMixin):

    _name = 'answer'
    _name_plural = 'answers'

    description = models.TextField(
        null=True, blank=True, verbose_name='Description')
    reply_user = models.ForeignKey(
        User, related_name=_name_plural, related_query_name=_name)
    like_count = models.PositiveSmallIntegerField(
        default=0, verbose_name='Number of likes for reply')


class Question(CommonFieldsMixin):

    _name = 'question'
    _name_plural = 'questions'

    PRIVATE = 0
    PUBLIC = 1
    POST_TYPE_CHOICES = ((
        PRIVATE, 'Private'),
        (PUBLIC, 'Public'),)

    user = models.ForeignKey(
        User, related_name=_name_plural, related_query_name=_name)
    title = models.CharField(
        max_length=500, db_index=True, verbose_name='Title')
    description = models.TextField(
        null=True, blank=True, verbose_name='Description')
    vote_count = models.PositiveSmallIntegerField(
        default=0, verbose_name='Number of post',
        help_text='Number of vote for post Optional will have.')
    ans_count = models.PositiveSmallIntegerField(
        default=0, verbose_name='Number of reply',
        help_text='Number of reply will have. Optional.')

    tags = models.ManyToManyField(
        Tag, related_name=_name_plural, related_query_name=_name)
    type = models.IntegerField(choices=POST_TYPE_CHOICES, default=PUBLIC)
    # Indicates whether the post has accepted answer.
    answers = models.ManyToManyField(
        Answer, related_name=_name_plural, blank=True, null=True, related_query_name=_name)
    has_accepted = models.BooleanField(db_index=True, default=False)
