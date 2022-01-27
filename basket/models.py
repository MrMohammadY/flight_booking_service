from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from flight.models import Flight, FlightSeat
from libs.models import BaseModel

User = get_user_model()


class Cart(BaseModel):
    user = models.ForeignKey(User, related_name='carts', on_delete=models.PROTECT, verbose_name=_('user'))
    is_paid = models.BooleanField(default=False, verbose_name=_('is paid'))

    def __str__(self):
        return f'{self.user.username} - {self.is_paid}'

    def is_empty(self):
        return True if self.tickets.count() == 0 else False

    @classmethod
    def get_or_created_cart(cls, user):
        cart, created = cls.objects.get_or_create(user=user, is_paid=False)
        return cart

    def calculate_cart_price(self):
        return self.tickets.aggregate(total_price=Sum('flight__price')).get('total_price')

    def cart_is_empty(self):
        return True if self.tickets.count() == 0 else False

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        db_table = 'cart'


class Ticket(BaseModel):
    flight = models.ForeignKey(Flight, related_name='tickets', on_delete=models.CASCADE, verbose_name=_('flight'))
    flight_seat = models.OneToOneField(
        FlightSeat,
        related_name='ticket',
        on_delete=models.CASCADE,
        verbose_name=_('flight seat')
    )
    cart = models.ForeignKey(Cart, related_name='tickets', on_delete=models.CASCADE, verbose_name=_('cart'))
    first_name = models.CharField(max_length=50, verbose_name=_('first name'))
    last_name = models.CharField(max_length=60, verbose_name=_('last name'))
    national_code = models.CharField(max_length=10, verbose_name=_('national code'))
    birthday = models.DateField(verbose_name=_('birthday'))

    def __str__(self):
        return f'{self.flight} - {self.cart.user.username} - {self.national_code}'

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        db_table = 'ticket'
