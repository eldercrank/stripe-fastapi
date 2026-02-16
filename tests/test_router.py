"""Tests for the eldercrank-stripe-fastapi package."""

from fastapi import FastAPI
from eldercrank.stripe.core import StripeHandler
from eldercrank.stripe.fastapi import create_stripe_router


class TestCreateStripeRouter:
    """Tests for the create_stripe_router function."""

    def test_create_stripe_router(self):
        """Test that create_stripe_router returns an APIRouter."""
        handler = StripeHandler(api_key="sk_test_123", webhook_secret="whsec_123")

        router = create_stripe_router(handler)

        assert router is not None

    def test_create_stripe_router_with_custom_path(self):
        """Test creating a router with a custom webhook path."""
        handler = StripeHandler(api_key="sk_test_123", webhook_secret="whsec_123")

        router = create_stripe_router(handler, webhook_path="/custom/webhook")

        assert router is not None

    def test_router_included_in_app(self):
        """Test that the router can be included in a FastAPI app."""
        handler = StripeHandler(api_key="sk_test_123", webhook_secret="whsec_123")

        router = create_stripe_router(handler)
        app = FastAPI()
        app.include_router(router)

        paths = [route.path for route in app.routes]
        assert "/webhook" in paths

    def test_router_with_custom_path_in_app(self):
        """Test that a custom path router works in a FastAPI app."""
        handler = StripeHandler(api_key="sk_test_123", webhook_secret="whsec_123")

        router = create_stripe_router(handler, webhook_path="/stripe/events")
        app = FastAPI()
        app.include_router(router)

        paths = [route.path for route in app.routes]
        assert "/stripe/events" in paths

    def test_default_webhook_path(self):
        """Test that the default webhook path is /webhook."""
        handler = StripeHandler(api_key="sk_test_123", webhook_secret="whsec_123")

        router = create_stripe_router(handler)
        app = FastAPI()
        app.include_router(router)

        # Find the webhook route
        webhook_routes = [
            r for r in app.routes if hasattr(r, "path") and "webhook" in r.path
        ]
        assert len(webhook_routes) == 1
        assert webhook_routes[0].path == "/webhook"
