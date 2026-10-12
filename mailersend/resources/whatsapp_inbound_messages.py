"""WhatsApp Inbound Messages resource."""

from .base import BaseResource
from ..models.whatsapp_inbound_messages import (
    WhatsAppInboundMessagesListRequest,
    WhatsAppInboundMessageGetRequest,
)
from ..models.base import APIResponse


class WhatsAppInboundMessages(BaseResource):
    """WhatsApp Inbound Messages resource for MailerSend API."""

    def list_whatsapp_inbound_messages(
        self, request: WhatsAppInboundMessagesListRequest
    ) -> APIResponse:
        """
        List WhatsApp inbound messages.

        Args:
            request: WhatsAppInboundMessagesListRequest object containing query parameters

        Returns:
            APIResponse: Response containing list of WhatsApp inbound messages
        """
        params = request.to_query_params()

        self.logger.debug(
            "Listing WhatsApp inbound messages with page: %s, limit: %s",
            request.query_params.page,
            request.query_params.limit,
        )

        return self._request(
            method="GET", path="whatsapp/inbound-messages", params=params
        )

    def get_whatsapp_inbound_message(
        self, request: WhatsAppInboundMessageGetRequest
    ) -> APIResponse:
        """
        Get a single WhatsApp inbound message.

        Args:
            request: WhatsAppInboundMessageGetRequest object containing inbound message ID

        Returns:
            APIResponse: Response containing WhatsApp inbound message details
        """
        self.logger.debug(
            "Getting WhatsApp inbound message: %s",
            request.whatsapp_inbound_message_id,
        )

        return self._request(
            method="GET",
            path=f"whatsapp/inbound-messages/{request.whatsapp_inbound_message_id}",
        )
