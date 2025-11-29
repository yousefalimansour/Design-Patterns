"""
Process Payment Command - Single payment processing.

This module implements the Command Pattern for processing individual payments.
"""

from decimal import Decimal
from typing import Optional
import logging

from command.core.base_command import BaseCommand
from command.payments.models.payment import Payment
from command.payments.gateways.mock_gateway import MockPaymentGateway

logger = logging.getLogger(__name__)


class ProcessPaymentCommand(BaseCommand):
    """
    Command to process a single payment transaction.
    
    This command encapsulates the logic for charging a payment through
    the payment gateway and creating a Payment record.
    
    Attributes:
        amount: Payment amount
        currency: Currency code
        customer_email: Customer's email
        payment_gateway: Payment gateway instance
        payment: Created Payment instance (set after execution)
    """
    
    def __init__(
        self,
        amount: Decimal,
        customer_email: str,
        currency: str = 'USD',
        payment_gateway: Optional[MockPaymentGateway] = None
    ):
        """
        Initialize the process payment command.
        
        Args:
            amount: Amount to charge
            customer_email: Customer's email address
            currency: Currency code (default: USD)
            payment_gateway: Payment gateway instance (creates new if None)
        """
        super().__init__()
        self.amount = amount
        self.currency = currency
        self.customer_email = customer_email
        self.payment_gateway = payment_gateway or MockPaymentGateway()
        self.payment: Optional[Payment] = None
    
    def execute(self) -> Payment:
        """
        Execute the payment processing command.
        
        Creates a Payment record and processes it through the payment gateway.
        
        Returns:
            Payment: The created and processed Payment instance
            
        Raises:
            Exception: If payment processing fails
        """
        logger.info(
            f"Processing payment: {self.amount} {self.currency} for {self.customer_email}"
        )
        
        # Create payment record
        self.payment = Payment.objects.create(
            amount=self.amount,
            currency=self.currency,
            customer_email=self.customer_email,
            status=Payment.Status.PENDING
        )
        
        try:
            # Process payment through gateway
            result = self.payment_gateway.charge(
                amount=self.amount,
                currency=self.currency,
                customer_email=self.customer_email
            )
            
            if result['success']:
                # Mark payment as completed
                self.payment.mark_completed(result['transaction_id'])
                logger.info(
                    f"Payment {self.payment.id} completed successfully. "
                    f"Transaction ID: {result['transaction_id']}"
                )
            else:
                # Mark payment as failed
                self.payment.mark_failed()
                logger.error(
                    f"Payment {self.payment.id} failed: {result['message']}"
                )
                raise Exception(f"Payment failed: {result['message']}")
            
            self.result = self.payment
            return self.payment
            
        except Exception as e:
            # Ensure payment is marked as failed
            if self.payment and self.payment.status == Payment.Status.PENDING:
                self.payment.mark_failed()
            logger.error(f"Payment processing error: {str(e)}")
            raise
    
    def undo(self) -> Optional[Payment]:
        """
        Undo the payment by processing a refund.
        
        Returns:
            Optional[Payment]: The refunded payment instance
            
        Raises:
            ValueError: If payment cannot be refunded
        """
        if not self.payment:
            logger.warning("Cannot undo: No payment to refund")
            return None
        
        if self.payment.status != Payment.Status.COMPLETED:
            raise ValueError(
                f"Cannot refund payment {self.payment.id} with status {self.payment.status}"
            )
        
        logger.info(f"Refunding payment {self.payment.id}")
        
        try:
            # Process refund through gateway
            result = self.payment_gateway.refund(
                transaction_id=self.payment.transaction_id,
                amount=self.payment.amount
            )
            
            if result['success']:
                # Mark payment as refunded
                self.payment.mark_refunded()
                logger.info(
                    f"Payment {self.payment.id} refunded successfully. "
                    f"Refund ID: {result['refund_id']}"
                )
            else:
                logger.error(
                    f"Refund for payment {self.payment.id} failed: {result['message']}"
                )
                raise Exception(f"Refund failed: {result['message']}")
            
            return self.payment
            
        except Exception as e:
            logger.error(f"Refund processing error: {str(e)}")
            raise
    
    def can_undo(self) -> bool:
        """
        Check if this command can be undone.
        
        Returns:
            bool: True if payment exists and is completed
        """
        return (
            self.payment is not None
            and self.payment.status == Payment.Status.COMPLETED
        )
    
    def __str__(self) -> str:
        """String representation of the command."""
        return (
            f"ProcessPaymentCommand("
            f"amount={self.amount}, "
            f"currency={self.currency}, "
            f"customer={self.customer_email})"
        )
