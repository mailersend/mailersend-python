from typing import List, Optional, Any
from pydantic import field_validator, Field

from .base import BaseModel as MailerSendBaseModel



class MessagesListQueryParams(MailerSendBaseModel):
    """Model for messages list query parameters with validation."""

    page: Optional[int] = Field(default=1, ge=1)
    limit: Optional[int] = Field(default=25, ge=10, le=100)

    def to_query_params(self) -> dict:
        """Convert to query parameters for API request."""
        params = {"page": self.page, "limit": self.limit}

        return {k: v for k, v in params.items() if v is not None}


class MessagesListRequest(MailerSendBaseModel):
    """Request model for listing messages."""

    query_params: MessagesListQueryParams

    def to_query_params(self) -> dict:
        """Convert query parameters for API request."""
        return self.query_params.to_query_params()


class MessageGetRequest(MailerSendBaseModel):
    """Request model for getting a single message."""

    message_id: str

    @field_validator("message_id")
    def validate_message_id(cls, v):
        """Validate message ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Message ID is required")
        return v.strip()



