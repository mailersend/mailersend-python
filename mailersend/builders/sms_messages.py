"""SMS Messages builder."""

from mailersend.models.sms_messages import (
    SmsMessagesListRequest,
    SmsMessagesListQueryParams,
    SmsMessageGetRequest,
)
from mailersend.exceptions import ValidationError


class SmsMessagesBuilder:
    """Builder for SMS Messages requests."""

    def __init__(self):
        """Initialize the builder."""
        self._sms_message_id = None
        self._page = 1
        self._limit = 25

    def sms_message_id(self, sms_message_id: str) -> "SmsMessagesBuilder":
        """
        Set the SMS message ID.

        Args:
            sms_message_id: SMS message ID

        Returns:
            SmsMessagesBuilder: Builder instance for method chaining
        """
        self._sms_message_id = sms_message_id
        return self

    def page(self, page: int) -> "SmsMessagesBuilder":
        """
        Set the page number.

        Args:
            page: Page number (must be >= 1)

        Returns:
            SmsMessagesBuilder: Builder instance for method chaining

        Raises:
            ValidationError: If page is less than 1
        """
        if page < 1:
            raise ValidationError("Page must be >= 1")
        self._page = page
        return self

    def limit(self, limit: int) -> "SmsMessagesBuilder":
        """
        Set the limit.

        Args:
            limit: Number of results per page (must be between 10 and 100)

        Returns:
            SmsMessagesBuilder: Builder instance for method chaining

        Raises:
            ValidationError: If limit is not between 10 and 100
        """
        if limit < 10 or limit > 100:
            raise ValidationError("Limit must be between 10 and 100")
        self._limit = limit
        return self

    def build_sms_messages_list(self) -> SmsMessagesListRequest:
        """
        Build an SMS messages list request.

        Returns:
            SmsMessagesListRequest: Request object for listing SMS messages
        """
        query_params = SmsMessagesListQueryParams(page=self._page, limit=self._limit)

        return SmsMessagesListRequest(query_params=query_params)

    def build_sms_message_get(self) -> SmsMessageGetRequest:
        """
        Build an SMS message get request.

        Returns:
            SmsMessageGetRequest: Request object for getting SMS message

        Raises:
            ValidationError: If SMS message ID is not set
        """
        if not self._sms_message_id:
            raise ValidationError("SMS message ID is required")

        return SmsMessageGetRequest(sms_message_id=self._sms_message_id)
