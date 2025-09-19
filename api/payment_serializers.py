from rest_framework import serializers
from .models import PaymentTransaction


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = [
            'id', 'gateway', 'transaction_id', 'amount', 'credits_purchased', 
            'status', 'created_at', 'completed_at', 'gateway_data'
        ]
        read_only_fields = ['id', 'created_at', 'completed_at']


class CreatePaymentSerializer(serializers.Serializer):
    gateway = serializers.ChoiceField(choices=[
        ('khalti', 'Khalti'),
        ('esewa', 'eSewa'),
        ('stripe', 'Stripe'),
        ('razorpay', 'Razorpay'),
        ('binance', 'Binance Pay'),
    ])
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    credits = serializers.IntegerField(min_value=1)
    return_url = serializers.URLField(required=False)


class VerifyPaymentSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(max_length=255)
    gateway_data = serializers.JSONField(required=False)
