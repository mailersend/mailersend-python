from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator, model_validator
import time

from .base import BaseModel as MailerSendBaseModel


class AnalyticsRequest(MailerSendBaseModel):
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
    event: Optional[List[Literal[
        "queued", "sent", "delivered", "soft_bounced", "hard_bounced", 
        "opened", "clicked", "unsubscribed", "spam_complaints", 
        "survey_opened", "survey_submitted", "opened_unique", "clicked_unique"
    ]]] = Field(None, alias="event[]")
    
    @field_validator('date_from', 'date_to')
    def validate_timestamps(cls, v):
        """Validate that timestamps are positive integers."""
        if v <= 0:
            raise ValueError("Timestamp must be a positive integer")
        return v
    
    @model_validator(mode='after')
    def validate_date_range(cls, v):
        """Validate that date_from is before date_to."""
        if v.date_from >= v.date_to:
            raise ValueError("date_from must be lower than date_to")
        return v
    
    @field_validator('recipient_id')
    def validate_recipient_count(cls, v):
        """Validate recipient count limit."""
        if v and len(v) > 50:
            raise ValueError("Maximum 50 recipients are allowed")
        return v
    
    @field_validator('tags')
    def validate_tags(cls, v):
        """Validate tags format."""
        if v:
            for tag in v:
                if not isinstance(tag, str) or not tag.strip():
                    raise ValueError("All tags must be non-empty strings")
        return v


class AnalyticsDateStats(MailerSendBaseModel):
    """Model for date-based analytics stats."""
    date: str
    queued: int = 0
    sent: int = 0
    delivered: int = 0
    opened: int = 0
    clicked: int = 0
    soft_bounced: int = 0
    hard_bounced: int = 0
    unsubscribed: int = 0
    spam_complaints: int = 0
    opened_unique: int = 0
    clicked_unique: int = 0
    survey_opened: int = 0
    survey_submitted: int = 0


class AnalyticsDateResponse(MailerSendBaseModel):
    """Response model for date analytics."""
    date_from: str
    date_to: str
    group_by: str
    stats: List[AnalyticsDateStats]


class AnalyticsCountryStats(MailerSendBaseModel):
    """Model for country-based analytics stats."""
    name: str  # 2-letter country code
    count: int


class AnalyticsCountryResponse(MailerSendBaseModel):
    """Response model for country analytics."""
    date_from: int
    date_to: int
    stats: List[AnalyticsCountryStats]


class AnalyticsUserAgentStats(MailerSendBaseModel):
    """Model for user agent analytics stats."""
    name: str  # User agent name (Chrome, Firefox, etc.)
    count: int


class AnalyticsUserAgentResponse(MailerSendBaseModel):
    """Response model for user agent analytics."""
    date_from: int
    date_to: int
    stats: List[AnalyticsUserAgentStats]


class AnalyticsReadingEnvironmentStats(MailerSendBaseModel):
    """Model for reading environment analytics stats."""
    name: Literal["webmail", "mobile", "desktop"]
    count: int


class AnalyticsReadingEnvironmentResponse(MailerSendBaseModel):
    """Response model for reading environment analytics."""
    date_from: int
    date_to: int
    stats: List[AnalyticsReadingEnvironmentStats] 