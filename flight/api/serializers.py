from rest_framework import serializers

from flight.models import Plane, AirLine, Flight, Seat, FlightSeat, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('name',)


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ('number', 'is_reserve')


class FlightSeatSerializer(serializers.ModelSerializer):
    seat = SeatSerializer()

    class Meta:
        model = FlightSeat
        fields = ('seat',)


class AirLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirLine
        fields = ('name',)


class PlaneSerializer(serializers.ModelSerializer):
    airline = AirLineSerializer()

    class Meta:
        model = Plane
        fields = ('name', 'airline', 'capacity')


class FlightSerializer(serializers.ModelSerializer):
    plane = PlaneSerializer()
    flight_seats = FlightSeatSerializer(many=True)
    from_city = CitySerializer()
    to_city = CitySerializer()

    class Meta:
        model = Flight
        fields = ('flight_number', 'plane', 'from_city', 'to_city',
                  'depart_datetime', 'arrive_datetime', 'flight_seats')
