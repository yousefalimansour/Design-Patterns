"""
DRF Views for Payment System API.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from decimal import Decimal

from command.payments.models.payment import Payment
from command.payments.models.subscription import Subscription
from command.payments.commands.process_payment_command import ProcessPaymentCommand
from command.payments.services.scheduler import RecurringPaymentScheduler
from command.core.invoker import CommandInvoker

from .serializers import (
    PaymentSerializer,
    ProcessPaymentSerializer,
    SubscriptionSerializer,
    CreateSubscriptionSerializer
)


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing Payment records.
    
    Provides list and retrieve endpoints for payments.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        """Filter payments by query parameters."""
        queryset = super().get_queryset()
        
        # Filter by status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filter by customer email
        customer_email = self.request.query_params.get('customer_email')
        if customer_email:
            queryset = queryset.filter(customer_email=customer_email)
        
        return queryset


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Subscription records.
    
    Provides CRUD endpoints for subscriptions.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    
    def get_queryset(self):
        """Filter subscriptions by query parameters."""
        queryset = super().get_queryset()
        
        # Filter by status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filter by customer email
        customer_email = self.request.query_params.get('customer_email')
        if customer_email:
            queryset = queryset.filter(customer_email=customer_email)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Create a new subscription."""
        serializer = CreateSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create subscription with validated data
        subscription = Subscription.objects.create(
            customer_email=serializer.validated_data['customer_email'],
            amount=serializer.validated_data['amount'],
            currency=serializer.validated_data.get('currency', 'USD'),
            interval=serializer.validated_data.get('interval', Subscription.Interval.MONTHLY),
            next_payment_date=serializer.validated_data.get('next_payment_date', timezone.now()),
            status=Subscription.Status.ACTIVE
        )
        
        output_serializer = SubscriptionSerializer(subscription)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        """Pause a subscription."""
        subscription = self.get_object()
        subscription.pause()
        serializer = self.get_serializer(subscription)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def resume(self, request, pk=None):
        """Resume a paused subscription."""
        subscription = self.get_object()
        subscription.resume()
        serializer = self.get_serializer(subscription)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a subscription."""
        subscription = self.get_object()
        subscription.cancel()
        serializer = self.get_serializer(subscription)
        return Response(serializer.data)


class ProcessPaymentView(APIView):
    """
    API view to process a single payment using ProcessPaymentCommand.
    
    This demonstrates the Command Pattern by encapsulating the payment
    processing logic in a command object.
    """
    
    def post(self, request):
        """
        Process a single payment.
        
        Request body:
        {
            "amount": "99.99",
            "currency": "USD",
            "customer_email": "customer@example.com"
        }
        """
        serializer = ProcessPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Create command
            command = ProcessPaymentCommand(
                amount=Decimal(str(serializer.validated_data['amount'])),
                customer_email=serializer.validated_data['customer_email'],
                currency=serializer.validated_data.get('currency', 'USD')
            )
            
            # Execute command through invoker
            invoker = CommandInvoker()
            payment = invoker.execute_command(command)
            
            # Return payment details
            output_serializer = PaymentSerializer(payment)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class RefundPaymentView(APIView):
    """
    API view to refund a payment using command undo functionality.
    
    This demonstrates the undo capability of the Command Pattern.
    """
    
    def post(self, request, pk):
        """
        Refund a payment by undoing the ProcessPaymentCommand.
        
        URL: /api/payments/{id}/refund/
        """
        try:
            payment = Payment.objects.get(pk=pk)
            
            # Recreate command with payment
            command = ProcessPaymentCommand(
                amount=payment.amount,
                customer_email=payment.customer_email,
                currency=payment.currency
            )
            command.payment = payment
            command.executed = True
            
            # Undo the command (refund)
            refunded_payment = command.undo()
            
            # Return updated payment details
            serializer = PaymentSerializer(refunded_payment)
            return Response(serializer.data)
            
        except Payment.DoesNotExist:
            return Response(
                {'error': 'Payment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProcessRecurringPaymentsView(APIView):
    """
    API view to manually trigger recurring payment processing.
    
    This uses the RecurringPaymentScheduler to find and process
    all subscriptions that are due for payment.
    """
    
    def post(self, request):
        """
        Process all recurring payments that are due.
        
        Returns a list of processed payments.
        """
        try:
            # Create scheduler and process due payments
            scheduler = RecurringPaymentScheduler()
            processed_payments = scheduler.process_due_payments()
            
            # Return list of processed payments
            serializer = PaymentSerializer(processed_payments, many=True)
            return Response({
                'processed_count': len(processed_payments),
                'payments': serializer.data
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
