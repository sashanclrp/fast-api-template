from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class WebhookBase(BaseModel):
    """Base webhook model with common fields."""
    event_type: str = Field(..., description="Type of the webhook event")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the event")

class WebhookPayload(WebhookBase):
    """Webhook payload model."""
    data: Dict[str, Any] = Field(..., description="Webhook payload data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "message.received",
                "timestamp": "2023-11-01T12:00:00",
                "data": {
                    "message_id": "123456789",
                    "from": "user123",
                    "content": "Hello, world!"
                }
            }
        }

class WebhookCallback(BaseModel):
    """Webhook callback model."""
    callback_id: str = Field(..., description="ID of the callback")
    status: str = Field(..., description="Status of the callback")
    data: Optional[Dict[str, Any]] = Field(None, description="Callback data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "callback_id": "cb_123456789",
                "status": "success",
                "data": {
                    "result": "processed",
                    "details": "Message delivered successfully"
                }
            }
        }

class WebhookVerification(BaseModel):
    """Webhook verification model."""
    token: str = Field(..., description="Verification token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "token": "your_verification_token_here"
            }
        } 