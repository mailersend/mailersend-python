"""WhatsApp Recipients builder for MailerSend SDK."""

from typing import Optional

from ..models.whatsapp_recipients import (
    WhatsAppRecipientsListRequest,
    WhatsAppRecipientsListQueryParams,
    WhatsAppRecipientGetRequest,
    WhatsAppRecipientStatus,
)


class WhatsAppRecipientsBuilder:
    """Builder for WhatsApp Recipients API requests."""

    def __init__(self) -> None:
        """Initialize the WhatsAppRecipientsBuilder."""
        self._status: Optional[WhatsAppRecipientStatus] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        self._whatsapp_recipient_id: Optional[str] = None

    def status(self, status: WhatsAppRecipientStatus) -> "WhatsAppRecipientsBuilder":
        """
        Set the status filter for listing WhatsApp recipients.

        Args:
            status: Status to filter by (active, invalid, suppressed or blocked)

        Returns:
            WhatsAppRecipientsBuilder: Builder instance for method chaining
        """
        self._status = status
        return self

    def page(self, page: int) -> "WhatsAppRecipientsBuilder":
        """
        Set the page number for pagination.

        Args:
            page: Page number (must be >= 1)

        Returns:
            WhatsAppRecipientsBuilder: Builder instance for method chaining
        """
        self._page = page
        return self

    def limit(self, limit: int) -> "WhatsAppRecipientsBuilder":
        """
        Set the limit for number of results per page.

        Args:
            limit: Number of results per page (10-100)

        Returns:
            WhatsAppRecipientsBuilder: Builder instance for method chaining
        """
        self._limit = limit
        return self

    def whatsapp_recipient_id(
        self, whatsapp_recipient_id: str
    ) -> "WhatsAppRecipientsBuilder":
        """
        Set the WhatsApp recipient ID for get operations.

        Args:
            whatsapp_recipient_id: WhatsApp recipient ID

        Returns:
            WhatsAppRecipientsBuilder: Builder instance for method chaining
        """
        self._whatsapp_recipient_id = whatsapp_recipient_id
        return self

    def build_list_request(self) -> WhatsAppRecipientsListRequest:
        """
        Build a request for listing WhatsApp recipients.

        Returns:
            WhatsAppRecipientsListRequest: Request object for listing WhatsApp recipients
        """
        params = {}

        if self._status is not None:
            params["status"] = self._status
        if self._page is not None:
            params["page"] = self._page
        if self._limit is not None:
            params["limit"] = self._limit

        return WhatsAppRecipientsListRequest(
            query_params=WhatsAppRecipientsListQueryParams(**params)
        )

    def build_get_request(self) -> WhatsAppRecipientGetRequest:
        """
        Build a request for getting a single WhatsApp recipient.

        Returns:
            WhatsAppRecipientGetRequest: Request object for getting WhatsApp recipient

        Raises:
            ValueError: If WhatsApp recipient ID is not set
        """
        if self._whatsapp_recipient_id is None:
            raise ValueError("WhatsApp recipient ID is required for get request")

        return WhatsAppRecipientGetRequest(
            whatsapp_recipient_id=self._whatsapp_recipient_id
        )
