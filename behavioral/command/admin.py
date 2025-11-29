from django.contrib import admin

from django.contrib import admin
from command.payments.models import Payment, Subscription


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin interface for Payment model."""
    list_display = ['id', 'customer_email', 'amount', 'currency', 'status', 'payment_date']
    list_filter = ['status', 'currency', 'payment_date']
    search_fields = ['customer_email', 'transaction_id']
    readonly_fields = ['transaction_id', 'payment_date', 'created_at', 'updated_at']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin interface for Subscription model."""
    list_display = ['id', 'customer_email', 'amount', 'currency', 'interval', 'status', 'next_payment_date']
    list_filter = ['status', 'interval', 'currency']
    search_fields = ['customer_email']
    readonly_fields = ['created_at', 'updated_at']
