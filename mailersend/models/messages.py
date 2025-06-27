from typing import List, Optional, Any
from pydantic import field_validator

from .base import BaseModel as MailerSendBaseModel
from .domains import Domain, DomainSettings


class MessagesListRequest(MailerSendBaseModel):
    """Request model for listing messages."""
    
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


class MessageGetRequest(MailerSendBaseModel):
    """Request model for getting a single message."""
    
    message_id: str
    
    @field_validator('message_id')
    def validate_message_id(cls, v):
        """Validate message ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Message ID is required")
        return v.strip()


class Email(MailerSendBaseModel):
    """Model representing an email within a message."""
    
    # Based on the API documentation, the emails array structure is not detailed
    # This is a placeholder that can be expanded when more information is available
    pass


class Message(MailerSendBaseModel):
    """Model representing a message."""
    
    id: str
    created_at: str
    updated_at: str
    emails: List[Email] = []
    domain: Optional[Domain] = None


class MessagesListResponse(MailerSendBaseModel):
    """Response model for messages list."""
    
    data: List[Message]
    links: dict
    meta: dict


class MessageResponse(MailerSendBaseModel):
    """Response model for single message."""
    
    data: Message 