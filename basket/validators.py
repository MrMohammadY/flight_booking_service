import re

from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError


def national_code_validation(national_code):
    if not re.match(r'^[0-9]{10}$', national_code):
        raise ValidationError(_('national code is not valid!'))
