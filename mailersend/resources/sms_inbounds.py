"""SMS Inbounds resource."""

from .base import BaseResource
from ..models.sms_inbounds import (
    SmsInboundsListRequest,
    SmsInboundGetRequest,
    SmsInboundCreateRequest,
    SmsInboundUpdateRequest,
    SmsInboundDeleteRequest,
)
from ..models.base import APIResponse


class SmsInbounds(BaseResource):
    """SMS Inbounds resource for MailerSend API."""

    def list_sms_inbounds(self, request: SmsInboundsListRequest) -> APIResponse:
        """List SMS inbound routes.

        Args:
            request: SmsInboundsListRequest with query parameters

        Returns:
            APIResponse: Response containing list of SMS inbound routes
        """
        params = request.to_query_params()

        self.logger.debug("Listing SMS inbounds with filters: %s", params)

        response = self.client.request(
            method="GET", endpoint="sms-inbounds", params=params
        )
        return self._create_response(response)

    def get_sms_inbound(self, request: SmsInboundGetRequest) -> APIResponse:
        """Get a single SMS inbound route.

        Args:
            request: SmsInboundGetRequest with inbound ID

        Returns:
            APIResponse: Response containing SMS inbound route details
        """
        self.logger.debug("Getting SMS inbound: %s", request.sms_inbound_id)

        response = self.client.request(
            method="GET", endpoint=f"sms-inbounds/{request.sms_inbound_id}"
        )

        return self._create_response(response)

    def create_sms_inbound(self, request: SmsInboundCreateRequest) -> APIResponse:
        """Create a new SMS inbound route.

        Args:
            request: SmsInboundCreateRequest with inbound route details

        Returns:
            APIResponse: Response containing created SMS inbound route
        """
        self.logger.debug(
            "Creating SMS inbound: %s for SMS number: %s",
            request.name,
            request.sms_number_id,
        )

        response = self.client.request(
            method="POST", endpoint="sms-inbounds", body=request.to_request_body()
        )

        return self._create_response(response)

    def update_sms_inbound(self, request: SmsInboundUpdateRequest) -> APIResponse:
        """Update an existing SMS inbound route.

        Args:
            request: SmsInboundUpdateRequest with inbound ID and updated fields

        Returns:
            APIResponse: Response containing updated SMS inbound route
        """
        self.logger.debug("Updating SMS inbound: %s", request.sms_inbound_id)

        response = self.client.request(
            method="PUT",
            endpoint=f"sms-inbounds/{request.sms_inbound_id}",
            body=request.to_request_body(),
        )

        return self._create_response(response)

    def delete_sms_inbound(self, request: SmsInboundDeleteRequest) -> APIResponse:
        """Delete an SMS inbound route.

        Args:
            request: SmsInboundDeleteRequest with inbound ID

        Returns:
            APIResponse: Response confirming deletion
        """
        self.logger.debug("Deleting SMS inbound: %s", request.sms_inbound_id)

        response = self.client.request(
            method="DELETE", endpoint=f"sms-inbounds/{request.sms_inbound_id}"
        )

        return self._create_response(response)
