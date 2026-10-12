"""WhatsApp Recipients resource."""

from .base import BaseResource
from ..models.whatsapp_recipients import (
    WhatsAppRecipientsListRequest,
    WhatsAppRecipientGetRequest,
)
from ..models.base import APIResponse


class WhatsAppRecipients(BaseResource):
    """WhatsApp Recipients resource for MailerSend API."""

    def list_whatsapp_recipients(
        self, request: WhatsAppRecipientsListRequest
    ) -> APIResponse:
        """
        List WhatsApp recipients.

        Args:
            request: WhatsAppRecipientsListRequest object containing query parameters

        Returns:
            APIResponse: Response containing list of WhatsApp recipients
        """
        params = request.to_query_params()

        self.logger.debug(
            "Listing WhatsApp recipients with page: %s, limit: %s",
            request.query_params.page,
            request.query_params.limit,
        )

        return self._request(method="GET", path="whatsapp/recipients", params=params)

    def get_whatsapp_recipient(
        self, request: WhatsAppRecipientGetRequest
    ) -> APIResponse:
        """
        Get a single WhatsApp recipient with their latest messages.

        Args:
            request: WhatsAppRecipientGetRequest object containing WhatsApp recipient ID

        Returns:
            APIResponse: Response containing WhatsApp recipient details
        """
        self.logger.debug(
            "Getting WhatsApp recipient: %s", request.whatsapp_recipient_id
        )

        return self._request(
            method="GET", path=f"whatsapp/recipients/{request.whatsapp_recipient_id}"
        )
