"""WhatsApp Activities models."""

from enum import Enum
from typing import Optional, List, Dict, Any, Union
from pydantic import Field, field_validator, model_validator
from .base import BaseModel


class WhatsAppActivityType(str, Enum):
    """WhatsApp activity type options."""

    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class WhatsAppActivitiesListQueryParams(BaseModel):
    """Query parameters for listing WhatsApp activities."""

    whatsapp_item_id: Optional[str] = Field(None, description="WhatsApp item ID filter")
    whatsapp_message_id: Optional[str] = Field(
        None, description="WhatsApp message ID filter"
    )
    recipient: Optional[str] = Field(
        None, description="Recipient phone number, WhatsApp username or BSUID filter"
    )
    type: Optional[List[WhatsAppActivityType]] = Field(
        None, description="Activity type filter"
    )
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

    @field_validator("whatsapp_item_id", "whatsapp_message_id", "recipient")
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

        if self.whatsapp_item_id is not None:
            params["whatsapp_item_id"] = self.whatsapp_item_id
        if self.whatsapp_message_id is not None:
            params["whatsapp_message_id"] = self.whatsapp_message_id
        if self.recipient is not None:
            params["recipient"] = self.recipient
        if self.type:
            params["type[]"] = [activity_type.value for activity_type in self.type]
        if self.date_from is not None:
            params["date_from"] = self.date_from
        if self.date_to is not None:
            params["date_to"] = self.date_to
        if self.page != 1:
            params["page"] = self.page
        if self.limit != 25:
            params["limit"] = self.limit

        return params


class WhatsAppActivitiesListRequest(BaseModel):
    """Request model for listing WhatsApp activities."""

    query_params: WhatsAppActivitiesListQueryParams = Field(
        default_factory=WhatsAppActivitiesListQueryParams
    )

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict."""
        return self.query_params.to_query_params()
