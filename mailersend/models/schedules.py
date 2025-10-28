from typing import List, Optional, Literal
from pydantic import field_validator, Field

from .base import BaseModel


class SchedulesListQueryParams(BaseModel):
    """Model for schedules list query parameters with validation."""

    domain_id: Optional[str] = None
    status: Optional[Literal["scheduled", "sent", "error"]] = None
    page: Optional[int] = Field(default=1, ge=1)
    limit: Optional[int] = Field(default=25, ge=10, le=100)

    @field_validator("domain_id")
    @classmethod
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


class SchedulesListRequest(BaseModel):
    """Request model for listing scheduled messages."""

    query_params: SchedulesListQueryParams

    def to_query_params(self) -> dict:
        """Convert query parameters for API request."""
        return self.query_params.to_query_params()


class ScheduleGetRequest(BaseModel):
    """Request model for getting a single scheduled message."""

    message_id: str

    @field_validator("message_id")
    @classmethod
    def validate_message_id(cls, v):
        """Validate message ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Message ID is required")
        return v.strip()


class ScheduleDeleteRequest(BaseModel):
    """Request model for deleting a scheduled message."""

    message_id: str

    @field_validator("message_id")
    @classmethod
    def validate_message_id(cls, v):
        """Validate message ID is provided and not empty."""
        if not v or not v.strip():
            raise ValueError("Message ID is required")
        return v.strip()
