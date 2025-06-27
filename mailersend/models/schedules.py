from typing import List, Optional, Literal
from pydantic import field_validator

from .base import BaseModel as MailerSendBaseModel


class SchedulesListRequest(MailerSendBaseModel):
    """Request model for listing scheduled messages."""
    
    domain_id: Optional[str] = None
    status: Optional[Literal["scheduled", "sent", "error"]] = None
    page: Optional[int] = None
    limit: Optional[int] = 25
    
    @field_validator('limit')
    def validate_limit(cls, v):
        """Validate limit is within acceptable range."""
        if v is not None and (v < 10 or v > 100):
            raise ValueError("Limit must be between 10 and 100")
        return v
    
    @field_validator('page')
    def validate_page(cls, v):
        """Validate page is positive."""
        if v is not None and v < 1:
            raise ValueError("Page must be greater than 0")
        return v
    
    @field_validator('domain_id')
    def validate_domain_id(cls, v):
        """Validate domain ID is not empty if provided."""
        if v is not None and not v.strip():
            raise ValueError("Domain ID cannot be empty")
        return v.strip() if v else None


class ScheduleGetRequest(MailerSendBaseModel):
    """Request model for getting a single scheduled message."""
    
    message_id: str
    
    @field_validator('message_id')
    def validate_message_id(cls, v):
        """Validate message ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Message ID is required")
        return v.strip()


class ScheduleDeleteRequest(MailerSendBaseModel):
    """Request model for deleting a scheduled message."""
    
    message_id: str
    
    @field_validator('message_id')
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