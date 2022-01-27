from django.db.models.signals import post_save
from django.dispatch import receiver

from flight.models import Flight


@receiver(post_save, sender=Flight)
def create_seats(sender, instance, created, **kwargs):
    if created:
        instance.prototype_create_seats()
