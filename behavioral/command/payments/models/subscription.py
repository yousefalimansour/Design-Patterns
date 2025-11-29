"""
Subscription model for managing recurring payments.
"""

from django.db import models
from django.utils import timezone
from datetime import timedelta


class Subscription(models.Model):
    """
    Represents a recurring payment subscription.
    
    Attributes:
        customer_email: Email of the subscribing customer
        amount: Recurring payment amount
        currency: Currency code
        interval: Billing interval (daily, weekly, monthly, yearly)
        status: Current subscription status
        next_payment_date: Date when next payment is due
        start_date: Date when subscription started
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
    """
    
    class Interval(models.TextChoices):
        """Subscription billing interval choices."""
        DAILY = 'DAILY', 'Daily'
        WEEKLY = 'WEEKLY', 'Weekly'
        MONTHLY = 'MONTHLY', 'Monthly'
        YEARLY = 'YEARLY', 'Yearly'
    
    class Status(models.TextChoices):
        """Subscription status choices."""
        ACTIVE = 'ACTIVE', 'Active'
        PAUSED = 'PAUSED', 'Paused'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    customer_email = models.EmailField(
        help_text="Customer's email address"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Recurring payment amount"
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        help_text="Currency code (ISO 4217)"
    )
    interval = models.CharField(
        max_length=20,
        choices=Interval.choices,
        default=Interval.MONTHLY,
        help_text="Billing interval"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        help_text="Current subscription status"
    )
    next_payment_date = models.DateTimeField(
        help_text="Date when next payment is due"
    )
    start_date = models.DateTimeField(
        default=timezone.now,
        help_text="Date when subscription started"
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
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
    
    def __str__(self):
        return f"Subscription {self.id} - {self.customer_email} - {self.amount} {self.currency} {self.interval} - {self.status}"
    
    def is_payment_due(self) -> bool:
        """
        Check if payment is due for this subscription.
        
        Returns:
            bool: True if payment is due, False otherwise
        """
        return (
            self.status == self.Status.ACTIVE
            and self.next_payment_date <= timezone.now()
        )
    
    def advance_next_payment_date(self) -> None:
        """
        Advance the next payment date based on the billing interval.
        """
        if self.interval == self.Interval.DAILY:
            self.next_payment_date += timedelta(days=1)
        elif self.interval == self.Interval.WEEKLY:
            self.next_payment_date += timedelta(weeks=1)
        elif self.interval == self.Interval.MONTHLY:
            # Approximate monthly as 30 days
            self.next_payment_date += timedelta(days=30)
        elif self.interval == self.Interval.YEARLY:
            # Approximate yearly as 365 days
            self.next_payment_date += timedelta(days=365)
        
        self.save()
    
    def pause(self) -> None:
        """Pause the subscription."""
        self.status = self.Status.PAUSED
        self.save()
    
    def resume(self) -> None:
        """Resume a paused subscription."""
        self.status = self.Status.ACTIVE
        self.save()
    
    def cancel(self) -> None:
        """Cancel the subscription."""
        self.status = self.Status.CANCELLED
        self.save()
