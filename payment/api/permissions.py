from rest_framework.permissions import BasePermission


class PaymentCheck(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.invoice.user != request.user or not obj.is_paid or obj.invoice.is_paid:
            return False
        return True
