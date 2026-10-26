"""WhatsApp Inbound Messages builder for MailerSend SDK."""

from datetime import datetime
from typing import List, Optional, Union

from ..models.whatsapp_inbound_messages import (
    WhatsAppInboundMessagesListRequest,
    WhatsAppInboundMessagesListQueryParams,
    WhatsAppInboundMessageGetRequest,
    WhatsAppInboundMessageType,
)


class WhatsAppInboundMessagesBuilder:
    """Builder for WhatsApp Inbound Messages API requests."""

    def __init__(self) -> None:
        """Initialize the WhatsAppInboundMessagesBuilder."""
        self._whatsapp_account_id: Optional[str] = None
        self._from_number: Optional[str] = None
        self._type: Optional[List[Union[WhatsAppInboundMessageType, str]]] = None
        self._date_from: Optional[Union[int, str]] = None
        self._date_to: Optional[Union[int, str]] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        self._whatsapp_inbound_message_id: Optional[str] = None

    def whatsapp_account_id(
        self, whatsapp_account_id: str
    ) -> "WhatsAppInboundMessagesBuilder":
        """
        Set the WhatsApp account (sender) ID filter.

        Args:
            whatsapp_account_id: Sender ID of the phone number that received the messages

        Returns:
            WhatsAppInboundMessagesBuilder: Builder instance for method chaining
        """
        self._whatsapp_account_id = whatsapp_account_id
        return self

    def from_number(self, phone_number: str) -> "WhatsAppInboundMessagesBuilder":
        """
        Set the customer filter.

        Args:
            phone_number: Customer's phone number in international format, or
                their BSUID when Meta withholds the phone number

        Returns:
            WhatsAppInboundMessagesBuilder: Builder instance for method chaining
        """
        self._from_number = phone_number
        return self

    def type(
        self,
        types: Union[
            WhatsAppInboundMessageType,
            str,
            List[Union[WhatsAppInboundMessageType, str]],
        ],
    ) -> "WhatsAppInboundMessagesBuilder":
        """
        Set the message type filter. Multiple values are combined with OR.

        Args:
            types: A message type, or a list of them (e.g. "image" or ["text", "image"])

        Returns:
            WhatsAppInboundMessagesBuilder: Builder instance for method chaining
        """
        self._type = [types] if isinstance(types, str) else list(types)
        return self

    def date_from(
        self, date_from: Union[datetime, int, str]
    ) -> "WhatsAppInboundMessagesBuilder":
        """
        Set the exclusive start of the date range.

        Args:
            date_from: datetime, Unix timestamp or ISO 8601 datetime with a time

        Returns:
            WhatsAppInboundMessagesBuilder: Builder instance for method chaining
        """
        self._date_from = self._convert_to_timestamp(date_from)
        return self

    def date_to(
        self, date_to: Union[datetime, int, str]
    ) -> "WhatsAppInboundMessagesBuilder":
        """
        Set the exclusive end of the date range.

        Args:
            date_to: datetime, Unix timestamp or ISO 8601 datetime with a time

        Returns:
            WhatsAppInboundMessagesBuilder: Builder instance for method chaining
        """
        self._date_to = self._convert_to_timestamp(date_to)
        return self

    def page(self, page: int) -> "WhatsAppInboundMessagesBuilder":
        """
        Set the page number for pagination.

        Args:
            page: Page number (1-100)

        Returns:
            WhatsAppInboundMessagesBuilder: Builder instance for method chaining
        """
        self._page = page
        return self

    def limit(self, limit: int) -> "WhatsAppInboundMessagesBuilder":
        """
        Set the limit for number of results per page.

        Args:
            limit: Number of results per page (1-100)

        Returns:
            WhatsAppInboundMessagesBuilder: Builder instance for method chaining
        """
        self._limit = limit
        return self

    def whatsapp_inbound_message_id(
        self, whatsapp_inbound_message_id: str
    ) -> "WhatsAppInboundMessagesBuilder":
        """
        Set the WhatsApp inbound message ID for get operations.

        Args:
            whatsapp_inbound_message_id: WhatsApp inbound message ID

        Returns:
            WhatsAppInboundMessagesBuilder: Builder instance for method chaining
        """
        self._whatsapp_inbound_message_id = whatsapp_inbound_message_id
        return self

    def _convert_to_timestamp(
        self, value: Union[datetime, int, str]
    ) -> Union[int, str]:
        if isinstance(value, datetime):
            return int(value.timestamp())
        return value

    def build_list_request(self) -> WhatsAppInboundMessagesListRequest:
        """
        Build a request for listing WhatsApp inbound messages.

        Returns:
            WhatsAppInboundMessagesListRequest: Request object for listing inbound messages
        """
        params = {}

        if self._whatsapp_account_id is not None:
            params["whatsapp_account_id"] = self._whatsapp_account_id
        if self._from_number is not None:
            params["from_"] = self._from_number
        if self._type is not None:
            params["type"] = self._type
        if self._date_from is not None:
            params["date_from"] = self._date_from
        if self._date_to is not None:
            params["date_to"] = self._date_to
        if self._page is not None:
            params["page"] = self._page
        if self._limit is not None:
            params["limit"] = self._limit

        return WhatsAppInboundMessagesListRequest(
            query_params=WhatsAppInboundMessagesListQueryParams(**params)
        )

    def build_get_request(self) -> WhatsAppInboundMessageGetRequest:
        """
        Build a request for getting a single WhatsApp inbound message.

        Returns:
            WhatsAppInboundMessageGetRequest: Request object for getting inbound message

        Raises:
            ValueError: If WhatsApp inbound message ID is not set
        """
        if self._whatsapp_inbound_message_id is None:
            raise ValueError("WhatsApp inbound message ID is required for get request")

        return WhatsAppInboundMessageGetRequest(
            whatsapp_inbound_message_id=self._whatsapp_inbound_message_id
        )
