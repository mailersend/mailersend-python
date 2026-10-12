"""WhatsApp Inbound Messages models."""

from enum import Enum
from typing import Optional, List, Dict, Any, Union
from pydantic import Field, field_validator, model_validator
from .base import BaseModel


class WhatsAppInboundMessageType(str, Enum):
    """WhatsApp inbound message type options."""

    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    STICKER = "sticker"
    LOCATION = "location"
    CONTACTS = "contacts"
    INTERACTIVE = "interactive"
    BUTTON = "button"
    ORDER = "order"
    REACTION = "reaction"
    SYSTEM = "system"
    UNKNOWN = "unknown"
    UNSUPPORTED = "unsupported"


class WhatsAppInboundMessagesListQueryParams(BaseModel):
    """Query parameters for listing WhatsApp inbound messages."""

    whatsapp_account_id: Optional[str] = Field(
        None, description="WhatsApp account (sender) ID filter"
    )
    type: Optional[List[WhatsAppInboundMessageType]] = Field(
        None, description="Message type filter"
    )
    date_from: Optional[Union[int, str]] = Field(
        None, description="Unix timestamp or ISO 8601 datetime (exclusive)"
    )
    date_to: Optional[Union[int, str]] = Field(
        None, description="Unix timestamp or ISO 8601 datetime (exclusive)"
    )
    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(
        default=25, ge=10, le=100, description="Number of results per page"
    )

    @field_validator("whatsapp_account_id")
    @classmethod
    def validate_whatsapp_account_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean whatsapp_account_id."""
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

        if self.whatsapp_account_id is not None:
            params["whatsapp_account_id"] = self.whatsapp_account_id
        if self.type:
            params["type[]"] = [message_type.value for message_type in self.type]
        if self.date_from is not None:
            params["date_from"] = self.date_from
        if self.date_to is not None:
            params["date_to"] = self.date_to
        if self.page != 1:
            params["page"] = self.page
        if self.limit != 25:
            params["limit"] = self.limit

        return params


class WhatsAppInboundMessagesListRequest(BaseModel):
    """Request model for listing WhatsApp inbound messages."""

    query_params: WhatsAppInboundMessagesListQueryParams = Field(
        default_factory=WhatsAppInboundMessagesListQueryParams
    )

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict."""
        return self.query_params.to_query_params()


class WhatsAppInboundMessageGetRequest(BaseModel):
    """Request model for getting a single WhatsApp inbound message."""

    whatsapp_inbound_message_id: str = Field(
        ..., min_length=1, description="WhatsApp inbound message ID"
    )

    @field_validator("whatsapp_inbound_message_id")
    @classmethod
    def validate_whatsapp_inbound_message_id(cls, v):
        """Validate WhatsApp inbound message ID."""
        if not v or not v.strip():
            raise ValueError("WhatsApp inbound message ID cannot be empty")
        return v.strip()
