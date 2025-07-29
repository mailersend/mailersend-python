"""
SMS Activity API models.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import Field

from .base import BaseModel as MailerSendBaseModel


class SmsActivity(MailerSendBaseModel):
    """SMS Activity model."""

    from_: str = Field(..., alias="from")
    to: str
    created_at: datetime
    content: str
    status: str
    sms_message_id: str


class SmsActivityListRequest(MailerSendBaseModel):
    """Request model for listing SMS activities."""

    sms_number_id: Optional[str] = None
    date_from: Optional[int] = None
    date_to: Optional[int] = None
    status: Optional[List[str]] = None
    page: Optional[int] = None
    limit: Optional[int] = None

    def to_query_params(self) -> dict:
        """Convert to query parameters."""
        params = {}

        if self.sms_number_id is not None:
            params["sms_number_id"] = self.sms_number_id

        if self.date_from is not None:
            params["date_from"] = self.date_from

        if self.date_to is not None:
            params["date_to"] = self.date_to

        if self.status is not None:
            # Convert list to multiple status[] parameters
            for status_value in self.status:
                if "status[]" not in params:
                    params["status[]"] = []
                params["status[]"].append(status_value)

        if self.page is not None:
            params["page"] = self.page

        if self.limit is not None:
            params["limit"] = self.limit

        return params


class SmsMessageGetRequest(MailerSendBaseModel):
    """Request model for getting SMS message activity."""

    sms_message_id: str = Field(..., min_length=1)


class SmsMessage(MailerSendBaseModel):
    """SMS Message model."""

    id: str
    from_: str = Field(..., alias="from")
    to: List[str]
    text: str
    paused: bool
    created_at: datetime
    sms: List[dict]
    sms_activity: List[SmsActivity]
