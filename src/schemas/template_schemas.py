from pydantic import BaseModel, Field, validator
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

class TemplateBase(BaseModel):
    """Base template model with common fields."""
    name: str = Field(..., description="Name of the template")
    description: Optional[str] = Field(None, description="Description of the template")
    content: Dict[str, Any] = Field(..., description="Content of the template")
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name must not be empty')
        return v

class TemplateCreate(TemplateBase):
    """Template creation model."""
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for the template")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Welcome Message",
                "description": "Template for welcoming new users",
                "content": {
                    "header": "Welcome to our service!",
                    "body": "Hello {{1}}, we're glad to have you on board.",
                    "footer": "The Team"
                },
                "tags": ["welcome", "onboarding"]
            }
        }

class TemplateUpdate(BaseModel):
    """Template update model."""
    name: Optional[str] = Field(None, description="Name of the template")
    description: Optional[str] = Field(None, description="Description of the template")
    content: Optional[Dict[str, Any]] = Field(None, description="Content of the template")
    tags: Optional[List[str]] = Field(None, description="Tags for the template")
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Name must not be empty')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Welcome Message",
                "description": "Updated template for welcoming new users",
                "content": {
                    "header": "Welcome to our amazing service!",
                    "body": "Hello {{1}}, we're thrilled to have you on board.",
                    "footer": "The Support Team"
                },
                "tags": ["welcome", "onboarding", "greeting"]
            }
        }

class TemplateResponse(TemplateBase):
    """Template response model."""
    id: str = Field(..., description="ID of the template")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    tags: List[str] = Field(default_factory=list, description="Tags for the template")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Welcome Message",
                "description": "Template for welcoming new users",
                "content": {
                    "header": "Welcome to our service!",
                    "body": "Hello {{1}}, we're glad to have you on board.",
                    "footer": "The Team"
                },
                "tags": ["welcome", "onboarding"],
                "created_at": "2023-11-01T12:00:00",
                "updated_at": "2023-11-01T12:00:00"
            }
        } 