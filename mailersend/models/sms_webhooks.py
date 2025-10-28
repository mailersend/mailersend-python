"""SMS Webhooks models."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import Field, field_validator, HttpUrl
from .base import BaseModel
from enum import Enum


class SmsWebhookEvent(str, Enum):
    """SMS webhook event types."""

    SMS_SENT = "sms.sent"
    SMS_DELIVERED = "sms.delivered"
    SMS_FAILED = "sms.failed"


# Query Parameters Models
class SmsWebhooksListQueryParams(BaseModel):
    """Query parameters for listing SMS webhooks."""

    sms_number_id: str = Field(
        ..., min_length=1, description="SMS number ID to filter webhooks"
    )

    @field_validator("sms_number_id")
    @classmethod
    def validate_sms_number_id(cls, v: str) -> str:
        """Validate sms_number_id is not empty."""
        if not v or not v.strip():
            raise ValueError("sms_number_id cannot be empty")
        return v.strip()

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return {"sms_number_id": self.sms_number_id}


# Request Models
class SmsWebhooksListRequest(BaseModel):
    """Request model for listing SMS webhooks."""

    query_params: SmsWebhooksListQueryParams

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dictionary."""
        return self.query_params.to_query_params()


class SmsWebhookGetRequest(BaseModel):
    """Request model for getting a single SMS webhook."""

    sms_webhook_id: str = Field(..., min_length=1, description="SMS Webhook ID")

    @field_validator("sms_webhook_id")
    @classmethod
    def validate_sms_webhook_id(cls, v):
        """Validate SMS webhook ID."""
        if not v or not v.strip():
            raise ValueError("SMS webhook ID cannot be empty")
        return v.strip()


class SmsWebhookCreateRequest(BaseModel):
    """Request model for creating an SMS webhook."""

    url: HttpUrl = Field(..., description="Webhook URL")
    name: str = Field(..., min_length=1, max_length=191, description="Webhook name")
    events: List[SmsWebhookEvent] = Field(
        ..., min_length=1, description="List of events to listen for"
    )
    enabled: Optional[bool] = Field(
        default=True, description="Whether webhook is enabled"
    )
    sms_number_id: str = Field(..., min_length=1, description="SMS number ID")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        """Validate webhook name."""
        if not v or not v.strip():
            raise ValueError("Webhook name cannot be empty")
        return v.strip()

    @field_validator("sms_number_id")
    @classmethod
    def validate_sms_number_id(cls, v):
        """Validate SMS number ID."""
        if not v or not v.strip():
            raise ValueError("SMS number ID cannot be empty")
        return v.strip()

    def to_request_body(self) -> Dict[str, Any]:
        """Convert to request body dict."""
        body = {
            "url": str(self.url),
            "name": self.name,
            "events": [event.value for event in self.events],
            "sms_number_id": self.sms_number_id,
        }
        if self.enabled is not None:
            body["enabled"] = self.enabled
        return body


class SmsWebhookUpdateRequest(BaseModel):
    """Request model for updating an SMS webhook."""

    sms_webhook_id: str = Field(..., min_length=1, description="SMS Webhook ID")
    url: Optional[HttpUrl] = Field(None, description="Webhook URL")
    name: Optional[str] = Field(
        None, min_length=1, max_length=191, description="Webhook name"
    )
    events: Optional[List[SmsWebhookEvent]] = Field(
        None, min_length=1, description="List of events to listen for"
    )
    enabled: Optional[bool] = Field(None, description="Whether webhook is enabled")

    @field_validator("sms_webhook_id")
    @classmethod
    def validate_sms_webhook_id(cls, v):
        """Validate SMS webhook ID."""
        if not v or not v.strip():
            raise ValueError("SMS webhook ID cannot be empty")
        return v.strip()

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        """Validate webhook name."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Webhook name cannot be empty")
        return v.strip() if v else v

    def to_request_body(self) -> Dict[str, Any]:
        """Convert to request body dict."""
        body = {}
        if self.url is not None:
            body["url"] = str(self.url)
        if self.name is not None:
            body["name"] = self.name
        if self.events is not None:
            body["events"] = [event.value for event in self.events]
        if self.enabled is not None:
            body["enabled"] = self.enabled
        return body


class SmsWebhookDeleteRequest(BaseModel):
    """Request model for deleting an SMS webhook."""

    sms_webhook_id: str = Field(..., min_length=1, description="SMS Webhook ID")

    @field_validator("sms_webhook_id")
    @classmethod
    def validate_sms_webhook_id(cls, v):
        """Validate SMS webhook ID."""
        if not v or not v.strip():
            raise ValueError("SMS webhook ID cannot be empty")
        return v.strip()


# Response Models
class SmsWebhook(BaseModel):
    """SMS webhook model."""

    id: str = Field(..., description="SMS webhook ID")
    url: str = Field(..., description="Webhook URL")
    name: str = Field(..., description="Webhook name")
    events: List[str] = Field(..., description="List of subscribed events")
    enabled: bool = Field(..., description="Whether webhook is enabled")
    sms_number_id: str = Field(..., description="SMS number ID")
    signing_secret: Optional[str] = Field(
        None, description="Signing secret for webhook verification"
    )
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
