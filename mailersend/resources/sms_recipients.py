"""SMS Recipients resource."""

from .base import BaseResource
from ..models.sms_recipients import (
    SmsRecipientsListRequest,
    SmsRecipientGetRequest,
    SmsRecipientUpdateRequest,
)
from ..models.base import APIResponse


class SmsRecipients(BaseResource):
    """SMS Recipients resource for MailerSend API."""

    def list_sms_recipients(self, request: SmsRecipientsListRequest) -> APIResponse:
        """
        List SMS recipients.

        Args:
            request: SmsRecipientsListRequest object containing query parameters

        Returns:
            APIResponse: Response containing list of SMS recipients
        """
        params = request.to_query_params()

        self.logger.debug(
            "Listing SMS recipients with page: {request.query_params.page}, limit: %s",
            request.query_params.limit,
        )

        response = self.client.request(
            method="GET", endpoint="sms-recipients", params=params
        )

        return self._create_response(response)

    def get_sms_recipient(self, request: SmsRecipientGetRequest) -> APIResponse:
        """
        Get a single SMS recipient.

        Args:
            request: SmsRecipientGetRequest object containing SMS recipient ID

        Returns:
            APIResponse: Response containing SMS recipient details
        """
        self.logger.debug("Getting SMS recipient: %s", request.sms_recipient_id)

        response = self.client.request(
            method="GET", endpoint=f"sms-recipients/{request.sms_recipient_id}"
        )

        return self._create_response(response)

    def update_sms_recipient(self, request: SmsRecipientUpdateRequest) -> APIResponse:
        """
        Update a single SMS recipient.

        Args:
            request: SmsRecipientUpdateRequest object containing SMS recipient ID and new status

        Returns:
            APIResponse: Response containing updated SMS recipient
        """
        self.logger.debug(
            "Updating SMS recipient: {request.sms_recipient_id} to status: %s",
            request.status,
        )

        response = self.client.request(
            method="PUT",
            endpoint=f"sms-recipients/{request.sms_recipient_id}",
            body=request.to_request_body(),
        )

        return self._create_response(response)
