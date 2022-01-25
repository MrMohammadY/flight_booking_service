from django.urls import path
from flight.api.views import FlightListAPIView

app_name = 'flight'

urlpatterns = [
    path('list/', FlightListAPIView.as_view(), name='flight-list'),
]
