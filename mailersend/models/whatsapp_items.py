"""WhatsApp Items models."""

from enum import Enum
from typing import Optional, List, Dict, Any, Union
from pydantic import Field, field_validator, model_validator
from .base import BaseModel


class WhatsAppItemStatus(str, Enum):
    """WhatsApp item status options."""

    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class WhatsAppItemsListQueryParams(BaseModel):
    """Query parameters for listing WhatsApp items."""

    recipient: Optional[str] = Field(
        None, description="Recipient phone number, WhatsApp username or BSUID filter"
    )
    whatsapp_message_id: Optional[str] = Field(
        None, description="WhatsApp message ID filter"
    )
    status: Optional[List[WhatsAppItemStatus]] = Field(
        None, description="Item status filter"
    )
    whatsapp_account_id: Optional[str] = Field(
        None, description="WhatsApp account (sender) ID filter"
    )
    from_: Optional[str] = Field(
        None, alias="from", description="Sender phone number filter"
    )
    template_id: Optional[str] = Field(None, description="Template ID filter")
    date_from: Optional[Union[int, str]] = Field(
        None, description="Unix timestamp or ISO 8601 datetime (exclusive)"
    )
    date_to: Optional[Union[int, str]] = Field(
        None, description="Unix timestamp or ISO 8601 datetime (exclusive)"
    )
    page: int = Field(default=1, ge=1, le=100, description="Page number")
    limit: int = Field(
        default=25, ge=1, le=100, description="Number of results per page"
    )

    @field_validator(
        "recipient",
        "whatsapp_message_id",
        "whatsapp_account_id",
        "from_",
        "template_id",
    )
    @classmethod
    def strip_filter(cls, v: Optional[str]) -> Optional[str]:
        """Strip whitespace from string filters."""
        if v is not None:
            return v.strip()
        return v

    @model_validator(mode="after")
    def validate_date_range(self):
        """Validate date_to is after date_from when both are Unix timestamps."""
        if (
            isinstance(self.date_from, int)
            and isinstance(self.date_to, int)
            and self.date_to <= self.date_from
        ):
            raise ValueError("date_to must be greater than date_from")
        return self

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict, excluding None and default values."""
        params = {}

        if self.recipient is not None:
            params["recipient"] = self.recipient
        if self.whatsapp_message_id is not None:
            params["whatsapp_message_id"] = self.whatsapp_message_id
        if self.status:
            params["status[]"] = [item_status.value for item_status in self.status]
        if self.whatsapp_account_id is not None:
            params["whatsapp_account_id"] = self.whatsapp_account_id
        if self.from_ is not None:
            params["from"] = self.from_
        if self.template_id is not None:
            params["template_id"] = self.template_id
        if self.date_from is not None:
            params["date_from"] = self.date_from
        if self.date_to is not None:
            params["date_to"] = self.date_to
        if self.page != 1:
            params["page"] = self.page
        if self.limit != 25:
            params["limit"] = self.limit

        return params


class WhatsAppItemsListRequest(BaseModel):
    """Request model for listing WhatsApp items."""

    query_params: WhatsAppItemsListQueryParams = Field(
        default_factory=WhatsAppItemsListQueryParams
    )

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict."""
        return self.query_params.to_query_params()


class WhatsAppItemGetRequest(BaseModel):
    """Request model for getting a single WhatsApp item."""

    whatsapp_item_id: str = Field(..., min_length=1, description="WhatsApp item ID")

    @field_validator("whatsapp_item_id")
    @classmethod
    def validate_whatsapp_item_id(cls, v):
        """Validate WhatsApp item ID."""
        if not v or not v.strip():
            raise ValueError("WhatsApp item ID cannot be empty")
        return v.strip()
