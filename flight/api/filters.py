from django_filters import FilterSet
from django_filters import NumberFilter, DateTimeFilter

from flight.models import Flight


class CustomFlightFilter(FilterSet):
    lte_depart_datetime = DateTimeFilter(field_name='depart_datetime', lookup_expr='lte')
    gte_depart_datetime = DateTimeFilter(field_name='depart_datetime', lookup_expr='gte')
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Flight
        fields = (
            'from_city',
            'to_city',
            'lte_depart_datetime',
            'gte_depart_datetime',
            'arrive_datetime',
            'min_price',
            'max_price'
        )
