"""WhatsApp Recipients models."""

from enum import Enum
from typing import Optional, Dict, Any
from pydantic import Field, field_validator
from .base import BaseModel


class WhatsAppRecipientStatus(str, Enum):
    """WhatsApp recipient status options."""

    ACTIVE = "active"
    INVALID = "invalid"
    SUPPRESSED = "suppressed"
    BLOCKED = "blocked"


class WhatsAppRecipientsListQueryParams(BaseModel):
    """Query parameters for listing WhatsApp recipients."""

    status: Optional[WhatsAppRecipientStatus] = Field(
        None, description="Recipient status filter"
    )
    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(
        default=25, ge=10, le=100, description="Number of results per page"
    )

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict, excluding None and default values."""
        params = {}

        if self.status is not None:
            params["status"] = self.status.value
        if self.page != 1:
            params["page"] = self.page
        if self.limit != 25:
            params["limit"] = self.limit

        return params


class WhatsAppRecipientsListRequest(BaseModel):
    """Request model for listing WhatsApp recipients."""

    query_params: WhatsAppRecipientsListQueryParams = Field(
        default_factory=WhatsAppRecipientsListQueryParams
    )

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict."""
        return self.query_params.to_query_params()


class WhatsAppRecipientGetRequest(BaseModel):
    """Request model for getting a single WhatsApp recipient."""

    whatsapp_recipient_id: str = Field(
        ..., min_length=1, description="WhatsApp recipient ID"
    )

    @field_validator("whatsapp_recipient_id")
    @classmethod
    def validate_whatsapp_recipient_id(cls, v):
        """Validate WhatsApp recipient ID."""
        if not v or not v.strip():
            raise ValueError("WhatsApp recipient ID cannot be empty")
        return v.strip()
