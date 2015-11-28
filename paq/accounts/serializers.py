# -*- coding: utf-8 -*-

from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from rest_framework import serializers
from djoser.serializers import (
    PasswordSerializer, CurrentPasswordSerializer, UidAndTokenSerializer)

from .models import User
from .validators import validate_password

MIN_PACKAGE_YEAR = 2016
MAX_PACKAGE_YEAR = MIN_PACKAGE_YEAR + 10


def validate_user_password(raw_password):
    try:
        validate_password(raw_password)
    except ValidationError as e:
        raise serializers.ValidationError(e.message)


class UserSerializer(serializers.ModelSerializer):
    '''
    Serializer for user management
    '''

    class Meta:
        model = User
        image_fields = ('images', )
        fields = ('pk', 'email', 'first_name', 'last_name', 'password')
        write_only_fields = ('password', )

    def validate_password(self, data):
        if data:
            validate_user_password(data)
        return data

    def update(self, instance, validated_data):
        '''
        Also set password hash when updating password
        '''
        # Do not update password
        allowed_fields = ['first_name', 'last_name']
        save_instance = False
        for attr, value in validated_data.items():
            # if (value is not None) and (attr in allowed_fields):
            if attr in allowed_fields:
                save_instance = True
                setattr(instance, attr, value)
        # Bug WEBAPP-475: To prevent user-instance signal when ONLY
        # profile-instance in saved.
        if save_instance:
            instance.save()

        update_session_auth_hash(self.context.get('request'), instance)
        return instance


class PasswordRetypeSerializer(PasswordSerializer):
    re_new_password = serializers.CharField()

    default_error_messages = {
        'password_mismatch': 'The two password fields didn\'t match.',
    }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['new_password'] != attrs['re_new_password']:
            raise serializers.ValidationError(self.error_messages['password_mismatch'])
        return attrs

    def validate_new_password(self, data):
        validate_user_password(data)
        return data


class SetPasswordRetypeSerializer(PasswordRetypeSerializer, CurrentPasswordSerializer):
    pass


class PasswordResetConfirmRetypeSerializer(UidAndTokenSerializer, PasswordRetypeSerializer):
    pass


class UserActivationSerializer(UidAndTokenSerializer):
    password = serializers.CharField(allow_blank=True, required=False)
    default_error_messages = {
        'password': 'Please set a password.',
    }

    def validate_password(self, data):
        if data:
            validate_user_password(data)
        elif not self.user.has_usable_password():
            raise serializers.ValidationError(self.error_messages['password'])
        return data
