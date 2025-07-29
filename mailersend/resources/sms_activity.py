"""
SMS Activity API resource.
"""

from .base import BaseResource
from ..models.sms_activity import SmsActivityListRequest, SmsMessageGetRequest
from ..models.base import APIResponse


class SmsActivity(BaseResource):
    """Resource for SMS Activity API endpoints."""

    def list(self, request: SmsActivityListRequest) -> APIResponse:
        """
        Get a list of SMS activities.

        Args:
            request: SMS activity list request

        Returns:
            API response with SMS activities

        Raises:
            ValidationError: If request is invalid
        """
        self.logger.debug("Preparing to list SMS activities")

        # Convert to query parameters
        params = request.to_query_params()

        self.logger.debug("Listing SMS activities with params: %s", params)

        # Make API request
        response = self.client.request(
            method="GET", endpoint="sms-activity", params=params
        )

        return self._create_response(response)

    def get(self, request: SmsMessageGetRequest) -> APIResponse:
        """
        Get activity of a single SMS message.

        Args:
            request: SMS message get request

        Returns:
            API response with SMS message activity
        """
        self.logger.debug("Getting SMS message activity: %s", request.sms_message_id)

        # Make API request
        response = self.client.request(
            method="GET", endpoint=f"sms-messages/{request.sms_message_id}"
        )

        return self._create_response(response)
