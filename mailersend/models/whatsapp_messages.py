"""WhatsApp Messages models."""

from typing import Optional, Dict, Any, Union
from pydantic import Field, field_validator, model_validator
from .base import BaseModel


class WhatsAppMessagesListQueryParams(BaseModel):
    """Query parameters for listing WhatsApp messages."""

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

    @field_validator("whatsapp_account_id", "from_", "template_id")
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
