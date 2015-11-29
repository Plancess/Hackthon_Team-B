from django.db import models
from utils.mixins import CommonFieldsMixin
from accounts.models import User


class Tag(CommonFieldsMixin):
    title = models.CharField(
        max_length=500, db_index=True, verbose_name='Title')


class Vote(CommonFieldsMixin):
    """
        Vote per user
    """
    _name = 'vote'
    _name_plural = 'votes'

    voter_user = models.ForeignKey(
        User, related_name=_name_plural, related_query_name=_name)
    vote_count = models.IntegerField(
        default=0, verbose_name='Number of post',
        help_text='Number of vote for post Optional will have.')


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
    vote = models.ManyToManyField(
        Vote, related_name=_name_plural, related_query_name=_name)
    tags = models.ManyToManyField(
        Tag, related_name=_name_plural, related_query_name=_name)
    type = models.IntegerField(choices=POST_TYPE_CHOICES, default=PUBLIC)
    # Indicates whether the post has accepted answer.
    answers = models.ManyToManyField(
        Answer, related_name=_name_plural, blank=True, null=True,
        related_query_name=_name)
    has_accepted = models.BooleanField(db_index=True, default=False)


class Comment(CommonFieldsMixin):
    _name = 'comment'
    _name_plural = 'comments'

    comment_user = models.ForeignKey(
        User, related_name=_name_plural, related_query_name=_name)
    question = models.ForeignKey(
        Question, blank=True, null=True, related_name=_name_plural,
        related_query_name=_name)
    answer = models.ForeignKey(
        Answer, blank=True, null=True, related_name=_name_plural,
        related_query_name=_name)
    description = models.TextField(
        null=True, blank=True, verbose_name='Description')


class UserScore(CommonFieldsMixin):
    _name = 'userscore'
    _name_plural = 'userscores'

    user = models.ForeignKey(
        User, related_name=_name_plural, related_query_name=_name)
    score = models.IntegerField(
        default=0, verbose_name='User Score')
    num_question = models.IntegerField(default=0)
    num_answer = models.IntegerField(default=0)
    num_vote = models.IntegerField(default=0)
    num_comments = models.IntegerField(default=0)
