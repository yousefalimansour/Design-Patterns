"""
URL configuration for Payment System API.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PaymentViewSet,
    SubscriptionViewSet,
    ProcessPaymentView,
    RefundPaymentView,
    ProcessRecurringPaymentsView
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

# URL patterns
urlpatterns = [
    # ViewSet routes (GET /api/payments/, GET /api/subscriptions/, etc.)
    path('', include(router.urls)),
    
    # Custom action endpoints
    path('payments/process/', ProcessPaymentView.as_view(), name='process-payment'),
    path('payments/<int:pk>/refund/', RefundPaymentView.as_view(), name='refund-payment'),
    path('payments/process-recurring/', ProcessRecurringPaymentsView.as_view(), name='process-recurring'),
]
