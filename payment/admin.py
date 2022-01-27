from django.contrib import admin

from payment.models import Invoice, Payment


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'cart', 'price', 'is_paid')
    list_filter = ('is_paid',)
    search_fields = ('user__username', 'price')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user', 'invoice', 'price', 'is_paid')
    list_filter = ('is_paid',)
    search_fields = ('user__username', 'price')
