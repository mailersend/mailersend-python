"""SMS Recipients models."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from enum import Enum

from .base import BaseModel as BaseMailerSendModel


class SmsRecipientStatus(str, Enum):
    """SMS recipient status options."""

    ACTIVE = "active"
    OPT_OUT = "opt_out"


# Query Parameters Models
class SmsRecipientsListQueryParams(BaseModel):
    """Query parameters for listing SMS recipients."""

    status: Optional[SmsRecipientStatus] = Field(
        None, description="Recipient status filter"
    )
    sms_number_id: Optional[str] = Field(None, description="SMS number ID filter")
    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(
        default=25, ge=10, le=100, description="Number of results per page"
    )

    @field_validator("sms_number_id")
    @classmethod
    def validate_sms_number_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean sms_number_id."""
        if v is not None:
            return v.strip()
        return v

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict, excluding None values."""
        params = {}

        if self.status is not None:
            params["status"] = self.status.value
        if self.sms_number_id is not None:
            params["sms_number_id"] = self.sms_number_id
        if self.page != 1:
            params["page"] = self.page
        if self.limit != 25:
            params["limit"] = self.limit

        return params


# Request Models
class SmsRecipientsListRequest(BaseModel):
    """Request model for listing SMS recipients."""

    query_params: SmsRecipientsListQueryParams = Field(
        default_factory=SmsRecipientsListQueryParams
    )

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters dict."""
        return self.query_params.to_query_params()


class SmsRecipientGetRequest(BaseModel):
    """Request model for getting a single SMS recipient."""

    sms_recipient_id: str = Field(..., min_length=1, description="SMS Recipient ID")

    @field_validator("sms_recipient_id")
    @classmethod
    def validate_sms_recipient_id(cls, v):
        """Validate SMS recipient ID."""
        if not v or not v.strip():
            raise ValueError("SMS recipient ID cannot be empty")
        return v.strip()


class SmsRecipientUpdateRequest(BaseModel):
    """Request model for updating an SMS recipient."""

    sms_recipient_id: str = Field(..., min_length=1, description="SMS Recipient ID")
    status: SmsRecipientStatus = Field(..., description="New recipient status")

    @field_validator("sms_recipient_id")
    @classmethod
    def validate_sms_recipient_id(cls, v):
        """Validate SMS recipient ID."""
        if not v or not v.strip():
            raise ValueError("SMS recipient ID cannot be empty")
        return v.strip()

    def to_request_body(self) -> Dict[str, Any]:
        """Convert to request body dict."""
        return {"status": self.status.value}


# Response Models
class SmsMessage(BaseMailerSendModel):
    """SMS message model for recipient details."""

    id: str = Field(..., description="SMS message ID")
    from_: str = Field(..., alias="from", description="Sender phone number")
    to: str = Field(..., description="Recipient phone number")
    text: str = Field(..., description="SMS message text")
    status: str = Field(..., description="SMS message status")
    segment_count: int = Field(..., description="Number of SMS segments")
    error_type: Optional[str] = Field(None, description="Error type if any")
    error_description: Optional[str] = Field(
        None, description="Error description if any"
    )
    created_at: datetime = Field(..., description="Creation timestamp")


class SmsRecipient(BaseMailerSendModel):
    """SMS recipient model."""

    id: str = Field(..., description="SMS recipient ID")
    number: str = Field(..., description="Phone number")
    status: str = Field(..., description="Recipient status")
    created_at: datetime = Field(..., description="Creation timestamp")


class SmsRecipientDetails(SmsRecipient):
    """SMS recipient with detailed information including SMS history."""

    sms: List[SmsMessage] = Field(
        default_factory=list, description="SMS messages sent to this recipient"
    )


class SmsRecipientsListResponse(BaseMailerSendModel):
    """Response model for SMS recipients list."""

    data: List[SmsRecipient] = Field(..., description="List of SMS recipients")
    links: Dict[str, Optional[str]]
    meta: Dict[str, Any]


class SmsRecipientGetResponse(BaseMailerSendModel):
    """Response model for single SMS recipient."""

    data: SmsRecipientDetails = Field(..., description="SMS recipient details")


class SmsRecipientUpdateResponse(BaseMailerSendModel):
    """Response model for SMS recipient update."""

    data: SmsRecipient = Field(..., description="Updated SMS recipient")
