"""
SMS Activity API resource.
"""

from .base import BaseResource
from ..models.sms_activity import SmsActivityListRequest, SmsMessageGetRequest
from ..models.base import APIResponse
from ..exceptions import ValidationError


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

        if not isinstance(request, SmsActivityListRequest):
            raise ValidationError("SmsActivityListRequest must be provided")

        # Convert to query parameters
        params = request.to_query_params()

        self.logger.info(f"Listing SMS activities with params: {params}")

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

        Raises:
            ValidationError: If request is invalid
        """
        self.logger.debug("Preparing to get SMS message activity")

        if not isinstance(request, SmsMessageGetRequest):
            raise ValidationError("SmsMessageGetRequest must be provided")

        self.logger.info(f"Getting SMS message activity: {request.sms_message_id}")

        # Make API request
        response = self.client.request(
            method="GET", endpoint=f"sms-messages/{request.sms_message_id}"
        )

        return self._create_response(response)
