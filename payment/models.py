import uuid as uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from basket.models import Cart
from libs.models import BaseModel

User = get_user_model()


class Invoice(BaseModel):
    user = models.ForeignKey(User, related_name='invoices', on_delete=models.PROTECT, verbose_name=_('user'))
    cart = models.ForeignKey(Cart, related_name='invoices', on_delete=models.PROTECT, verbose_name=_('cart'))
    price = models.IntegerField(verbose_name=_('price'))
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.is_paid}'

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        db_table = 'invoice'


class Payment(BaseModel):
    uuid = models.CharField(max_length=32, default=uuid.uuid4().hex, unique=True, verbose_name=_('uuid'))
    user = models.ForeignKey(User, related_name='payments', on_delete=models.PROTECT, verbose_name=_('user'))
    invoice = models.ForeignKey(Invoice, related_name='payments', on_delete=models.PROTECT, verbose_name=_('invoice'))
    price = models.IntegerField(verbose_name=_('price'))
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.uuid} - {self.is_paid} - {self.price}'

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        db_table = 'payment'
