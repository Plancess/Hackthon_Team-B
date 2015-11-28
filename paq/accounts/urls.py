# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework_social_oauth2.views import convert_token
from oauth2_provider.views import AuthorizationView

from .views import (
    UserViewSet, SetPasswordView, PasswordResetConfirmView, PasswordResetView,
    RevokeTokenView, ActivationView, TokenView)


router = DefaultRouter()
router.register(r'users', UserViewSet, 'users')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/authorize/?$', AuthorizationView.as_view(), name="authorize"),
    url(r'^auth/token/?$', TokenView.as_view(), name="token"),
    url(r'^auth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^auth/convert-token/?$', convert_token, name="convert_token"),
    url(r'^auth/revoke-token/?$', RevokeTokenView.as_view(), name="revoke_token"),
    url(r'^users/password/change/$', SetPasswordView.as_view(), name='set_password'),
    url(r'^auth/password/reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^auth/password/reset/confirm/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^auth/activate/$', ActivationView.as_view(), name='account_activate'),
]
