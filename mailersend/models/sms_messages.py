"""SMS Messages models."""

from typing import Dict, Any
from pydantic import Field, field_validator
from .base import BaseModel


class SmsMessagesListQueryParams(BaseModel):
    """Query parameters for listing SMS messages."""

    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(
        default=25, ge=10, le=100, description="Number of results per page"
    )

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict, excluding default values."""
        params = {}

        # Only include non-default values
        if self.page != 1:
            params["page"] = self.page
        if self.limit != 25:
            params["limit"] = self.limit

        return params


class SmsMessagesListRequest(BaseModel):
    """Request model for listing SMS messages."""

    query_params: SmsMessagesListQueryParams = Field(
        default_factory=SmsMessagesListQueryParams
    )

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict."""
        return self.query_params.to_query_params()


class SmsMessageGetRequest(BaseModel):
    """Request model for getting a single SMS message."""

    sms_message_id: str = Field(..., min_length=1, description="SMS Message ID")

    @field_validator("sms_message_id")
    @classmethod
    def validate_sms_message_id(cls, v):
        """Validate SMS message ID."""
        if not v or not v.strip():
            raise ValueError("SMS message ID cannot be empty")
        return v.strip()
