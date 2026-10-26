"""WhatsApp Activities builder for MailerSend SDK."""

from datetime import datetime
from typing import List, Optional, Union

from ..models.whatsapp_activities import (
    WhatsAppActivitiesListRequest,
    WhatsAppActivitiesListQueryParams,
    WhatsAppActivityType,
)


class WhatsAppActivitiesBuilder:
    """Builder for WhatsApp Activities API requests."""

    def __init__(self) -> None:
        """Initialize the WhatsAppActivitiesBuilder."""
        self._whatsapp_item_id: Optional[str] = None
        self._whatsapp_message_id: Optional[str] = None
        self._recipient: Optional[str] = None
        self._type: Optional[List[Union[WhatsAppActivityType, str]]] = None
        self._date_from: Optional[Union[int, str]] = None
        self._date_to: Optional[Union[int, str]] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None

    def whatsapp_item_id(self, whatsapp_item_id: str) -> "WhatsAppActivitiesBuilder":
        """
        Set the WhatsApp item ID filter.

        Args:
            whatsapp_item_id: ID of the item the activities belong to

        Returns:
            WhatsAppActivitiesBuilder: Builder instance for method chaining
        """
        self._whatsapp_item_id = whatsapp_item_id
        return self

    def whatsapp_message_id(
        self, whatsapp_message_id: str
    ) -> "WhatsAppActivitiesBuilder":
        """
        Set the WhatsApp message ID filter.

        Args:
            whatsapp_message_id: ID of the message the activities belong to

        Returns:
            WhatsAppActivitiesBuilder: Builder instance for method chaining
        """
        self._whatsapp_message_id = whatsapp_message_id
        return self

    def recipient(self, recipient: str) -> "WhatsAppActivitiesBuilder":
        """
        Set the recipient filter.

        Args:
            recipient: Recipient's phone number in international format,
                WhatsApp username or BSUID

        Returns:
            WhatsAppActivitiesBuilder: Builder instance for method chaining
        """
        self._recipient = recipient
        return self

    def type(
        self,
        types: Union[WhatsAppActivityType, str, List[Union[WhatsAppActivityType, str]]],
    ) -> "WhatsAppActivitiesBuilder":
        """
        Set the activity type filter. Multiple values are combined with OR.

        Args:
            types: An activity type, or a list of them (e.g. "failed" or ["delivered", "read"])

        Returns:
            WhatsAppActivitiesBuilder: Builder instance for method chaining
        """
        self._type = [types] if isinstance(types, str) else list(types)
        return self

    def date_from(
        self, date_from: Union[datetime, int, str]
    ) -> "WhatsAppActivitiesBuilder":
        """
        Set the exclusive start of the date range.

        Args:
            date_from: datetime, Unix timestamp or ISO 8601 datetime with a time

        Returns:
            WhatsAppActivitiesBuilder: Builder instance for method chaining
        """
        self._date_from = self._convert_to_timestamp(date_from)
        return self

    def date_to(
        self, date_to: Union[datetime, int, str]
    ) -> "WhatsAppActivitiesBuilder":
        """
        Set the exclusive end of the date range.

        Args:
            date_to: datetime, Unix timestamp or ISO 8601 datetime with a time

        Returns:
            WhatsAppActivitiesBuilder: Builder instance for method chaining
        """
        self._date_to = self._convert_to_timestamp(date_to)
        return self

    def page(self, page: int) -> "WhatsAppActivitiesBuilder":
        """
        Set the page number for pagination.

        Args:
            page: Page number (1-100)

        Returns:
            WhatsAppActivitiesBuilder: Builder instance for method chaining
        """
        self._page = page
        return self

    def limit(self, limit: int) -> "WhatsAppActivitiesBuilder":
        """
        Set the limit for number of results per page.

        Args:
            limit: Number of results per page (1-100)

        Returns:
            WhatsAppActivitiesBuilder: Builder instance for method chaining
        """
        self._limit = limit
        return self

    def _convert_to_timestamp(
        self, value: Union[datetime, int, str]
    ) -> Union[int, str]:
        if isinstance(value, datetime):
            return int(value.timestamp())
        return value

    def build_list_request(self) -> WhatsAppActivitiesListRequest:
        """
        Build a request for listing WhatsApp activities.

        Returns:
            WhatsAppActivitiesListRequest: Request object for listing WhatsApp activities
        """
        params = {}

        if self._whatsapp_item_id is not None:
            params["whatsapp_item_id"] = self._whatsapp_item_id
        if self._whatsapp_message_id is not None:
            params["whatsapp_message_id"] = self._whatsapp_message_id
        if self._recipient is not None:
            params["recipient"] = self._recipient
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

        return WhatsAppActivitiesListRequest(
            query_params=WhatsAppActivitiesListQueryParams(**params)
        )
