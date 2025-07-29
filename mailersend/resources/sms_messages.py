"""SMS Messages resource."""

from .base import BaseResource
from ..models.sms_messages import SmsMessagesListRequest, SmsMessageGetRequest
from ..models.base import APIResponse


class SmsMessages(BaseResource):
    """SMS Messages resource for MailerSend API."""

    def list_sms_messages(self, request: SmsMessagesListRequest) -> APIResponse:
        """
        List SMS messages.

        Args:
            request: SmsMessagesListRequest object containing query parameters

        Returns:
            APIResponse: Response containing list of SMS messages
        """
        params = request.to_query_params()

        self.logger.info(
            f"Listing SMS messages with page: {request.query_params.page}, limit: {request.query_params.limit}"
        )

        response = self.client.request(
            method="GET", endpoint="sms-messages", params=params
        )

        return self._create_response(response)

    def get_sms_message(self, request: SmsMessageGetRequest) -> APIResponse:
        """
        Get a single SMS message.

        Args:
            request: SmsMessageGetRequest object containing SMS message ID

        Returns:
            APIResponse: Response containing SMS message details
        """
        self.logger.info(f"Getting SMS message: {request.sms_message_id}")

        response = self.client.request(
            method="GET", endpoint=f"sms-messages/{request.sms_message_id}"
        )

        return self._create_response(response)
