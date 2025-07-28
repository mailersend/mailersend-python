"""SMS Recipients builder for MailerSend SDK."""
from typing import Optional

from ..models.sms_recipients import (
    SmsRecipientsListRequest,
    SmsRecipientsListQueryParams,
    SmsRecipientGetRequest,
    SmsRecipientUpdateRequest,
    SmsRecipientStatus,
)


class SmsRecipientsBuilder:
    """Builder for SMS Recipients API requests."""

    def __init__(self) -> None:
        """Initialize the SmsRecipientsBuilder."""
        self._status: Optional[SmsRecipientStatus] = None
        self._sms_number_id: Optional[str] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        self._sms_recipient_id: Optional[str] = None

    def status(self, status: SmsRecipientStatus) -> "SmsRecipientsBuilder":
        """
        Set the status filter for listing SMS recipients.
        
        Args:
            status: Status to filter by (active or opt_out)
            
        Returns:
            SmsRecipientsBuilder: Builder instance for method chaining
        """
        self._status = status
        return self

    def sms_number_id(self, sms_number_id: str) -> "SmsRecipientsBuilder":
        """
        Set the SMS number ID filter for listing SMS recipients.
        
        Args:
            sms_number_id: SMS number ID to filter by
            
        Returns:
            SmsRecipientsBuilder: Builder instance for method chaining
        """
        self._sms_number_id = sms_number_id
        return self

    def page(self, page: int) -> "SmsRecipientsBuilder":
        """
        Set the page number for pagination.
        
        Args:
            page: Page number (must be >= 1)
            
        Returns:
            SmsRecipientsBuilder: Builder instance for method chaining
        """
        self._page = page
        return self

    def limit(self, limit: int) -> "SmsRecipientsBuilder":
        """
        Set the limit for number of results per page.
        
        Args:
            limit: Number of results per page (10-100)
            
        Returns:
            SmsRecipientsBuilder: Builder instance for method chaining
        """
        self._limit = limit
        return self

    def sms_recipient_id(self, sms_recipient_id: str) -> "SmsRecipientsBuilder":
        """
        Set the SMS recipient ID for get and update operations.
        
        Args:
            sms_recipient_id: SMS recipient ID
            
        Returns:
            SmsRecipientsBuilder: Builder instance for method chaining
        """
        self._sms_recipient_id = sms_recipient_id
        return self

    def build_list_request(self) -> SmsRecipientsListRequest:
        """
        Build a request for listing SMS recipients.
        
        Returns:
            SmsRecipientsListRequest: Request object for listing SMS recipients
        """
        query_params = SmsRecipientsListQueryParams()
        
        if self._status is not None:
            query_params.status = self._status
        if self._sms_number_id is not None:
            query_params.sms_number_id = self._sms_number_id
        if self._page is not None:
            query_params.page = self._page
        if self._limit is not None:
            query_params.limit = self._limit
            
        return SmsRecipientsListRequest(query_params=query_params)

    def build_get_request(self) -> SmsRecipientGetRequest:
        """
        Build a request for getting a single SMS recipient.
        
        Returns:
            SmsRecipientGetRequest: Request object for getting SMS recipient
            
        Raises:
            ValueError: If SMS recipient ID is not set
        """
        if self._sms_recipient_id is None:
            raise ValueError("SMS recipient ID is required for get request")
            
        return SmsRecipientGetRequest(sms_recipient_id=self._sms_recipient_id)

    def build_update_request(self, status: SmsRecipientStatus) -> SmsRecipientUpdateRequest:
        """
        Build a request for updating an SMS recipient.
        
        Args:
            status: New status for the SMS recipient
            
        Returns:
            SmsRecipientUpdateRequest: Request object for updating SMS recipient
            
        Raises:
            ValueError: If SMS recipient ID is not set
        """
        if self._sms_recipient_id is None:
            raise ValueError("SMS recipient ID is required for update request")
            
        return SmsRecipientUpdateRequest(
            sms_recipient_id=self._sms_recipient_id,
            status=status
        ) 