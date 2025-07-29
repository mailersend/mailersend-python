from typing import List, Optional, Literal
from pydantic import field_validator, Field

from .base import BaseModel as MailerSendBaseModel


class SchedulesListQueryParams(MailerSendBaseModel):
    """Model for schedules list query parameters with validation."""

    domain_id: Optional[str] = None
    status: Optional[Literal["scheduled", "sent", "error"]] = None
    page: Optional[int] = Field(default=1, ge=1)
    limit: Optional[int] = Field(default=25, ge=10, le=100)

    @field_validator("domain_id")
    def validate_domain_id(cls, v):
        """Validate domain ID is not empty if provided."""
        if v is not None and not v.strip():
            raise ValueError("Domain ID cannot be empty")
        return v.strip() if v else None

    def to_query_params(self) -> dict:
        """Convert to query parameters for API request."""
        params = {
            "domain_id": self.domain_id,
            "status": self.status,
            "page": self.page,
            "limit": self.limit,
        }

        return {k: v for k, v in params.items() if v is not None}


class SchedulesListRequest(MailerSendBaseModel):
    """Request model for listing scheduled messages."""

    query_params: SchedulesListQueryParams

    def to_query_params(self) -> dict:
        """Convert query parameters for API request."""
        return self.query_params.to_query_params()


class ScheduleGetRequest(MailerSendBaseModel):
    """Request model for getting a single scheduled message."""

    message_id: str

    @field_validator("message_id")
    def validate_message_id(cls, v):
        """Validate message ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Message ID is required")
        return v.strip()


class ScheduleDeleteRequest(MailerSendBaseModel):
    """Request model for deleting a scheduled message."""

    message_id: str

    @field_validator("message_id")
    def validate_message_id(cls, v):
        """Validate message ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Message ID is required")
        return v.strip()


class ScheduleDomain(MailerSendBaseModel):
    """Model representing a domain in scheduled message response."""

    id: str
    name: str
    created_at: str
    updated_at: str


class ScheduleMessage(MailerSendBaseModel):
    """Model representing a message in scheduled message response."""

    id: str
    created_at: str
    updated_at: str


class ScheduledMessage(MailerSendBaseModel):
    """Model representing a scheduled message."""

    message_id: str
    subject: str
    send_at: str
    status: Literal["scheduled", "sent", "error"]
    status_message: Optional[str] = None
    created_at: str
    domain: Optional[ScheduleDomain] = None
    message: Optional[ScheduleMessage] = None


class SchedulesListResponse(MailerSendBaseModel):
    """Response model for scheduled messages list."""

    data: List[ScheduledMessage]
    links: Optional[dict] = None
    meta: Optional[dict] = None


class ScheduleResponse(MailerSendBaseModel):
    """Response model for single scheduled message."""

    data: ScheduledMessage
