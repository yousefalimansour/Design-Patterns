"""
Recurring Payment Scheduler Service.

This service finds subscriptions that are due for payment and processes them
using the RecurringPaymentCommand.
"""

from typing import List
import logging
from django.utils import timezone

from command.payments.models.subscription import Subscription
from command.payments.models.payment import Payment
from command.payments.commands.recurring_payment_command import RecurringPaymentCommand
from command.payments.gateways.mock_gateway import MockPaymentGateway
from command.core.invoker import CommandInvoker

logger = logging.getLogger(__name__)


class RecurringPaymentScheduler:
    """
    Service to process recurring payments for active subscriptions.
    
    This scheduler finds all subscriptions that are due for payment
    and processes them using the Command Pattern.
    
    Attributes:
        payment_gateway: Payment gateway instance
        invoker: Command invoker for executing commands
    """
    
    def __init__(
        self,
        payment_gateway: MockPaymentGateway = None,
        invoker: CommandInvoker = None
    ):
        """
        Initialize the recurring payment scheduler.
        
        Args:
            payment_gateway: Payment gateway instance (creates new if None)
            invoker: Command invoker (creates new if None)
        """
        self.payment_gateway = payment_gateway or MockPaymentGateway()
        self.invoker = invoker or CommandInvoker()
    
    def process_due_payments(self) -> List[Payment]:
        """
        Process all subscriptions that are due for payment.
        
        Finds all active subscriptions with next_payment_date <= now
        and processes their payments.
        
        Returns:
            List[Payment]: List of successfully processed payments
        """
        logger.info("Starting recurring payment processing")
        
        # Find subscriptions due for payment
        due_subscriptions = Subscription.objects.filter(
            status=Subscription.Status.ACTIVE,
            next_payment_date__lte=timezone.now()
        )
        
        logger.info(f"Found {due_subscriptions.count()} subscriptions due for payment")
        
        processed_payments = []
        
        for subscription in due_subscriptions:
            try:
                # Create recurring payment command
                command = RecurringPaymentCommand(
                    subscription=subscription,
                    payment_gateway=self.payment_gateway
                )
                
                # Execute command through invoker
                payment = self.invoker.execute_command(command)
                
                if payment:
                    processed_payments.append(payment)
                    logger.info(
                        f"Successfully processed payment {payment.id} for "
                        f"subscription {subscription.id}"
                    )
                else:
                    logger.info(
                        f"Payment not processed for subscription {subscription.id} "
                        f"(not due yet)"
                    )
                    
            except Exception as e:
                logger.error(
                    f"Failed to process payment for subscription {subscription.id}: "
                    f"{str(e)}"
                )
                # Continue processing other subscriptions even if one fails
                continue
        
        logger.info(
            f"Recurring payment processing completed. "
            f"Processed {len(processed_payments)} payments"
        )
        
        return processed_payments
    
    def process_subscription(self, subscription_id: int) -> Payment:
        """
        Process a specific subscription's recurring payment.
        
        Args:
            subscription_id: ID of the subscription to process
            
        Returns:
            Payment: The processed payment
            
        Raises:
            Subscription.DoesNotExist: If subscription not found
            Exception: If payment processing fails
        """
        logger.info(f"Processing recurring payment for subscription {subscription_id}")
        
        subscription = Subscription.objects.get(id=subscription_id)
        
        # Create and execute recurring payment command
        command = RecurringPaymentCommand(
            subscription=subscription,
            payment_gateway=self.payment_gateway
        )
        
        payment = self.invoker.execute_command(command)
        
        return payment
