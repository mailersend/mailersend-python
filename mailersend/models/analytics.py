from typing import List, Optional, Literal
from pydantic import Field, field_validator, model_validator

from .base import BaseModel


class AnalyticsRequest(BaseModel):
    """
    Request model for Analytics API endpoints.

    This model handles all analytics endpoints since they share similar parameters:
    - Activity data by date
    - Opens by country
    - Opens by user-agent name
    - Opens by reading environment
    """

    domain_id: Optional[str] = None
    recipient_id: Optional[List[str]] = Field(None, alias="recipient_id[]")
    date_from: int
    date_to: int
    tags: Optional[List[str]] = Field(None, alias="tags[]")

    # Date endpoint specific parameters
    group_by: Optional[Literal["days", "weeks", "months", "years"]] = "days"
    event: Optional[
        List[
            Literal[
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
                "opened_unique",
                "clicked_unique",
            ]
        ]
    ] = Field(None, alias="event[]")

    @field_validator("date_from", "date_to")
    @classmethod
    def validate_timestamps(cls, v):
        """Validate that timestamps are positive integers."""
        if v <= 0:
            raise ValueError("Timestamp must be a positive integer")
        return v

    @model_validator(mode="after")
    def validate_date_range(self):
        """Validate that date_from is before date_to."""
        if self.date_from >= self.date_to:
            raise ValueError("date_from must be lower than date_to")
        return self

    @field_validator("recipient_id")
    @classmethod
    def validate_recipient_count(cls, v):
        """Validate recipient count limit."""
        if v and len(v) > 50:
            raise ValueError("Maximum 50 recipients are allowed")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v):
        """Validate tags format."""
        if v:
            for tag in v:
                if not isinstance(tag, str) or not tag.strip():
                    raise ValueError("All tags must be non-empty strings")
        return v
