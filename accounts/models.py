from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    """
    AbstractUser has some problems like username not case-sensitive or email not unique,
     we fix problem here and add some custom fields.
    you can read about AbstractUser problems here:
    https://simpleisbetterthancomplex.com/article/2021/07/08/what-you-should-know-about-the-django-user-model.html

    note: we can be case-sensitive username, but we should use postgresql as database
    """
    email = models.EmailField(_('email address'), unique=True)  # we set unique true
    phone_number = models.CharField(
        _('phone number'),
        max_length=12,
        unique=True,
        help_text=_('A phone number should 12 characters like 981234567890'),
        error_messages={
            'unique': _("A user with that phone number already exists."),
        },
    )

    otp = models.PositiveSmallIntegerField(_('otp'))
    otp_expire_time = models.DateTimeField(_('otp expire time'), default=None, null=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'user'
