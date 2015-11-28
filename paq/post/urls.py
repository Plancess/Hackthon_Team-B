# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import TagCreateView, QuestionCreateView, AnswerCreateView


router = DefaultRouter()

urlpatterns = [
    url(r'^question/$', QuestionCreateView.as_view(), name='posts'),
    url(r'^tags/$', TagCreateView.as_view(), name='tags'),
    url(r'^answer/$', AnswerCreateView.as_view(), name='answers'),
    url(r'^question/(?P<question_id>[0-9]+)/$', QuestionCreateView.as_view(), name='question_answers'),
]
