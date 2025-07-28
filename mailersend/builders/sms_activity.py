"""
SMS Activity API builder.
"""
from typing import Optional, List

from ..models.sms_activity import (
    SmsActivityListRequest, SmsMessageGetRequest
)


class SmsActivityBuilder:
    """Builder for SMS Activity API requests."""
    
    def __init__(self):
        """Initialize SMS Activity builder."""
        self.reset()
    
    def reset(self) -> 'SmsActivityBuilder':
        """Reset builder state."""
        self._sms_number_id = None
        self._date_from = None
        self._date_to = None
        self._status = None
        self._page = None
        self._limit = None
        self._sms_message_id = None
        return self
    
    def sms_number_id(self, sms_number_id: str) -> 'SmsActivityBuilder':
        """Set SMS number ID filter."""
        self._sms_number_id = sms_number_id
        return self
    
    def date_from(self, date_from: int) -> 'SmsActivityBuilder':
        """Set date from filter (Unix timestamp)."""
        self._date_from = date_from
        return self
    
    def date_to(self, date_to: int) -> 'SmsActivityBuilder':
        """Set date to filter (Unix timestamp)."""
        self._date_to = date_to
        return self
    
    def status(self, status: List[str]) -> 'SmsActivityBuilder':
        """Set status filter."""
        self._status = status
        return self
    
    def page(self, page: int) -> 'SmsActivityBuilder':
        """Set page number."""
        self._page = page
        return self
    
    def limit(self, limit: int) -> 'SmsActivityBuilder':
        """Set page limit."""
        self._limit = limit
        return self
    
    def sms_message_id(self, sms_message_id: str) -> 'SmsActivityBuilder':
        """Set SMS message ID."""
        self._sms_message_id = sms_message_id
        return self
    
    def build_list_request(self) -> SmsActivityListRequest:
        """Build SMS activity list request."""
        return SmsActivityListRequest(
            sms_number_id=self._sms_number_id,
            date_from=self._date_from,
            date_to=self._date_to,
            status=self._status,
            page=self._page,
            limit=self._limit
        )
    
    def build_get_request(self) -> SmsMessageGetRequest:
        """Build SMS message get request."""
        if not self._sms_message_id:
            raise ValueError("SMS message ID must be set")
        
        return SmsMessageGetRequest(
            sms_message_id=self._sms_message_id
        )