import re

from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError


def phone_number_validation(phone_number):
    if not re.match(r'^(98)+?9\d{9}$', phone_number):
        raise ValidationError(_('phone number is not valid\nphone number must like 981234567890'))
