# Payment System MVP - Command Pattern

This directory contains a complete MVP implementation of a Payment System using the **Command Pattern**.

## 🚀 Quick Start

```bash
# 1. Activate virtual environment
source ../.venv/bin/activate  # from behavioral/command/

# 2. Run migrations (from behavioral/)
cd ..
python manage.py makemigrations command
python manage.py migrate

# 3. Run tests
python manage.py test command.tests -v 2

# 4. Start server
python manage.py runserver
```

## 📁 Structure

```
command/
├── core/               # Command Pattern foundation
├── payments/           # Payment domain logic
│   ├── models/        # Payment & Subscription models
│   ├── commands/      # Payment commands
│   ├── gateways/      # Mock payment gateway
│   └── services/      # Recurring payment scheduler
├── api/               # REST API endpoints
└── tests/             # Unit tests
```

## 🎯 Key Features

- ✅ Single payment processing via `ProcessPaymentCommand`
- ✅ Recurring payments via `RecurringPaymentCommand`
- ✅ Command execution through `CommandInvoker`
- ✅ Undo support (refunds)
- ✅ Mock payment gateway (90% success rate)
- ✅ REST API with DRF
- ✅ Comprehensive unit tests

## 🌐 API Endpoints

Base: `http://localhost:8000/command/api/`

- `POST /payments/process/` - Process payment
- `POST /payments/{id}/refund/` - Refund payment
- `POST /payments/process-recurring/` - Trigger recurring payments
- `GET /payments/` - List payments
- `GET /subscriptions/` - List subscriptions
- `POST /subscriptions/` - Create subscription

## 📖 Example Usage

### Process a Payment

```bash
curl -X POST http://localhost:8000/command/api/payments/process/ \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "99.99",
    "currency": "USD",
    "customer_email": "customer@example.com"
  }'
```

### Create a Subscription

```bash
curl -X POST http://localhost:8000/command/api/subscriptions/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_email": "subscriber@example.com",
    "amount": "29.99",
    "currency": "USD",
    "interval": "MONTHLY"
  }'
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test command.tests -v 2

# Run specific tests
python manage.py test command.tests.test_commands
python manage.py test command.tests.test_scheduler
```

## 📝 Models

### Payment
- `amount`, `currency`, `status`, `transaction_id`
- Status: `PENDING`, `COMPLETED`, `FAILED`, `REFUNDED`

### Subscription
- `amount`, `currency`, `interval`, `status`, `next_payment_date`
- Interval: `DAILY`, `WEEKLY`, `MONTHLY`, `YEARLY`
- Status: `ACTIVE`, `PAUSED`, `CANCELLED`

## 🏗️ Command Pattern

```python
# Create command
command = ProcessPaymentCommand(
    amount=Decimal('99.99'),
    customer_email='customer@example.com'
)

# Execute via invoker
invoker = CommandInvoker()
payment = invoker.execute_command(command)

# Undo (refund)
invoker.undo_last_command()
```

## 🔧 Extension Points

- Add real payment gateways (Stripe, PayPal)
- Add Celery for automated recurring payments
- Add webhooks for payment notifications
- Add authentication/authorization
- Add payment retries and error handling

---

For detailed documentation, see the walkthrough artifact in `.gemini/antigravity/brain/*/walkthrough.md`
