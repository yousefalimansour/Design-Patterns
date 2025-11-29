"""
Payment model for storing individual payment transactions.
"""

from django.db import models
from django.utils import timezone


class Payment(models.Model):
    """
    Represents a single payment transaction in the system.
    
    Attributes:
        amount: Payment amount
        currency: Currency code (e.g., USD, EUR)
        status: Current status of the payment
        transaction_id: Unique transaction identifier from payment gateway
        payment_date: Date and time when payment was processed
        customer_email: Email of the customer making the payment
        subscription: Optional reference to subscription if this is a recurring payment
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
    """
    
    class Status(models.TextChoices):
        """Payment status choices."""
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Payment amount"
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        help_text="Currency code (ISO 4217)"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        help_text="Current payment status"
    )
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        help_text="Unique transaction ID from payment gateway"
    )
    payment_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date and time when payment was processed"
    )
    customer_email = models.EmailField(
        help_text="Customer's email address"
    )
    subscription = models.ForeignKey(
        'Subscription',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        help_text="Associated subscription for recurring payments"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when record was last updated"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
    
    def __str__(self):
        return f"Payment {self.id} - {self.customer_email} - {self.amount} {self.currency} - {self.status}"
    
    def mark_completed(self, transaction_id: str) -> None:
        """
        Mark payment as completed.
        
        Args:
            transaction_id: Transaction ID from payment gateway
        """
        self.status = self.Status.COMPLETED
        self.transaction_id = transaction_id
        self.payment_date = timezone.now()
        self.save()
    
    def mark_failed(self) -> None:
        """Mark payment as failed."""
        self.status = self.Status.FAILED
        self.save()
    
    def mark_refunded(self) -> None:
        """Mark payment as refunded."""
        self.status = self.Status.REFUNDED
        self.save()
