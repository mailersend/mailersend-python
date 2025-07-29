"""Builder for SMS Phone Numbers API requests."""

from typing import Optional
from ..models.sms_numbers import (
    SmsNumbersListRequest,
    SmsNumberGetRequest,
    SmsNumberUpdateRequest,
    SmsNumberDeleteRequest,
)


class SmsNumbersBuilder:
    """Builder for constructing SMS Phone Numbers API requests."""

    def __init__(self):
        """Initialize the builder."""
        self._paused: Optional[bool] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        self._sms_number_id: Optional[str] = None

    def paused(self, paused: bool) -> "SmsNumbersBuilder":
        """
        Set the paused filter for listing SMS phone numbers.

        Args:
            paused: Filter by paused status

        Returns:
            Self for method chaining
        """
        self._paused = paused
        return self

    def page(self, page: int) -> "SmsNumbersBuilder":
        """
        Set the page number for pagination.

        Args:
            page: Page number to retrieve

        Returns:
            Self for method chaining
        """
        self._page = page
        return self

    def limit(self, limit: int) -> "SmsNumbersBuilder":
        """
        Set the limit for pagination.

        Args:
            limit: Number of items per page (10-100)

        Returns:
            Self for method chaining
        """
        self._limit = limit
        return self

    def sms_number_id(self, sms_number_id: str) -> "SmsNumbersBuilder":
        """
        Set the SMS phone number ID.

        Args:
            sms_number_id: The SMS phone number ID

        Returns:
            Self for method chaining
        """
        self._sms_number_id = sms_number_id
        return self

    def build_list_request(self) -> SmsNumbersListRequest:
        """
        Build a request for listing SMS phone numbers.

        Returns:
            SmsNumbersListRequest object
        """
        return SmsNumbersListRequest(
            paused=self._paused, page=self._page, limit=self._limit
        )

    def build_get_request(self) -> SmsNumberGetRequest:
        """
        Build a request for getting a specific SMS phone number.

        Returns:
            SmsNumberGetRequest object

        Raises:
            ValueError: If SMS number ID is not set
        """
        if not self._sms_number_id:
            raise ValueError("SMS number ID must be set")

        return SmsNumberGetRequest(sms_number_id=self._sms_number_id)

    def build_update_request(self) -> SmsNumberUpdateRequest:
        """
        Build a request for updating an SMS phone number.

        Returns:
            SmsNumberUpdateRequest object

        Raises:
            ValueError: If SMS number ID is not set
        """
        if not self._sms_number_id:
            raise ValueError("SMS number ID must be set")

        return SmsNumberUpdateRequest(
            sms_number_id=self._sms_number_id, paused=self._paused
        )

    def build_delete_request(self) -> SmsNumberDeleteRequest:
        """
        Build a request for deleting an SMS phone number.

        Returns:
            SmsNumberDeleteRequest object

        Raises:
            ValueError: If SMS number ID is not set
        """
        if not self._sms_number_id:
            raise ValueError("SMS number ID must be set")

        return SmsNumberDeleteRequest(sms_number_id=self._sms_number_id)

    def reset(self) -> "SmsNumbersBuilder":
        """
        Reset the builder to initial state.

        Returns:
            Self for method chaining
        """
        self._paused = None
        self._page = None
        self._limit = None
        self._sms_number_id = None
        return self
