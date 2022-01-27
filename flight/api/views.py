import django_filters
from rest_framework import filters
from rest_framework.generics import ListAPIView

from flight.api.filters import CustomFlightFilter
from flight.api.serializers import FlightSerializer
from flight.models import Flight


class FlightListAPIView(ListAPIView):
    """
    Return list of flights with:
    - filtering
    - ordering
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = CustomFlightFilter
    ordering_fields = ('depart_datetime', 'arrive_datetime', 'price')
