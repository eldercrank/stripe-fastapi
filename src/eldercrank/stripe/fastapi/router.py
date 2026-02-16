from fastapi import APIRouter, Request, Header, HTTPException
from eldercrank_stripe_core import StripeHandler
from typing import Optional


def create_stripe_router(
    handler: StripeHandler, webhook_path: str = "/webhook"
) -> APIRouter:
    """
    Creates a FastAPI router for handling Stripe webhooks.

    Args:
        handler: An instance of StripeHandler to process the webhooks.
        webhook_path: The URL path for the webhook endpoint (default: "/webhook").

    Returns:
        FastAPI APIRouter with the webhook route registered.

    Example:
        ```python
        from fastapi import FastAPI
        from eldercrank_stripe_core import StripeHandler
        from eldercrank.stripe.fastapi import create_stripe_router

        handler = StripeHandler(api_key="sk_test_...", webhook_secret="whsec_...")
        app = FastAPI()
        app.include_router(create_stripe_router(handler))
        ```
    """
    router = APIRouter()

    @router.post(webhook_path)
    async def stripe_webhook(
        request: Request, stripe_signature: Optional[str] = Header(None)
    ):
        if not stripe_signature:
            raise HTTPException(
                status_code=400, detail="Missing stripe-signature header"
            )

        payload = await request.body()
        try:
            handler.process_webhook(payload.decode("utf-8"), stripe_signature)
            return {"status": "success"}
        except Exception as e:
            # Return 400 so Stripe knows to retry on failure
            raise HTTPException(status_code=400, detail=str(e))

    return router
