import uuid as uuid
from django.contrib.auth import get_user_model
from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _

from basket.models import Cart
from libs.models import BaseModel

User = get_user_model()


class Invoice(BaseModel):
    user = models.ForeignKey(User, related_name='invoices', on_delete=models.PROTECT, verbose_name=_('user'))
    cart = models.OneToOneField(Cart, related_name='invoice', on_delete=models.PROTECT, verbose_name=_('cart'))
    price = models.IntegerField(verbose_name=_('price'))
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.is_paid}'

    @classmethod
    def create_invoice_payment(cls, user, cart):
        invoice, created = cls.objects.update_or_create(
            user=user,
            cart=cart,
            defaults={'price': cart.calculate_cart_price()}
        )
        payment = Payment.create_payment(invoice)
        return invoice, payment

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        db_table = 'invoice'


class Payment(BaseModel):
    uuid = models.CharField(max_length=50, default=uuid.uuid4, unique=True, verbose_name=_('uuid'))
    user = models.ForeignKey(User, related_name='payments', on_delete=models.PROTECT, verbose_name=_('user'))
    invoice = models.ForeignKey(Invoice, related_name='payments', on_delete=models.PROTECT, verbose_name=_('invoice'))
    price = models.IntegerField(verbose_name=_('price'))
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.uuid} - {self.is_paid} - {self.price}'

    @classmethod
    def create_payment(cls, invoice):
        return cls.objects.create(user=invoice.user, invoice=invoice, price=invoice.price)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        db_table = 'payment'
