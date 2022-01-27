from rest_framework import serializers

from payment.models import Payment


class PaymentVerifySerializer(serializers.ModelSerializer):
    is_paid = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = Payment
        fields = ('is_paid',)

    def update(self, instance, validated_data):
        if validated_data.get('is_paid'):
            instance.is_paid = True
            instance.save()
        return instance
