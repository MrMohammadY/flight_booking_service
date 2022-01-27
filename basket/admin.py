from django.contrib import admin

from .models import *


class TicketInline(admin.StackedInline):
    model = Ticket
    extra = 0
    can_delete = False
    readonly_fields = ('flight', 'flight_seat', 'first_name', 'last_name', 'national_code', 'birthday')

    def has_add_permission(self, request, obj):
        return False


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_paid', 'created_time', 'modified_time')
    list_filter = ('is_paid',)
    search_fields = ('user__username',)
    readonly_fields = ('user', 'is_paid')
    inlines = (TicketInline,)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'flight', 'cart', 'first_name', 'last_name',
        'national_code', 'birthday', 'created_time', 'modified_time'
    )
    search_fields = ('first_name', 'last_name', 'national_code')
    readonly_fields = ('cart', 'flight', 'flight_seat', 'first_name', 'last_name', 'national_code', 'birthday')
