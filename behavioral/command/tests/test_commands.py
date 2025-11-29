"""
Unit tests for Command Pattern implementation.

Tests for BaseCommand, ProcessPaymentCommand, RecurringPaymentCommand, and CommandInvoker.
"""

from django.test import TestCase
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from command.core.base_command import BaseCommand
from command.core.invoker import CommandInvoker
from command.payments.models.payment import Payment
from command.payments.models.subscription import Subscription
from command.payments.commands.process_payment_command import ProcessPaymentCommand
from command.payments.commands.recurring_payment_command import RecurringPaymentCommand
from command.payments.gateways.mock_gateway import MockPaymentGateway


class SimpleTestCommand(BaseCommand):
    """Simple test command for testing base functionality."""
    
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def execute(self):
        """Execute by returning the value."""
        self.result = self.value * 2
        return self.result
    
    def undo(self):
        """Undo by returning original value."""
        self.result = self.value
        return self.result
    
    def can_undo(self):
        """This command supports undo."""
        return True


class BaseCommandTestCase(TestCase):
    """Test cases for BaseCommand."""
    
    def test_command_initialization(self):
        """Test command initializes with correct default state."""
        command = SimpleTestCommand(5)
        self.assertFalse(command.executed)
        self.assertIsNone(command.result)
    
    def test_command_execute(self):
        """Test command execution."""
        command = SimpleTestCommand(5)
        result = command.execute()
        self.assertEqual(result, 10)
        self.assertEqual(command.result, 10)
    
    def test_command_undo(self):
        """Test command undo."""
        command = SimpleTestCommand(5)
        command.execute()
        result = command.undo()
        self.assertEqual(result, 5)
    
    def test_command_can_undo(self):
        """Test can_undo check."""
        command = SimpleTestCommand(5)
        self.assertTrue(command.can_undo())


class CommandInvokerTestCase(TestCase):
    """Test cases for CommandInvoker."""
    
    def test_invoker_initialization(self):
        """Test invoker initializes correctly."""
        invoker = CommandInvoker()
        self.assertEqual(len(invoker.history), 0)
    
    def test_invoker_execute_command(self):
        """Test invoker executes commands."""
        invoker = CommandInvoker()
        command = SimpleTestCommand(5)
        result = invoker.execute_command(command)
        
        self.assertEqual(result, 10)
        self.assertTrue(command.executed)
        self.assertEqual(len(invoker.history), 1)
    
    def test_invoker_undo_command(self):
        """Test invoker undoes commands."""
        invoker = CommandInvoker()
        command = SimpleTestCommand(5)
        invoker.execute_command(command)
        
        result = invoker.undo_last_command()
        self.assertEqual(result, 5)
        self.assertEqual(len(invoker.history), 0)
    
    def test_invoker_command_history(self):
        """Test invoker maintains command history."""
        invoker = CommandInvoker()
        command1 = SimpleTestCommand(5)
        command2 = SimpleTestCommand(10)
        
        invoker.execute_command(command1)
        invoker.execute_command(command2)
        
        self.assertEqual(len(invoker.history), 2)
        history = invoker.get_history()
        self.assertEqual(len(history), 2)
    
    def test_invoker_clear_history(self):
        """Test invoker clears history."""
        invoker = CommandInvoker()
        command = SimpleTestCommand(5)
        invoker.execute_command(command)
        
        invoker.clear_history()
        self.assertEqual(len(invoker.history), 0)


class ProcessPaymentCommandTestCase(TestCase):
    """Test cases for ProcessPaymentCommand."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Use a gateway with 100% success rate for predictable tests
        self.gateway = MockPaymentGateway(success_rate=1.0)
    
    def test_process_payment_success(self):
        """Test successful payment processing."""
        command = ProcessPaymentCommand(
            amount=Decimal('99.99'),
            customer_email='test@example.com',
            currency='USD',
            payment_gateway=self.gateway
        )
        
        payment = command.execute()
        
        self.assertIsNotNone(payment)
        self.assertEqual(payment.status, Payment.Status.COMPLETED)
        self.assertEqual(payment.amount, Decimal('99.99'))
        self.assertEqual(payment.customer_email, 'test@example.com')
        self.assertIsNotNone(payment.transaction_id)
    
    def test_process_payment_failure(self):
        """Test failed payment processing."""
        # Use gateway with 0% success rate
        failing_gateway = MockPaymentGateway(success_rate=0.0)
        command = ProcessPaymentCommand(
            amount=Decimal('99.99'),
            customer_email='test@example.com',
            payment_gateway=failing_gateway
        )
        
        with self.assertRaises(Exception):
            command.execute()
        
        # Payment should be marked as failed
        self.assertEqual(command.payment.status, Payment.Status.FAILED)
    
    def test_payment_refund(self):
        """Test payment refund using undo."""
        command = ProcessPaymentCommand(
            amount=Decimal('99.99'),
            customer_email='test@example.com',
            payment_gateway=self.gateway
        )
        
        payment = command.execute()
        self.assertEqual(payment.status, Payment.Status.COMPLETED)
        
        # Test undo (refund)
        refunded_payment = command.undo()
        self.assertEqual(refunded_payment.status, Payment.Status.REFUNDED)
    
    def test_payment_can_undo(self):
        """Test can_undo for completed payment."""
        command = ProcessPaymentCommand(
            amount=Decimal('99.99'),
            customer_email='test@example.com',
            payment_gateway=self.gateway
        )
        
        self.assertFalse(command.can_undo())
        
        command.execute()
        self.assertTrue(command.can_undo())


class RecurringPaymentCommandTestCase(TestCase):
    """Test cases for RecurringPaymentCommand."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.gateway = MockPaymentGateway(success_rate=1.0)
        
        # Create an active subscription due for payment
        self.subscription = Subscription.objects.create(
            customer_email='subscriber@example.com',
            amount=Decimal('29.99'),
            currency='USD',
            interval=Subscription.Interval.MONTHLY,
            status=Subscription.Status.ACTIVE,
            next_payment_date=timezone.now() - timedelta(days=1)  # Past due
        )
    
    def test_recurring_payment_execution(self):
        """Test recurring payment execution."""
        command = RecurringPaymentCommand(
            subscription=self.subscription,
            payment_gateway=self.gateway
        )
        
        payment = command.execute()
        
        self.assertIsNotNone(payment)
        self.assertEqual(payment.status, Payment.Status.COMPLETED)
        self.assertEqual(payment.subscription, self.subscription)
        self.assertEqual(payment.amount, Decimal('29.99'))
        
        # Check that next payment date was advanced
        self.subscription.refresh_from_db()
        self.assertGreater(self.subscription.next_payment_date, timezone.now())
    
    def test_recurring_payment_not_due(self):
        """Test recurring payment when not due."""
        # Create subscription with future payment date
        future_subscription = Subscription.objects.create(
            customer_email='future@example.com',
            amount=Decimal('19.99'),
            currency='USD',
            interval=Subscription.Interval.MONTHLY,
            status=Subscription.Status.ACTIVE,
            next_payment_date=timezone.now() + timedelta(days=30)
        )
        
        command = RecurringPaymentCommand(
            subscription=future_subscription,
            payment_gateway=self.gateway
        )
        
        payment = command.execute()
        
        # Should return None when not due
        self.assertIsNone(payment)
    
    def test_recurring_payment_inactive_subscription(self):
        """Test recurring payment with inactive subscription."""
        self.subscription.status = Subscription.Status.PAUSED
        self.subscription.save()
        
        command = RecurringPaymentCommand(
            subscription=self.subscription,
            payment_gateway=self.gateway
        )
        
        with self.assertRaises(ValueError):
            command.execute()
    
    def test_recurring_payment_undo(self):
        """Test undoing a recurring payment."""
        command = RecurringPaymentCommand(
            subscription=self.subscription,
            payment_gateway=self.gateway
        )
        
        payment = command.execute()
        self.assertEqual(payment.status, Payment.Status.COMPLETED)
        
        # Test undo
        refunded_payment = command.undo()
        self.assertEqual(refunded_payment.status, Payment.Status.REFUNDED)
