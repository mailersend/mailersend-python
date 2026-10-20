"""WhatsApp Messages builder for MailerSend SDK."""

from datetime import datetime
from typing import Optional, Union

from ..models.whatsapp_messages import (
    WhatsAppMessagesListRequest,
    WhatsAppMessagesListQueryParams,
    WhatsAppMessageGetRequest,
)


class WhatsAppMessagesBuilder:
    """Builder for WhatsApp Messages API requests."""

    def __init__(self) -> None:
        """Initialize the WhatsAppMessagesBuilder."""
        self._whatsapp_account_id: Optional[str] = None
        self._from_number: Optional[str] = None
        self._template_id: Optional[str] = None
        self._date_from: Optional[Union[int, str]] = None
        self._date_to: Optional[Union[int, str]] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        self._whatsapp_message_id: Optional[str] = None

    def whatsapp_account_id(
        self, whatsapp_account_id: str
    ) -> "WhatsAppMessagesBuilder":
        """
        Set the WhatsApp account (sender) ID filter.

        Args:
            whatsapp_account_id: MailerSend sender ID the messages were sent from

        Returns:
            WhatsAppMessagesBuilder: Builder instance for method chaining
        """
        self._whatsapp_account_id = whatsapp_account_id
        return self

    def from_number(self, phone_number: str) -> "WhatsAppMessagesBuilder":
        """
        Set the sender phone number filter.

        Args:
            phone_number: Sender's phone number in international format

        Returns:
            WhatsAppMessagesBuilder: Builder instance for method chaining
        """
        self._from_number = phone_number
        return self

    def template_id(self, template_id: str) -> "WhatsAppMessagesBuilder":
        """
        Set the template ID filter.

        Args:
            template_id: ID of the template that was sent

        Returns:
            WhatsAppMessagesBuilder: Builder instance for method chaining
        """
        self._template_id = template_id
        return self

    def date_from(
        self, date_from: Union[datetime, int, str]
    ) -> "WhatsAppMessagesBuilder":
        """
        Set the exclusive start of the date range.

        Args:
            date_from: datetime, Unix timestamp or ISO 8601 datetime with a time

        Returns:
            WhatsAppMessagesBuilder: Builder instance for method chaining
        """
        self._date_from = self._convert_to_timestamp(date_from)
        return self

    def date_to(self, date_to: Union[datetime, int, str]) -> "WhatsAppMessagesBuilder":
        """
        Set the exclusive end of the date range.

        Args:
            date_to: datetime, Unix timestamp or ISO 8601 datetime with a time

        Returns:
            WhatsAppMessagesBuilder: Builder instance for method chaining
        """
        self._date_to = self._convert_to_timestamp(date_to)
        return self

    def page(self, page: int) -> "WhatsAppMessagesBuilder":
        """
        Set the page number for pagination.

        Args:
            page: Page number (1-100)

        Returns:
            WhatsAppMessagesBuilder: Builder instance for method chaining
        """
        self._page = page
        return self

    def limit(self, limit: int) -> "WhatsAppMessagesBuilder":
        """
        Set the limit for number of results per page.

        Args:
            limit: Number of results per page (1-100)

        Returns:
            WhatsAppMessagesBuilder: Builder instance for method chaining
        """
        self._limit = limit
        return self

    def whatsapp_message_id(
        self, whatsapp_message_id: str
    ) -> "WhatsAppMessagesBuilder":
        """
        Set the WhatsApp message ID for get operations.

        Args:
            whatsapp_message_id: WhatsApp message ID

        Returns:
            WhatsAppMessagesBuilder: Builder instance for method chaining
        """
        self._whatsapp_message_id = whatsapp_message_id
        return self

    def _convert_to_timestamp(
        self, value: Union[datetime, int, str]
    ) -> Union[int, str]:
        if isinstance(value, datetime):
            return int(value.timestamp())
        return value

    def build_list_request(self) -> WhatsAppMessagesListRequest:
        """
        Build a request for listing WhatsApp messages.

        Returns:
            WhatsAppMessagesListRequest: Request object for listing WhatsApp messages
        """
        params = {}

        if self._whatsapp_account_id is not None:
            params["whatsapp_account_id"] = self._whatsapp_account_id
        if self._from_number is not None:
            params["from_"] = self._from_number
        if self._template_id is not None:
            params["template_id"] = self._template_id
        if self._date_from is not None:
            params["date_from"] = self._date_from
        if self._date_to is not None:
            params["date_to"] = self._date_to
        if self._page is not None:
            params["page"] = self._page
        if self._limit is not None:
            params["limit"] = self._limit

        return WhatsAppMessagesListRequest(
            query_params=WhatsAppMessagesListQueryParams(**params)
        )

    def build_get_request(self) -> WhatsAppMessageGetRequest:
        """
        Build a request for getting a single WhatsApp message.

        Returns:
            WhatsAppMessageGetRequest: Request object for getting WhatsApp message

        Raises:
            ValueError: If WhatsApp message ID is not set
        """
        if self._whatsapp_message_id is None:
            raise ValueError("WhatsApp message ID is required for get request")

        return WhatsAppMessageGetRequest(whatsapp_message_id=self._whatsapp_message_id)
