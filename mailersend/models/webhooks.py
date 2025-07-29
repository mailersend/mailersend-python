"""Webhooks API models for MailerSend SDK."""

from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field, field_validator


# Query Parameters Models
class WebhooksListQueryParams(BaseModel):
    """Query parameters for listing webhooks."""

    domain_id: str = Field(..., description="Domain ID to filter webhooks")

    @field_validator("domain_id")
    @classmethod
    def validate_domain_id(cls, v: str) -> str:
        """Validate domain_id is not empty."""
        if not v or not v.strip():
            raise ValueError("domain_id cannot be empty")
        return v.strip()

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return {"domain_id": self.domain_id}


# Request Models
class WebhooksListRequest(BaseModel):
    """Request model for listing webhooks."""

    query_params: WebhooksListQueryParams

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return self.query_params.to_query_params()


class WebhookGetRequest(BaseModel):
    """Request model for getting a single webhook."""

    webhook_id: str = Field(..., description="Webhook ID to retrieve")

    @field_validator("webhook_id")
    @classmethod
    def validate_webhook_id(cls, v: str) -> str:
        """Validate webhook_id is not empty."""
        if not v or not v.strip():
            raise ValueError("webhook_id cannot be empty")
        return v.strip()


class WebhookCreateRequest(BaseModel):
    """Request model for creating a webhook."""

    url: str = Field(..., max_length=191, description="Webhook URL")
    name: str = Field(..., max_length=191, description="Webhook name")
    events: List[str] = Field(..., description="List of events to subscribe to")
    domain_id: str = Field(..., description="Domain ID for the webhook")
    enabled: Optional[bool] = Field(None, description="Whether webhook is enabled")

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate URL is not empty and not too long."""
        if not v or not v.strip():
            raise ValueError("url cannot be empty")
        if len(v.strip()) > 191:
            raise ValueError("url cannot exceed 191 characters")
        return v.strip()

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate name is not empty and not too long."""
        if not v or not v.strip():
            raise ValueError("name cannot be empty")
        if len(v.strip()) > 191:
            raise ValueError("name cannot exceed 191 characters")
        return v.strip()

    @field_validator("events")
    @classmethod
    def validate_events(cls, v: List[str]) -> List[str]:
        """Validate events list is not empty."""
        if not v:
            raise ValueError("events cannot be empty")
        return v

    @field_validator("domain_id")
    @classmethod
    def validate_domain_id(cls, v: str) -> str:
        """Validate domain_id is not empty."""
        if not v or not v.strip():
            raise ValueError("domain_id cannot be empty")
        return v.strip()


class WebhookUpdateRequest(BaseModel):
    """Request model for updating a webhook."""

    webhook_id: str = Field(..., description="Webhook ID to update")
    url: Optional[str] = Field(None, max_length=191, description="Webhook URL")
    name: Optional[str] = Field(None, max_length=191, description="Webhook name")
    events: Optional[List[str]] = Field(
        None, description="List of events to subscribe to"
    )
    enabled: Optional[bool] = Field(None, description="Whether webhook is enabled")

    @field_validator("webhook_id")
    @classmethod
    def validate_webhook_id(cls, v: str) -> str:
        """Validate webhook_id is not empty."""
        if not v or not v.strip():
            raise ValueError("webhook_id cannot be empty")
        return v.strip()

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        """Validate URL if provided."""
        if v is not None:
            if not v.strip():
                raise ValueError("url cannot be empty when provided")
            if len(v.strip()) > 191:
                raise ValueError("url cannot exceed 191 characters")
            return v.strip()
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate name if provided."""
        if v is not None:
            if not v.strip():
                raise ValueError("name cannot be empty when provided")
            if len(v.strip()) > 191:
                raise ValueError("name cannot exceed 191 characters")
            return v.strip()
        return v

    @field_validator("events")
    @classmethod
    def validate_events(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate events if provided."""
        if v is not None and not v:
            raise ValueError("events cannot be empty when provided")
        return v


class WebhookDeleteRequest(BaseModel):
    """Request model for deleting a webhook."""

    webhook_id: str = Field(..., description="Webhook ID to delete")

    @field_validator("webhook_id")
    @classmethod
    def validate_webhook_id(cls, v: str) -> str:
        """Validate webhook_id is not empty."""
        if not v or not v.strip():
            raise ValueError("webhook_id cannot be empty")
        return v.strip()


# Response Models
class Webhook(BaseModel):
    """Webhook response model."""

    id: str = Field(..., description="Webhook ID")
    url: str = Field(..., description="Webhook URL")
    name: str = Field(..., description="Webhook name")
    events: List[str] = Field(..., description="List of subscribed events")
    enabled: bool = Field(..., description="Whether webhook is enabled")
    domain_id: str = Field(..., description="Domain ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
