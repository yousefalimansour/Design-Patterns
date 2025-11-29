"""
Unit tests for RecurringPaymentScheduler service.
"""

from django.test import TestCase
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from command.payments.models.payment import Payment
from command.payments.models.subscription import Subscription
from command.payments.services.scheduler import RecurringPaymentScheduler
from command.payments.gateways.mock_gateway import MockPaymentGateway


class RecurringPaymentSchedulerTestCase(TestCase):
    """Test cases for RecurringPaymentScheduler."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.gateway = MockPaymentGateway(success_rate=1.0)
        self.scheduler = RecurringPaymentScheduler(payment_gateway=self.gateway)
        
        # Create multiple subscriptions
        self.due_subscription_1 = Subscription.objects.create(
            customer_email='due1@example.com',
            amount=Decimal('29.99'),
            currency='USD',
            interval=Subscription.Interval.MONTHLY,
            status=Subscription.Status.ACTIVE,
            next_payment_date=timezone.now() - timedelta(days=1)
        )
        
        self.due_subscription_2 = Subscription.objects.create(
            customer_email='due2@example.com',
            amount=Decimal('49.99'),
            currency='USD',
            interval=Subscription.Interval.WEEKLY,
            status=Subscription.Status.ACTIVE,
            next_payment_date=timezone.now() - timedelta(hours=1)
        )
        
        self.future_subscription = Subscription.objects.create(
            customer_email='future@example.com',
            amount=Decimal('19.99'),
            currency='USD',
            interval=Subscription.Interval.MONTHLY,
            status=Subscription.Status.ACTIVE,
            next_payment_date=timezone.now() + timedelta(days=30)
        )
        
        self.paused_subscription = Subscription.objects.create(
            customer_email='paused@example.com',
            amount=Decimal('39.99'),
            currency='USD',
            interval=Subscription.Interval.MONTHLY,
            status=Subscription.Status.PAUSED,
            next_payment_date=timezone.now() - timedelta(days=1)
        )
    
    def test_process_due_payments(self):
        """Test processing all due payments."""
        payments = self.scheduler.process_due_payments()
        
        # Should process 2 due subscriptions
        self.assertEqual(len(payments), 2)
        
        # Check that all processed payments are completed
        for payment in payments:
            self.assertEqual(payment.status, Payment.Status.COMPLETED)
        
        # Check that next payment dates were advanced
        self.due_subscription_1.refresh_from_db()
        self.due_subscription_2.refresh_from_db()
        self.assertGreater(self.due_subscription_1.next_payment_date, timezone.now())
        self.assertGreater(self.due_subscription_2.next_payment_date, timezone.now())
    
    def test_process_specific_subscription(self):
        """Test processing a specific subscription."""
        payment = self.scheduler.process_subscription(self.due_subscription_1.id)
        
        self.assertIsNotNone(payment)
        self.assertEqual(payment.status, Payment.Status.COMPLETED)
        self.assertEqual(payment.subscription, self.due_subscription_1)
    
    def test_no_due_payments(self):
        """Test when no payments are due."""
        # Mark all subscriptions as future or paused
        Subscription.objects.filter(
            status=Subscription.Status.ACTIVE
        ).update(next_payment_date=timezone.now() + timedelta(days=30))
        
        payments = self.scheduler.process_due_payments()
        
        # Should process 0 payments
        self.assertEqual(len(payments), 0)
    
    def test_partial_failure_continues_processing(self):
        """Test that scheduler continues processing even if one payment fails."""
        # Use gateway with 50% success rate to simulate some failures
        unreliable_gateway = MockPaymentGateway(success_rate=0.5)
        scheduler = RecurringPaymentScheduler(payment_gateway=unreliable_gateway)
        
        # This should not raise an exception even if some payments fail
        payments = scheduler.process_due_payments()
        
        # Should attempt to process, but may have failures
        # We just verify it doesn't crash and returns a list
        self.assertIsInstance(payments, list)
