from django.contrib import admin

from .models import *


@admin.register(AirLine)
class AdminAirLine(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Plane)
class AdminPlane(admin.ModelAdmin):
    list_display = ('name', 'airline', 'capacity')
    list_filter = ('airline',)
    search_fields = ('name', 'airline__name')


@admin.register(Flight)
class AdminFlight(admin.ModelAdmin):
    list_display = ('plane', 'from_city', 'to_city', 'depart_datetime', 'arrive_datetime')
    list_filter = ('from_city', 'to_city')
    search_fields = ('plane', 'from_city__name', 'to_city__name')


@admin.register(Seat)
class AdminSeat(admin.ModelAdmin):
    list_display = ('number', 'is_reserve')
    list_filter = ('is_reserve',)


@admin.register(FlightSeat)
class AdminFlightSeat(admin.ModelAdmin):
    list_display = ('flight', 'seat', 'customer')


@admin.register(State)
class AdminState(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(City)
class AdminCity(admin.ModelAdmin):
    list_display = ('name', 'state')
    search_fields = ('name',)
