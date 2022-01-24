from django.contrib import admin

from .models import *


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'is_paid')
    list_filter = ('is_paid',)
    search_fields = ('user__username',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'flight__flight_number', 'flight__from_city', 'flight__to_city',
        'cart', 'first_name', 'last_name', 'national_code', 'birthday'
    )
    list_filter = ('flight__from_city', 'flight__to_city')
