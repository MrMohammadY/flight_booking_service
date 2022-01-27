from datetime import datetime

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from basket.models import Ticket
from payment.models import Invoice


@receiver(post_save, sender=Ticket)
def reserve_seat(sender, instance, created, **kwargs):
    if created:
        instance.flight_seat.customer = instance.cart.user
        instance.flight_seat.seat.is_reserve = True
        instance.flight_seat.seat.reserved_time = datetime.now()
        instance.flight_seat.save()
        instance.flight_seat.seat.save()


@receiver(post_delete, sender=Ticket)
def un_reserve_seat(sender, instance, **kwargs):
    instance.flight_seat.customer = None
    instance.flight_seat.seat.is_reserve = False
    instance.flight_seat.seat.reserved_time = None
    instance.flight_seat.save()
    instance.flight_seat.seat.save()


@receiver(post_delete, sender=Ticket)
def delete_invoice_payment(sender, instance, **kwargs):
    if instance.cart.is_empty():
        try:
            instance.cart.invoice.payments.all().delete()
            instance.cart.invoice.delete()
        except Invoice.DoesNotExist:
            pass
    else:
        instance.cart.invoice.create_invoice_payment(instance.cart.user, instance.cart)
