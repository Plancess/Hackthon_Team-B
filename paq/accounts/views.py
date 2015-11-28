# -*- coding: utf-8 -*-
'''
Basic view for user
'''
from datetime import date
from io import BytesIO

from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from djoser import settings as djoser_settings, signals, serializers
from djoser.views import PasswordResetView as BasePasswordResetView
from djoser.utils import ActionViewMixin, SendEmailViewMixin
from oauth2_provider.views import RevokeTokenView as BaseRevokeTokenView, TokenView as BaseTokenView
from rest_framework.decorators import list_route
from rest_framework import generics, permissions, viewsets, status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError, NotFound, ValidationError as RestFrameworkValidationError
from rest_framework.response import Response


from .models import User
from .serializers import (
    UserSerializer, SetPasswordRetypeSerializer, PasswordResetConfirmRetypeSerializer,
    UserActivationSerializer,)


class UserViewSet(SendEmailViewMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    '''
    Create/(partial)Update/Delete users
    '''
    # lookup_field = 'email'
    serializer_class = UserSerializer
    token_generator = default_token_generator
    subject_template_name = 'email/activation_email_subject.txt'
    html_body_template_name = 'email/activation_email_body.txt'

    def get_queryset(self):
        return User.objects.all()

    def post_save(self, obj, created=False):
        if djoser_settings.get('LOGIN_AFTER_REGISTRATION'):
            Token.objects.get_or_create(user=obj)
        if djoser_settings.get('SEND_ACTIVATION_EMAIL'):
            context = self.get_send_email_kwargs(obj).get('context', {})
            context['first_name'] = obj.first_name

    def create(self, request, *args, **kwargs):
        '''
        Register new user.
        '''
        # Taking full name from front end splitting it into first name and last name at backend.
        if request.data.get('full_name'):
            first_name, last_name = request.data.get('full_name').split(' ', 1)
            request.data['first_name'] = first_name
            request.data['last_name'] = last_name

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.create_user(**serializer.validated_data)
            except ValidationError as e:
                return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)

            signals.user_registered.send(
                sender=self.__class__, user=user, request=self.request)
            self.post_save(obj=user, created=True)

            return Response({
                'user_id': user.id,
                'email': serializer.validated_data['email'],
                'status': 'Success',
                'message': 'Account created successfully'
            }, status=status.HTTP_201_CREATED)

        existing_user = User.objects.filter(email=request.data.get('email', None)).first()
        # sending user_id if user has already signed up.
        data = {'error': serializer.errors,
                'user_id': existing_user.id if existing_user else None,
                }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    # LoggedIn User's profile info without Id, needed for frontend.
    @list_route(methods=['get'], url_path='details')
    def user_details(self, request):
        '''
        User's (unread)notifications.
        This holds ALL notifications
        '''
        user = User.objects.get(pk=request.user.id)
        if user:
            # Adding User Photos to response
            return Response({
                'user_id': user.id,
                'email': user.email,
            }, status=status.HTTP_200_OK)
        raise NotFound("user with user id {0} does not exist.".format(request.user.id))


class SetPasswordView(ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to change user password.
    """
    serializer_class = SetPasswordRetypeSerializer

    def action(self, serializer):
        self.request.user.set_password(serializer.data['new_password'])
        self.request.user.save()
        data = {
            'title': None,
            '_id': None,
            'description': 'Your password has been changed successfuly'
        }
        return Response(status=status.HTTP_200_OK)


class PasswordResetConfirmView(ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to finish reset password process.
    """
    permission_classes = (
        permissions.AllowAny,
    )
    token_generator = default_token_generator
    serializer_class = PasswordResetConfirmRetypeSerializer

    def action(self, serializer):
        serializer.user.set_password(serializer.data['new_password'])
        serializer.user.save()
        return Response(status=status.HTTP_200_OK)


class RevokeTokenView(BaseRevokeTokenView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            response['Content-Type'] = 'application/json'
            response.content = "{\"message\": \"Token destroyed successfully\"}"
        return response


class TokenView(BaseTokenView):

    @method_decorator(sensitive_post_parameters('password'))
    def post(self, request, *args, **kwargs):
        import ipdb
        ipdb.set_trace()
        response = super().post(request, *args, **kwargs)
        if request.POST['grant_type'] == 'password':
            try:
                user = User.objects.get(email=request.POST['username'])
            except User.DoesNotExist:
                # raise NotFound('user does not exist')
                user = None
            if user and not user.is_active:
                response.content = "{\"message\" : \"User is inactive \"}"
        return response


class ActivationView(SendEmailViewMixin, ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to activate user account.
    """
    serializer_class = UserActivationSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    token_generator = default_token_generator
    subject_template_name = 'email/welcome_email_subject.txt'
    html_body_template_name = 'email/welcome_email_body.txt'

    def get_email_context(self, user):
        context = super(ActivationView, self).get_email_context(user)
        context['first_name'] = user.first_name
        return context

    def action(self, serializer):
        if serializer.user.is_active:
            raise ParseError('This token has already been used')
        serializer.user.is_active = True
        if serializer.validated_data.get('password', None):
            serializer.user.set_password(serializer.validated_data['password'])
        serializer.user.save()
        signals.user_activated.send(
            sender=self.__class__, user=serializer.user, request=self.request)
        if djoser_settings.get('LOGIN_AFTER_ACTIVATION'):
            token, _ = Token.objects.get_or_create(user=serializer.user)
            data = serializers.TokenSerializer(token).data
        else:
            data = {}

        return Response(data=data, status=status.HTTP_200_OK)


class PasswordResetView(BasePasswordResetView):
    """
    Use this endpoint to send email to user with password reset link.
    """

    def action(self, serializer):
        for user in self.get_users(serializer.data['email']):
            context = self.get_email_context(user)
            # ResetPasswordEmailNotification(user.email, context={'context': context, 'first_name': user.first_name}).send()
        return Response(status=status.HTTP_200_OK)

    def get_email_context(self, user):
        context = super().get_email_context(user)
        context['url'] = djoser_settings.get('PASSWORD_RESET_CONFIRM_URL').format(**context)
        return context
