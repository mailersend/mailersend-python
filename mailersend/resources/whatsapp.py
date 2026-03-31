"""WhatsApp resource."""

from .base import BaseResource
from ..models.whatsapp import WhatsAppSendRequest
from ..models.base import APIResponse


class WhatsApp(BaseResource):
    """
    Client for interacting with the MailerSend WhatsApp API.
    """

    def send(self, request: WhatsAppSendRequest) -> APIResponse:
        """
        Send a WhatsApp message.

        Args:
            request: WhatsAppSendRequest with message details

        Returns:
            APIResponse with WhatsApp sending response and metadata
        """
        self.logger.debug("Preparing to send WhatsApp message")

        payload = request.to_json()

        self.logger.debug("WhatsApp payload: %s", payload)

        response = self.client.request(
            method="POST", path="whatsapp/send", body=payload
        )

        return self._create_response(response)