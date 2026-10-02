"""WhatsApp Messages builder for MailerSend SDK."""

from typing import Optional

from ..models.whatsapp_messages import (
    WhatsAppMessagesListRequest,
    WhatsAppMessagesListQueryParams,
    WhatsAppMessageGetRequest,
)


class WhatsAppMessagesBuilder:
    """Builder for WhatsApp Messages API requests."""

    def __init__(self) -> None:
        """Initialize the WhatsAppMessagesBuilder."""
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        self._whatsapp_message_id: Optional[str] = None

    def page(self, page: int) -> "WhatsAppMessagesBuilder":
        """
        Set the page number for pagination.

        Args:
            page: Page number (must be >= 1)

        Returns:
            WhatsAppMessagesBuilder: Builder instance for method chaining
        """
        self._page = page
        return self

    def limit(self, limit: int) -> "WhatsAppMessagesBuilder":
        """
        Set the limit for number of results per page.

        Args:
            limit: Number of results per page (10-100)

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

    def build_list_request(self) -> WhatsAppMessagesListRequest:
        """
        Build a request for listing WhatsApp messages.

        Returns:
            WhatsAppMessagesListRequest: Request object for listing WhatsApp messages
        """
        params = {}

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
