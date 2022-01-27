from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from libs.models import BaseModel

User = get_user_model()


class State(BaseModel):
    name = models.CharField(verbose_name=_('name'), max_length=80)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')
        db_table = 'state'


class City(BaseModel):
    name = models.CharField(verbose_name=_('name'), max_length=80)
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE, verbose_name=_('state'))

    def __str__(self):
        return f'{self.name} - {self.state}'

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        db_table = 'city'


class AirLine(BaseModel):
    name = models.CharField(verbose_name=_('name'), max_length=80)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Air Line')
        verbose_name_plural = _('Air Lines')
        db_table = 'airline'


class Plane(BaseModel):
    name = models.CharField(verbose_name=_('name'), max_length=50)
    airline = models.ForeignKey(AirLine, related_name='planes', on_delete=models.CASCADE, verbose_name=_('air line'))
    capacity = models.PositiveSmallIntegerField(verbose_name=_('capacity'))

    def __str__(self):
        return f'{self.name} - {self.airline} - {self.capacity}'

    class Meta:
        verbose_name = _('Plane')
        verbose_name_plural = _('Planes')
        db_table = 'plane'


class Flight(BaseModel):
    flight_number = models.CharField(max_length=150, verbose_name=_('flight number'))
    plane = models.ForeignKey(Plane, related_name='flights', on_delete=models.CASCADE, verbose_name=_('plane'))
    from_city = models.ForeignKey(
        City,
        related_name='origin_flights',
        on_delete=models.CASCADE,
        verbose_name=_('origin')
    )
    to_city = models.ForeignKey(
        City,
        related_name='destination_flights',
        on_delete=models.CASCADE,
        verbose_name=_('destination')
    )
    depart_datetime = models.DateTimeField(verbose_name=_('depart datetime'))
    arrive_datetime = models.DateTimeField(verbose_name=_('modified time'))
    price = models.IntegerField(verbose_name=_('price'))

    def prototype_create_seats(self):
        for c in range(1, self.plane.capacity + 1):
            FlightSeat.objects.create(flight=self, seat=Seat.objects.create(number=c))

    def available_flight_depart_datetime(self):
        return bool(self.depart_datetime > timezone.now())

    def __str__(self):
        return f'{self.plane} - {self.from_city} - {self.to_city}'

    class Meta:
        verbose_name = _('Flight')
        verbose_name_plural = _('Flights')
        db_table = 'flight'


class Seat(BaseModel):
    number = models.PositiveSmallIntegerField(verbose_name=_('number'))
    is_reserve = models.BooleanField(verbose_name=_('is reserve'), default=False)
    reserved_time = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f'{self.number} - {self.is_reserve}'

    class Meta:
        verbose_name = _('Seat')
        verbose_name_plural = _('Seats')
        db_table = 'seat'


class FlightSeat(BaseModel):
    flight = models.ForeignKey(Flight, related_name='flight_seats', on_delete=models.CASCADE, verbose_name=_('flight'))
    seat = models.ForeignKey(Seat, related_name='flight_seats', on_delete=models.CASCADE, verbose_name=_('seat'))
    customer = models.ForeignKey(
        User,
        related_name='flight_seats',
        on_delete=models.CASCADE,
        verbose_name=_('customer'),
        null=True, blank=True
    )

    def available_flight_seat(self):
        return bool(self.customer is None and not self.seat.is_reserve)

    class Meta:
        verbose_name = _('Flight Seat')
        verbose_name_plural = _('Flight Seats')
        db_table = 'flight_seat'
