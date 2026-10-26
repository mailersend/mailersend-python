"""WhatsApp Items builder for MailerSend SDK."""

from datetime import datetime
from typing import List, Optional, Union

from ..models.whatsapp_items import (
    WhatsAppItemsListRequest,
    WhatsAppItemsListQueryParams,
    WhatsAppItemGetRequest,
    WhatsAppItemStatus,
)


class WhatsAppItemsBuilder:
    """Builder for WhatsApp Items API requests."""

    def __init__(self) -> None:
        """Initialize the WhatsAppItemsBuilder."""
        self._recipient: Optional[str] = None
        self._whatsapp_message_id: Optional[str] = None
        self._status: Optional[List[Union[WhatsAppItemStatus, str]]] = None
        self._whatsapp_account_id: Optional[str] = None
        self._from_number: Optional[str] = None
        self._template_id: Optional[str] = None
        self._date_from: Optional[Union[int, str]] = None
        self._date_to: Optional[Union[int, str]] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        self._whatsapp_item_id: Optional[str] = None

    def recipient(self, recipient: str) -> "WhatsAppItemsBuilder":
        """
        Set the recipient filter.

        Args:
            recipient: Recipient's phone number in international format,
                WhatsApp username or BSUID

        Returns:
            WhatsAppItemsBuilder: Builder instance for method chaining
        """
        self._recipient = recipient
        return self

    def whatsapp_message_id(self, whatsapp_message_id: str) -> "WhatsAppItemsBuilder":
        """
        Set the WhatsApp message ID filter.

        Args:
            whatsapp_message_id: ID of the message the items belong to

        Returns:
            WhatsAppItemsBuilder: Builder instance for method chaining
        """
        self._whatsapp_message_id = whatsapp_message_id
        return self

    def status(
        self,
        statuses: Union[WhatsAppItemStatus, str, List[Union[WhatsAppItemStatus, str]]],
    ) -> "WhatsAppItemsBuilder":
        """
        Set the status filter. Multiple values are combined with OR.

        Args:
            statuses: A status, or a list of statuses (e.g. "failed" or ["delivered", "read"])

        Returns:
            WhatsAppItemsBuilder: Builder instance for method chaining
        """
        self._status = [statuses] if isinstance(statuses, str) else list(statuses)
        return self

    def whatsapp_account_id(self, whatsapp_account_id: str) -> "WhatsAppItemsBuilder":
        """
        Set the WhatsApp account (sender) ID filter.

        Args:
            whatsapp_account_id: MailerSend sender ID the messages were sent from

        Returns:
            WhatsAppItemsBuilder: Builder instance for method chaining
        """
        self._whatsapp_account_id = whatsapp_account_id
        return self

    def from_number(self, phone_number: str) -> "WhatsAppItemsBuilder":
        """
        Set the sender phone number filter.

        Args:
            phone_number: Sender's phone number in international format

        Returns:
            WhatsAppItemsBuilder: Builder instance for method chaining
        """
        self._from_number = phone_number
        return self

    def template_id(self, template_id: str) -> "WhatsAppItemsBuilder":
        """
        Set the template ID filter.

        Args:
            template_id: ID of the template that was sent

        Returns:
            WhatsAppItemsBuilder: Builder instance for method chaining
        """
        self._template_id = template_id
        return self

    def date_from(self, date_from: Union[datetime, int, str]) -> "WhatsAppItemsBuilder":
        """
        Set the exclusive start of the date range.

        Args:
            date_from: datetime, Unix timestamp or ISO 8601 datetime with a time

        Returns:
            WhatsAppItemsBuilder: Builder instance for method chaining
        """
        self._date_from = self._convert_to_timestamp(date_from)
        return self

    def date_to(self, date_to: Union[datetime, int, str]) -> "WhatsAppItemsBuilder":
        """
        Set the exclusive end of the date range.

        Args:
            date_to: datetime, Unix timestamp or ISO 8601 datetime with a time

        Returns:
            WhatsAppItemsBuilder: Builder instance for method chaining
        """
        self._date_to = self._convert_to_timestamp(date_to)
        return self

    def page(self, page: int) -> "WhatsAppItemsBuilder":
        """
        Set the page number for pagination.

        Args:
            page: Page number (1-100)

        Returns:
            WhatsAppItemsBuilder: Builder instance for method chaining
        """
        self._page = page
        return self

    def limit(self, limit: int) -> "WhatsAppItemsBuilder":
        """
        Set the limit for number of results per page.

        Args:
            limit: Number of results per page (1-100)

        Returns:
            WhatsAppItemsBuilder: Builder instance for method chaining
        """
        self._limit = limit
        return self

    def whatsapp_item_id(self, whatsapp_item_id: str) -> "WhatsAppItemsBuilder":
        """
        Set the WhatsApp item ID for get operations.

        Args:
            whatsapp_item_id: WhatsApp item ID

        Returns:
            WhatsAppItemsBuilder: Builder instance for method chaining
        """
        self._whatsapp_item_id = whatsapp_item_id
        return self

    def _convert_to_timestamp(
        self, value: Union[datetime, int, str]
    ) -> Union[int, str]:
        if isinstance(value, datetime):
            return int(value.timestamp())
        return value

    def build_list_request(self) -> WhatsAppItemsListRequest:
        """
        Build a request for listing WhatsApp items.

        Returns:
            WhatsAppItemsListRequest: Request object for listing WhatsApp items
        """
        params = {}

        if self._recipient is not None:
            params["recipient"] = self._recipient
        if self._whatsapp_message_id is not None:
            params["whatsapp_message_id"] = self._whatsapp_message_id
        if self._status is not None:
            params["status"] = self._status
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

        return WhatsAppItemsListRequest(
            query_params=WhatsAppItemsListQueryParams(**params)
        )

    def build_get_request(self) -> WhatsAppItemGetRequest:
        """
        Build a request for getting a single WhatsApp item.

        Returns:
            WhatsAppItemGetRequest: Request object for getting WhatsApp item

        Raises:
            ValueError: If WhatsApp item ID is not set
        """
        if self._whatsapp_item_id is None:
            raise ValueError("WhatsApp item ID is required for get request")

        return WhatsAppItemGetRequest(whatsapp_item_id=self._whatsapp_item_id)
