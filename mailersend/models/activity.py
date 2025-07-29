from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, EmailStr, ConfigDict

from .base import BaseModel as BaseMailerSendModel


class ActivityRecipient(BaseModel):
    """Model for activity recipient information."""

    id: str
    email: EmailStr
    created_at: str
    updated_at: str
    deleted_at: Optional[str] = None

    model_config = ConfigDict(validate_by_name=True)


class ActivityEmail(BaseModel):
    """Model for activity email information."""

    id: str
    from_email: EmailStr = Field(alias="from")
    subject: str
    text: Optional[str] = None
    html: Optional[str] = None
    status: str
    tags: Optional[List[str]] = None
    created_at: str
    updated_at: str
    recipient: ActivityRecipient

    model_config = ConfigDict(validate_by_name=True)


class Activity(BaseModel):
    """Model for activity data."""

    id: str
    created_at: str
    updated_at: str
    type: str  # Activity type (queued, sent, delivered, etc.)
    email: ActivityEmail

    model_config = ConfigDict(validate_by_name=True)


class ActivityQueryParams(BaseModel):
    """Model for activity query parameters with validation."""

    page: Optional[int] = Field(default=1, ge=1)
    limit: Optional[int] = Field(default=25, ge=10, le=100)
    date_from: int  # Unix timestamp
    date_to: int  # Unix timestamp
    event: Optional[List[str]] = None

    model_config = ConfigDict(validate_by_name=True)

    def model_post_init(self, __context: Any) -> None:
        """Post-initialization validation."""
        # Validate date range
        if self.date_to <= self.date_from:
            raise ValueError("date_to must be greater than date_from")

        # Validate timeframe (max 7 days = 604800 seconds)
        if (self.date_to - self.date_from) > 604800:
            raise ValueError(
                "Timeframe between date_from and date_to cannot exceed 7 days"
            )

        # Validate event types if provided
        if self.event:
            valid_events = {
                "queued",
                "sent",
                "delivered",
                "soft_bounced",
                "hard_bounced",
                "opened",
                "clicked",
                "unsubscribed",
                "spam_complaints",
                "survey_opened",
                "survey_submitted",
            }
            invalid_events = set(self.event) - valid_events
            if invalid_events:
                raise ValueError(f"Invalid event types: {invalid_events}")

    def to_query_params(self) -> dict:
        """Convert to query parameters for API request."""
        params = {
            "page": self.page,
            "limit": self.limit,
            "date_from": self.date_from,
            "date_to": self.date_to,
        }

        if self.event:
            # Convert event list to query parameter format
            for i, event in enumerate(self.event):
                params[f"event[{i}]"] = event

        return {k: v for k, v in params.items() if v is not None}


class ActivityRequest(BaseModel):
    """Model for activity request with domain_id (path param) and query parameters."""

    domain_id: str  # Path parameter
    query_params: ActivityQueryParams  # Query parameters

    model_config = ConfigDict(validate_by_name=True)

    def to_query_params(self) -> dict:
        """Convert query parameters for API request."""
        return self.query_params.to_query_params()


class SingleActivityRequest(BaseModel):
    """Model for getting a single activity by ID."""

    activity_id: str

    model_config = ConfigDict(validate_by_name=True)

    def model_post_init(self, __context: Any) -> None:
        """Post-initialization validation."""
        if not self.activity_id or not self.activity_id.strip():
            raise ValueError("activity_id cannot be empty")
        # Strip whitespace
        self.activity_id = self.activity_id.strip()


class ActivityListResponse(BaseMailerSendModel):
    """Response model for activity list."""
    
    data: List[Activity] = Field(..., description="List of activities")
    links: Dict[str, Optional[str]]
    meta: Dict[str, Any]


class SingleActivityResponse(BaseMailerSendModel):
    """Response model for single activity."""
    
    data: Activity = Field(..., description="Activity details")
