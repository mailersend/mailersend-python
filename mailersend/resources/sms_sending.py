from .base import BaseResource
from ..models.sms_sending import SmsSendRequest
from ..models.base import APIResponse


class SmsSending(BaseResource):
    """
    Client for interacting with the MailerSend SMS Sending API.
    """

    def send(self, request: SmsSendRequest) -> APIResponse:
        """
        Send an SMS message.

        Args:
            request: SmsSendRequest with SMS details

        Returns:
            APIResponse with SMS sending response and metadata
        """
        self.logger.debug("Preparing to send SMS message")

        # Convert to JSON payload
        payload = request.to_json()

        self.logger.debug(f"SMS payload: {payload}")

        response = self.client.request(method="POST", endpoint="sms", body=payload)

        return self._create_response(response)
