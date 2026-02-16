# eldercrank-stripe-fastapi

FastAPI integration for the eldercrank-stripe library, providing easy webhook handling for Stripe events in FastAPI applications.

## Features

- **Simple Router Creation**: One function call to create a webhook router
- **Automatic Signature Verification**: Handled by the underlying StripeHandler
- **Customizable Path**: Configure your webhook endpoint path
- **Proper Error Handling**: Returns appropriate HTTP status codes for Stripe

## Installation

```bash
pip install eldercrank-stripe-fastapi
```

## Quick Start

```python
from fastapi import FastAPI
from eldercrank_stripe_core import StripeHandler
from eldercrank.stripe.fastapi import create_stripe_router

# Create your Stripe handler
handler = StripeHandler(
    api_key="sk_test_...",
    webhook_secret="whsec_..."
)

# Create your FastAPI app
app = FastAPI()

# Include the Stripe webhook router
app.include_router(create_stripe_router(handler))

# Register event handlers
def handle_payment_success(event_data):
    print(f"Payment successful!")

handler.add_event_handler("payment_intent.succeeded", handle_payment_success)
```

## Custom Webhook Path

```python
# Use a custom webhook path
app.include_router(
    create_stripe_router(handler, webhook_path="/stripe/webhook")
)
```

## License

MIT
