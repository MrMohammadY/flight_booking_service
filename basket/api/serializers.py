from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.utils.translation import ugettext_lazy as _

from basket.models import Ticket
from flight.models import Flight, FlightSeat


class TickerCreateSerializer(serializers.ModelSerializer):
    flight = serializers.IntegerField(min_value=1, write_only=True)
    flight_seat = serializers.IntegerField(min_value=1, write_only=True)

    class Meta:
        model = Ticket
        fields = ('flight', 'flight_seat', 'first_name', 'last_name', 'national_code', 'birthday')

    def validate_flight(self, flight):
        try:
            flight = Flight.objects.get(pk=flight)
        except Flight.DoesNotExist:
            raise ValidationError(_('flight does not exists!'))

        if not flight.available_flight_depart_datetime():
            raise ValidationError(_('can\'t select this flight because departed time is near!'))

        return flight

    def validate_flight_seat(self, flight_seat):
        try:
            flight_seat = FlightSeat.objects.get(pk=flight_seat)
        except FlightSeat.DoesNotExist:
            raise ValidationError(_('flight seat does not exists!'))

        if not flight_seat.available_flight_seat():
            raise ValidationError(_('can\'t reserve this flight seat because is reserved!'))

        return flight_seat

