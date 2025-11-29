"""
Mock Payment Gateway for simulating payment processing.

This module provides a mock implementation of a payment gateway
that simulates successful and failed payment transactions.
"""

import random
import uuid
from typing import Dict, Any
from decimal import Decimal


class MockPaymentGateway:
    """
    Mock payment gateway that simulates payment processing.
    
    This gateway randomly succeeds or fails to simulate real-world scenarios.
    In a production environment, this would be replaced with actual payment
    gateway integrations (Stripe, PayPal, etc.).
    """
    
    def __init__(self, success_rate: float = 0.9):
        """
        Initialize the mock payment gateway.
        
        Args:
            success_rate: Probability of successful payment (0.0 to 1.0, default: 0.9)
        """
        self.success_rate = success_rate
    
    def charge(
        self,
        amount: Decimal,
        currency: str = 'USD',
        customer_email: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Simulate charging a payment.
        
        Args:
            amount: Amount to charge
            currency: Currency code
            customer_email: Customer's email address
            **kwargs: Additional payment parameters
            
        Returns:
            Dict containing transaction result with keys:
                - success: Boolean indicating if payment succeeded
                - transaction_id: Unique transaction identifier
                - message: Status message
                - amount: Charged amount
                - currency: Currency code
        """
        # Simulate payment processing
        success = random.random() < self.success_rate
        transaction_id = f"txn_{uuid.uuid4().hex[:16]}" if success else None
        
        if success:
            return {
                'success': True,
                'transaction_id': transaction_id,
                'message': 'Payment processed successfully',
                'amount': amount,
                'currency': currency,
                'customer_email': customer_email
            }
        else:
            return {
                'success': False,
                'transaction_id': None,
                'message': 'Payment processing failed - insufficient funds or card declined',
                'amount': amount,
                'currency': currency,
                'customer_email': customer_email
            }
    
    def refund(
        self,
        transaction_id: str,
        amount: Decimal = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Simulate refunding a payment.
        
        Args:
            transaction_id: Original transaction ID to refund
            amount: Amount to refund (None for full refund)
            **kwargs: Additional refund parameters
            
        Returns:
            Dict containing refund result with keys:
                - success: Boolean indicating if refund succeeded
                - refund_id: Unique refund identifier
                - message: Status message
        """
        # Simulate refund processing
        success = random.random() < 0.95  # Higher success rate for refunds
        refund_id = f"rfnd_{uuid.uuid4().hex[:16]}" if success else None
        
        if success:
            return {
                'success': True,
                'refund_id': refund_id,
                'transaction_id': transaction_id,
                'message': 'Refund processed successfully',
                'amount': amount
            }
        else:
            return {
                'success': False,
                'refund_id': None,
                'transaction_id': transaction_id,
                'message': 'Refund processing failed',
                'amount': amount
            }
    
    def verify_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """
        Simulate verifying a transaction.
        
        Args:
            transaction_id: Transaction ID to verify
            
        Returns:
            Dict containing verification result
        """
        return {
            'valid': True,
            'transaction_id': transaction_id,
            'message': 'Transaction verified'
        }
