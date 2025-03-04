from fastapi import APIRouter, Depends, Request, Query
from typing import Dict, Any, Optional

from controllers.webhook_controller import WebhookController
from schemas.webhook_schemas import WebhookCallback

router = APIRouter()

@router.get("/verify")
async def verify_webhook(token: str = Query(..., description="Verification token")):
    """
    Verify a webhook with the provided token.
    """
    return await WebhookController.verify_webhook(token)

@router.post("/receive")
async def receive_webhook(request: Request):
    """
    Receive and process a webhook.
    """
    return await WebhookController.receive_webhook(request)

@router.post("/callback")
async def webhook_callback(callback_data: WebhookCallback):
    """
    Handle a webhook callback.
    """
    return await WebhookController.handle_webhook_callback(callback_data.dict()) 