"""
DRF Serializers for Payment System API.
"""

from rest_framework import serializers
from command.payments.models.payment import Payment
from command.payments.models.subscription import Subscription


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model."""
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'amount',
            'currency',
            'status',
            'transaction_id',
            'payment_date',
            'customer_email',
            'subscription',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'status',
            'transaction_id',
            'payment_date',
            'created_at',
            'updated_at'
        ]


class ProcessPaymentSerializer(serializers.Serializer):
    """Serializer for processing a single payment."""
    
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        help_text="Payment amount"
    )
    currency = serializers.CharField(
        max_length=3,
        default='USD',
        help_text="Currency code (ISO 4217)"
    )
    customer_email = serializers.EmailField(
        help_text="Customer's email address"
    )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for Subscription model."""
    
    payments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Subscription
        fields = [
            'id',
            'customer_email',
            'amount',
            'currency',
            'interval',
            'status',
            'next_payment_date',
            'start_date',
            'created_at',
            'updated_at',
            'payments_count'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'payments_count'
        ]
    
    def get_payments_count(self, obj):
        """Get the count of payments for this subscription."""
        return obj.payments.count()


class CreateSubscriptionSerializer(serializers.Serializer):
    """Serializer for creating a new subscription."""
    
    customer_email = serializers.EmailField(
        help_text="Customer's email address"
    )
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        help_text="Recurring payment amount"
    )
    currency = serializers.CharField(
        max_length=3,
        default='USD',
        help_text="Currency code (ISO 4217)"
    )
    interval = serializers.ChoiceField(
        choices=Subscription.Interval.choices,
        default=Subscription.Interval.MONTHLY,
        help_text="Billing interval"
    )
    next_payment_date = serializers.DateTimeField(
        required=False,
        help_text="Date when first payment is due (defaults to now)"
    )
