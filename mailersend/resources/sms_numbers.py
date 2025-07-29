"""SMS Numbers resource"""

from .base import BaseResource
from ..models.sms_numbers import (
    SmsNumbersListRequest,
    SmsNumberGetRequest,
    SmsNumberUpdateRequest,
    SmsNumberDeleteRequest,
)
from ..models.base import APIResponse


class SmsNumbers(BaseResource):
    """
    Client for interacting with the MailerSend SMS Phone Numbers API.
    """

    def list(self, request: SmsNumbersListRequest) -> APIResponse:
        """
        Get a list of SMS phone numbers.

        Args:
            request: SmsNumbersListRequest with query parameters

        Returns:
            APIResponse with SMS phone numbers list and metadata
        """
        self.logger.debug("Preparing to list SMS phone numbers")

        # Convert to query parameters
        params = request.to_query_params()

        self.logger.debug("Listing SMS phone numbers with params: %s", params)

        response = self.client.request(
            method="GET", path="sms-numbers", params=params
        )

        return self._create_response(response)

    def get(self, request: SmsNumberGetRequest) -> APIResponse:
        """
        Get a specific SMS phone number.

        Args:
            request: SmsNumberGetRequest with SMS number ID

        Returns:
            APIResponse with SMS phone number data and metadata
        """
        self.logger.debug("Getting SMS phone number: %s", request.sms_number_id)

        response = self.client.request(
            method="GET", path=f"sms-numbers/{request.sms_number_id}"
        )

        return self._create_response(response)

    def update(self, request: SmsNumberUpdateRequest) -> APIResponse:
        """
        Update a specific SMS phone number.

        Args:
            request: SmsNumberUpdateRequest with SMS number ID and update data

        Returns:
            APIResponse with updated SMS phone number data and metadata
        """
        self.logger.debug("Preparing to update SMS phone number")

        # Convert to JSON payload
        payload = request.to_json()

        self.logger.debug("Updating SMS phone number: %s", payload)

        response = self.client.request(
            method="PUT", path=f"sms-numbers/{request.sms_number_id}", body=payload
        )

        return self._create_response(response)

    def delete(self, request: SmsNumberDeleteRequest) -> APIResponse:
        """
        Delete a specific SMS phone number.

        Args:
            request: SmsNumberDeleteRequest with SMS number ID

        Returns:
            APIResponse with deletion confirmation and metadata
        """
        self.logger.debug("Deleting SMS phone number: %s", request.sms_number_id)

        response = self.client.request(
            method="DELETE", path=f"sms-numbers/{request.sms_number_id}"
        )

        return self._create_response(response)
