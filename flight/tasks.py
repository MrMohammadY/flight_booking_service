import datetime

from django.utils import timezone

from celery import shared_task

from basket.models import Ticket


@shared_task
def un_reserved_not_paid_seat():
    Ticket.objects.filter(
        flight_seat__seat__is_reserve=True,
        cart__is_paid=False,
        flight_seat__seat__reserved_time__lt=timezone.now() - datetime.timedelta(minutes=5)
    ).delete()
