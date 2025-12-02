# ZendFi Python SDK

A lightweight, production-ready Python SDK for the ZendFi API. Supports payments, customers, invoices, webhooks, subscriptions, payment links, installment plans, and escrows.

**Package:** [`zendfi-sdk`](https://pypi.org/project/zendfi-sdk) on PyPI  
**License:** MIT  
**Python:** 3.8+

---

## Installation

```bash
pip install zendfi-sdk
```

With optional retry support (via tenacity):
```bash
pip install zendfi-sdk[retry]
```

---

## Quick Start

```python
from zendfi import from_env

# Initialize client from ZENDFI_API_KEY environment variable
client = from_env()

# Create a payment
payment = client.payments.create(
    amount=100.0,
    currency="USD",
    token="SOL",
    description="Order #12345"
)
print(payment.get("checkout_url"))
```

---

## Configuration

Set your API key via environment variable:

```bash
export ZENDFI_API_KEY="zfi_test_your_api_key_here"
```

Or pass it directly (not recommended for production):

```python
from zendfi import ZendFi

client = ZendFi(api_key="zfi_test_your_api_key_here")
```

Optional environment variables:
- `ZENDFI_BASE_URL` — Override API base URL (default: `https://api.zendfi.tech`)
- `ZENDFI_ENV` — Set environment (e.g., `test`, `live`)

---

## API Reference

### Payments

```python
# Create a payment
payment = client.payments.create(
    amount=100.0,
    currency="USD",
    token="SOL",
    description="Payment description",
    metadata={"order_id": "12345"},
    idempotency_key=None  # Optional: UUID for idempotency
)

# With split payments
payment = client.payments.create(
    amount=100.0,
    currency="USD",
    token="SOL",
    split_recipients=[
        {"recipient_wallet": "addr1", "percentage": 70.0},
        {"recipient_wallet": "addr2", "percentage": 30.0},
    ]
)

# Retrieve a payment
payment = client.payments.retrieve(payment_id="pay_xxx")

# List payments
payments = client.payments.list(limit=20, starting_after="pay_xxx")
```

### Customers

```python
# Create a customer
customer = client.customers.create(
    email="customer@example.com",
    name="John Doe",
    metadata={"user_id": "usr_123"}
)

# Retrieve a customer
customer = client.customers.retrieve(customer_id="cust_xxx")

# Update a customer
customer = client.customers.update(
    customer_id="cust_xxx",
    email="newemail@example.com",
    name="Jane Doe"
)

# Delete a customer
client.customers.delete(customer_id="cust_xxx")

# List customers
customers = client.customers.list(limit=20)
```

### Invoices

```python
# Create an invoice
invoice = client.invoices.create(
    amount=500.0,
    currency="USD",
    customer_email="client@example.com",
    customer_name="Acme Corp",
    line_items=[
        {"description": "Consulting", "quantity": 10, "unit_price": 50.0},
        {"description": "Setup", "quantity": 1, "unit_price": 0.0},
    ],
    due_date="2025-12-31T23:59:59Z",
    description="Invoice for services",
    metadata={"invoice_type": "service"}
)

# Send invoice to customer
sent = client.invoices.send(invoice_id=invoice.get("invoice_id"))

# Retrieve an invoice
invoice = client.invoices.retrieve(invoice_id="inv_xxx")

# List invoices
invoices = client.invoices.list(limit=20)
```

### Webhooks

```python
# Verify a webhook signature
payload = request.get_data()  # Raw request body
signature = request.headers.get("X-Signature-Header")

try:
    verified_payload = client.webhooks.verify(payload, signature)
    # Process webhook event
    print(verified_payload)
except Exception as e:
    print(f"Webhook verification failed: {e}")
```

### Subscriptions

```python
# Create a subscription plan
plan = client.subscriptions.create_plan(
    name="Monthly Plan",
    amount=29.99,
    currency="USD",
    interval="month"
)

# Create a subscription
sub = client.subscriptions.create(
    customer_id="cust_xxx",
    plan_id=plan.get("plan_id")
)

# Retrieve a subscription
sub = client.subscriptions.retrieve(subscription_id="sub_xxx")

# Cancel a subscription
client.subscriptions.cancel(subscription_id="sub_xxx")
```

### Payment Links

```python
# Create a payment link
link = client.payment_links.create(
    amount=100.0,
    currency="USD",
    description="One-time payment link"
)

# Retrieve a link
link = client.payment_links.retrieve(link_id="link_xxx")

# List links
links = client.payment_links.list(limit=20)
```

### Installment Plans

```python
# Create an installment plan
plan = client.installment_plans.create(
    customer_id="cust_xxx",
    amount=1000.0,
    currency="USD",
    num_installments=12
)

# Get plan details
plan = client.installment_plans.get(plan_id="inst_xxx")

# List plans for a customer
plans = client.installment_plans.list_customer_plans(customer_id="cust_xxx")

# Cancel a plan
client.installment_plans.cancel(plan_id="inst_xxx")
```

### Escrows

```python
# Create an escrow
escrow = client.escrows.create(
    amount=500.0,
    currency="USD",
    buyer_id="cust_buyer_xxx",
    seller_id="cust_seller_xxx"
)

# Approve an escrow
escrow = client.escrows.approve(escrow_id="esc_xxx")

# Refund an escrow
escrow = client.escrows.refund(escrow_id="esc_xxx")

# Dispute an escrow
escrow = client.escrows.dispute(escrow_id="esc_xxx", reason="Item not received")

# Retrieve an escrow
escrow = client.escrows.get(escrow_id="esc_xxx")

# List escrows
escrows = client.escrows.list(limit=20)
```

---

## Testing

### Mock Tests (Safe, no network calls)

Run test scripts in mock mode:

```bash
ZENDFI_RUN_MOCK=1 python tests/test_payments_splits.py
ZENDFI_RUN_MOCK=1 python tests/test_invoices.py
ZENDFI_RUN_MOCK=1 python tests/test_customers_unit.py
ZENDFI_RUN_MOCK=1 python tests/test_webhooks.py
```

### Integration Tests (Real API)

To test against the live ZendFi API:

```bash
export ZENDFI_API_KEY="zfi_test_your_key"
python tests/test_invoices.py
```

### Unit Tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

---

## Error Handling

```python
from zendfi import ZendFi
from zendfi.errors import APIError, WebhookVerificationError

client = ZendFi(api_key="zfi_test_xxx")

try:
    payment = client.payments.create(amount=100.0, currency="USD", token="SOL")
except APIError as e:
    print(f"API Error ({e.status_code}): {e.message}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Features

- ✅ Sync HTTP client with automatic retries on 5xx errors
- ✅ Idempotency support via `Idempotency-Key` headers
- ✅ Webhook signature verification (HMAC-SHA256)
- ✅ Mock-friendly test scripts
- ✅ Type hints (Python 3.8+)
- ✅ Comprehensive error handling
- ✅ Optional tenacity-based retry logic

---

## Publishing to PyPI

### Prerequisites

Generate a PyPI API token: https://pypi.org/manage/account/tokens/

### Manual Publish

```bash
pip install twine
python -m build
python -m twine upload dist/*
```

### Automated via GitHub Actions

1. Add `PYPI_API_TOKEN` secret to your GitHub repository settings
2. Tag and push a release:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
3. The `.github/workflows/publish.yml` workflow will build and publish automatically

---

## Development

### Setup

```bash
git clone https://github.com/zendfi/zendfi-python-toolkit.git
cd zendfi-python-toolkit
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

### Build

```bash
python -m build
```

### Lint & Type Check

```bash
ruff check .
mypy zendfi/
```

---

## Security

- **Never commit API keys or tokens** to the repository
- Use environment variables for secrets
- For CI/CD, use GitHub Secrets or your platform's secret management
- Webhook signatures are verified using HMAC-SHA256

---

## Support

For issues, feature requests, or questions, open an issue on GitHub:  
https://github.com/zendfi/zendfi-python-toolkit/issues

---

## License

MIT License. See [LICENSE](LICENSE) file for details.

