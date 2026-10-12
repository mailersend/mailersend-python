"""WhatsApp Messages resource."""

from .base import BaseResource
from ..models.whatsapp_messages import (
    WhatsAppMessagesListRequest,
    WhatsAppMessageGetRequest,
)
from ..models.base import APIResponse


class WhatsAppMessages(BaseResource):
    """WhatsApp Messages resource for MailerSend API."""

    def list_whatsapp_messages(
        self, request: WhatsAppMessagesListRequest
    ) -> APIResponse:
        """
        List WhatsApp messages.

        Args:
            request: WhatsAppMessagesListRequest object containing query parameters

        Returns:
            APIResponse: Response containing list of WhatsApp messages
        """
        params = request.to_query_params()

        self.logger.debug(
            "Listing WhatsApp messages with page: %s, limit: %s",
            request.query_params.page,
            request.query_params.limit,
        )

        return self._request(method="GET", path="whatsapp/messages", params=params)

    def get_whatsapp_message(self, request: WhatsAppMessageGetRequest) -> APIResponse:
        """
        Get a single WhatsApp message with the status and activity of its recipients.

        Args:
            request: WhatsAppMessageGetRequest object containing WhatsApp message ID

        Returns:
            APIResponse: Response containing WhatsApp message details
        """
        self.logger.debug("Getting WhatsApp message: %s", request.whatsapp_message_id)

        return self._request(
            method="GET", path=f"whatsapp/messages/{request.whatsapp_message_id}"
        )
