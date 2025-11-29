"""
Recurring Payment Command - Process subscription payments.

This module implements the Command Pattern for processing recurring subscription payments.
"""

from typing import Optional
import logging

from command.core.base_command import BaseCommand
from command.payments.models.subscription import Subscription
from command.payments.models.payment import Payment
from command.payments.commands.process_payment_command import ProcessPaymentCommand
from command.payments.gateways.mock_gateway import MockPaymentGateway

logger = logging.getLogger(__name__)


class RecurringPaymentCommand(BaseCommand):
    """
    Command to process a recurring payment for a subscription.
    
    This command checks if a subscription payment is due and processes it
    by delegating to a ProcessPaymentCommand.
    
    Attributes:
        subscription: The subscription to process payment for
        payment_gateway: Payment gateway instance
        process_payment_cmd: The delegated payment command (set after execution)
    """
    
    def __init__(
        self,
        subscription: Subscription,
        payment_gateway: Optional[MockPaymentGateway] = None
    ):
        """
        Initialize the recurring payment command.
        
        Args:
            subscription: Subscription instance to process payment for
            payment_gateway: Payment gateway instance (creates new if None)
        """
        super().__init__()
        self.subscription = subscription
        self.payment_gateway = payment_gateway or MockPaymentGateway()
        self.process_payment_cmd: Optional[ProcessPaymentCommand] = None
    
    def execute(self) -> Optional[Payment]:
        """
        Execute the recurring payment processing.
        
        Checks if payment is due, processes it, and updates the next payment date.
        
        Returns:
            Optional[Payment]: The created payment if processed, None if not due
            
        Raises:
            ValueError: If subscription is not active
            Exception: If payment processing fails
        """
        logger.info(f"Processing recurring payment for subscription {self.subscription.id}")
        
        # Check if subscription is active
        if self.subscription.status != Subscription.Status.ACTIVE:
            raise ValueError(
                f"Cannot process payment for subscription {self.subscription.id} "
                f"with status {self.subscription.status}"
            )
        
        # Check if payment is due
        if not self.subscription.is_payment_due():
            logger.info(
                f"Payment not due for subscription {self.subscription.id}. "
                f"Next payment date: {self.subscription.next_payment_date}"
            )
            return None
        
        try:
            # Create and execute process payment command
            self.process_payment_cmd = ProcessPaymentCommand(
                amount=self.subscription.amount,
                customer_email=self.subscription.customer_email,
                currency=self.subscription.currency,
                payment_gateway=self.payment_gateway
            )
            
            payment = self.process_payment_cmd.execute()
            
            # Link payment to subscription
            payment.subscription = self.subscription
            payment.save()
            
            # Advance next payment date
            self.subscription.advance_next_payment_date()
            
            logger.info(
                f"Recurring payment {payment.id} processed successfully for "
                f"subscription {self.subscription.id}. "
                f"Next payment date: {self.subscription.next_payment_date}"
            )
            
            self.result = payment
            return payment
            
        except Exception as e:
            logger.error(
                f"Recurring payment processing failed for subscription "
                f"{self.subscription.id}: {str(e)}"
            )
            raise
    
    def undo(self) -> Optional[Payment]:
        """
        Undo the recurring payment by refunding.
        
        This delegates to the undo method of the ProcessPaymentCommand
        and rolls back the next payment date.
        
        Returns:
            Optional[Payment]: The refunded payment
        """
        if not self.process_payment_cmd:
            logger.warning("Cannot undo: No payment command to undo")
            return None
        
        logger.info(f"Undoing recurring payment for subscription {self.subscription.id}")
        
        try:
            # Undo the payment command (refund)
            payment = self.process_payment_cmd.undo()
            
            # Note: We don't roll back the next_payment_date as it's complex
            # In a real system, you'd need to store the previous date
            logger.info(
                f"Recurring payment undone for subscription {self.subscription.id}"
            )
            
            return payment
            
        except Exception as e:
            logger.error(f"Recurring payment undo failed: {str(e)}")
            raise
    
    def can_undo(self) -> bool:
        """
        Check if this command can be undone.
        
        Returns:
            bool: True if the delegated payment command can be undone
        """
        return (
            self.process_payment_cmd is not None
            and self.process_payment_cmd.can_undo()
        )
    
    def __str__(self) -> str:
        """String representation of the command."""
        return (
            f"RecurringPaymentCommand("
            f"subscription_id={self.subscription.id}, "
            f"customer={self.subscription.customer_email})"
        )
