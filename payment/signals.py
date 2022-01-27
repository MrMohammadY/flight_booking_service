from django.db.models.signals import post_save, post_init
from django.dispatch import receiver

from payment.models import Payment


@receiver(post_save, sender=Payment)
def change_is_paid_invoice_cart(sender, instance, created, **kwargs):
    if not created and instance.is_paid and instance.before_update_is_paid != instance.is_paid:
        instance.invoice.is_paid = True
        instance.invoice.cart.is_paid = True
        instance.invoice.cart.save()
        instance.invoice.save()


@receiver(post_init, sender=Payment)
def store_change_is_paid(sender, instance, **kwargs):
    instance.before_update_is_paid = instance.is_paid
