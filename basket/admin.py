from django.contrib import admin

from .models import *


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_paid')
    list_filter = ('is_paid',)
    search_fields = ('user__username',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('flight', 'cart', 'first_name', 'last_name', 'national_code', 'birthday')
    search_fields = ('first_name', 'last_name', 'national_code')
