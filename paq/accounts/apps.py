# -*- coding: utf-8 -*-

from django.apps import AppConfig


class UserMgmtConfig(AppConfig):
    name = 'accounts'
    verbose_name = "User Management"

    def ready(self):
        super().ready()
