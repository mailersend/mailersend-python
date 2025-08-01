"""Models for SMS Phone Numbers API."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator

from .base import BaseModel as BaseMailerSendModel


class SmsNumber(BaseMailerSendModel):
    """SMS Phone Number model."""

    id: str
    telephone_number: str
    paused: bool
    created_at: datetime


class SmsNumbersListRequest(BaseMailerSendModel):
    """Request model for listing SMS phone numbers."""

    paused: Optional[bool] = None
    page: Optional[int] = None
    limit: Optional[int] = None

    def to_query_params(self) -> Dict[str, Any]:
        """Convert to query parameters."""
        params = {}
        if self.paused is not None:
            params["paused"] = str(self.paused).lower()
        if self.page is not None:
            params["page"] = self.page
        if self.limit is not None:
            params["limit"] = self.limit
        return params


class SmsNumberGetRequest(BaseMailerSendModel):
    """Request model for getting a specific SMS phone number."""

    sms_number_id: str = Field(..., min_length=1, description="SMS Number ID")


class SmsNumberUpdateRequest(BaseMailerSendModel):
    """Request model for updating an SMS phone number."""

    sms_number_id: str = Field(..., min_length=1, description="SMS Number ID")
    paused: Optional[bool] = None

    def to_json(self) -> Dict[str, Any]:
        """Convert to JSON payload."""
        payload = {}
        if self.paused is not None:
            payload["paused"] = self.paused
        return payload


class SmsNumberDeleteRequest(BaseMailerSendModel):
    """Request model for deleting an SMS phone number."""

    sms_number_id: str = Field(..., min_length=1, description="SMS Number ID")
