# -*- coding: utf-8 -*-

import re
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

phone_re = re.compile(r'^[7-9]\d{9}$')
# password_re = re.compile(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&^])[A-Za-z\d@$!%*?&^]{8,16}$')
password_re = re.compile(r'^.{6,}$')
name_re = re.compile(r"^[a-zA-Z][a-zA-Z-' ]*$")


validate_phone = RegexValidator(
    regex=phone_re, code='Invalid phone number',
    message='Must be 10 digit number. Must start with 7, 8 or 9.')

validate_password = RegexValidator(
    regex=password_re, code='Invalid Password',
    message='Must be at least 6 or more characters.')

validate_name = RegexValidator(
    regex=name_re, code='Invalid',
    message='Enter a valid name consisting of letters and spaces, which starts and ends with a letter or \'')
