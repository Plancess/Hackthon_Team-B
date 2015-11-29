# -*- coding: utf-8 -*-
'''
Models specific to user onboarding and user management
'''
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import NotFound


from .validators import validate_name


VALID_EXTRA_FIELDS = ['first_name', 'last_name']


def filter_extra_fields(**extra_fields):
    return {k: extra_fields[k] for k in VALID_EXTRA_FIELDS if k in extra_fields}


class DataMapper:
    DATE = 'date'
    DATETIME = 'datetime'

    # response_key: (db_key, data_type, data_format(s))
    key_mapping = {
        'birthday': ('date_of_birth', 'date', ['%m/%d/%Y', '%Y-%m-%d']),
        'image': ('photo', 'image', [])
    }

    def _convert(self, data, typ, frmt=None):
        if typ == self.DATE or typ == self.DATETIME:
            return datetime.strptime(data, frmt)

    def map_key(self, key, value):
        key_value = None
        if value:
            val = self.key_mapping[key]
            for frmt in val[2]:
                try:
                    key_value = self._convert(value, typ=val[1], frmt=frmt)
                    break
                except ValueError:
                    pass
        return key_value


class UserManager(BaseUserManager):
    use_in_migrations = True
    mapper = DataMapper()

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        '''
        Creates and saves a User with given email and password.
        '''
        email = self.normalize_email(email)
        if not email:
            raise ValueError('Users must have valid email address')
        extra_fields = self._normalize_fields(extra_fields)
        user = self.model(email=email, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

    def _normalize_fields(self, extra_fields):
        for key, value in self.mapper.key_mapping.items():
            if key in extra_fields:
                val = self.mapper.map_key(key, extra_fields.pop(key))
                if val:
                    extra_fields[value[0]] = val
        return extra_fields


class User(AbstractBaseUser, PermissionsMixin):
    '''
    A fully featured custom User model with admin-compliant permissions.
    '''

    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='Email Address',
        help_text='Should be valid email, e.g. john@example.com')
    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='First Name',
        help_text='John',
        validators=[validate_name])
    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Last Name',
        help_text='Doe',
        validators=[validate_name])
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Admin Status',
        help_text='Designates whether the user can log into admin site.')
    is_active = models.BooleanField(
        default=False,
        verbose_name='Active Status',
        help_text='Designates whether this user should be treated as active.')
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name='Date Joined',
        help_text='The date and time when user registered.')
    is_guru = models.BooleanField(
        default=False,
        verbose_name='Active Status',
        help_text='Designates whether this user should be treated as guru or not.')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser


User._meta.get_field('password').blank = True
