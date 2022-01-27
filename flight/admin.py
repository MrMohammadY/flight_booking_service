from django.contrib import admin

from .models import *


@admin.register(AirLine)
class AirLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


@admin.register(Plane)
class PlaneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'airline', 'capacity')
    list_filter = ('airline',)
    search_fields = ('name', 'airline__name')


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'flight_number', 'plane', 'from_city', 'to_city', 'depart_datetime', 'arrive_datetime')
    list_filter = ('from_city', 'to_city')
    search_fields = ('plane', 'from_city__name', 'to_city__name')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'is_reserve')
    list_filter = ('is_reserve',)


@admin.register(FlightSeat)
class FlightSeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'flight', 'seat', 'customer')


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state')
    search_fields = ('name',)
