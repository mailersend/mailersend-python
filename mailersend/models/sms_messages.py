"""SMS Messages models."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

from .base import BaseModel as BaseMailerSendModel


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


# Response Models
class SmsActivity(BaseMailerSendModel):
    """SMS Activity model."""

    from_: str = Field(..., alias="from", description="Sender phone number")
    to: str = Field(..., description="Recipient phone number")
    created_at: datetime = Field(..., description="Creation timestamp")
    status: str = Field(..., description="SMS activity status")
    sms_message_id: str = Field(..., description="SMS message ID")


class Sms(BaseMailerSendModel):
    """Individual SMS model."""

    id: str = Field(..., description="SMS ID")
    from_: str = Field(..., alias="from", description="Sender phone number")
    to: str = Field(..., description="Recipient phone number")
    text: str = Field(..., description="SMS text content")
    compiled_text: str = Field(..., description="Compiled SMS text")
    status: str = Field(..., description="SMS status")
    segment_count: int = Field(..., description="Number of SMS segments")
    error_type: Optional[str] = Field(None, description="Error type if any")
    error_description: Optional[str] = Field(
        None, description="Error description if any"
    )
    created_at: datetime = Field(..., description="Creation timestamp")


class SmsMessage(BaseMailerSendModel):
    """SMS Message model."""

    id: str = Field(..., description="SMS Message ID")
    from_: str = Field(..., alias="from", description="Sender phone number")
    to: List[str] = Field(..., description="List of recipient phone numbers")
    text: str = Field(..., description="SMS text content")
    paused: bool = Field(..., description="Whether the SMS is paused")
    created_at: datetime = Field(..., description="Creation timestamp")
    sms: Optional[List[Sms]] = Field(None, description="Individual SMS objects")
    sms_activity: Optional[List[SmsActivity]] = Field(
        None, description="SMS activity objects"
    )


class SmsMessagesListResponse(BaseMailerSendModel):
    """Response model for SMS messages list."""

    data: List[SmsMessage] = Field(..., description="List of SMS messages")
    links: Optional[Dict[str, str]] = Field(None, description="Pagination links")
    meta: Optional[Dict[str, int]] = Field(None, description="Pagination metadata")


class SmsMessageResponse(BaseMailerSendModel):
    """Response model for single SMS message."""

    data: SmsMessage = Field(..., description="SMS message data")
