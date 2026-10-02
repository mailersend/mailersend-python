"""WhatsApp Messages models."""

from typing import Dict, Any
from pydantic import Field, field_validator
from .base import BaseModel


class WhatsAppMessagesListQueryParams(BaseModel):
    """Query parameters for listing WhatsApp messages."""

    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(
        default=25, ge=10, le=100, description="Number of results per page"
    )

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict, excluding default values."""
        params = {}

        if self.page != 1:
            params["page"] = self.page
        if self.limit != 25:
            params["limit"] = self.limit

        return params


class WhatsAppMessagesListRequest(BaseModel):
    """Request model for listing WhatsApp messages."""

    query_params: WhatsAppMessagesListQueryParams = Field(
        default_factory=WhatsAppMessagesListQueryParams
    )

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict."""
        return self.query_params.to_query_params()


class WhatsAppMessageGetRequest(BaseModel):
    """Request model for getting a single WhatsApp message."""

    whatsapp_message_id: str = Field(
        ..., min_length=1, description="WhatsApp message ID"
    )

    @field_validator("whatsapp_message_id")
    @classmethod
    def validate_whatsapp_message_id(cls, v):
        """Validate WhatsApp message ID."""
        if not v or not v.strip():
            raise ValueError("WhatsApp message ID cannot be empty")
        return v.strip()
