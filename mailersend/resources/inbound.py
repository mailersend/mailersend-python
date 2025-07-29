from mailersend.models.inbound import (
    InboundListRequest,
    InboundGetRequest,
    InboundCreateRequest,
    InboundUpdateRequest,
    InboundDeleteRequest,
)
from mailersend.models.base import APIResponse
from mailersend.resources.base import BaseResource


class InboundResource(BaseResource):
    """Resource for managing inbound routes."""

    def list(self, request: InboundListRequest) -> APIResponse:
        """
        Get a list of inbound routes.

        Args:
            request: The inbound list request containing filtering and pagination parameters

        Returns:
            APIResponse containing the inbound routes list response
        """
        self.logger.debug("Preparing to list inbound routes with query parameters")

        # Extract query parameters
        params = request.to_query_params()

        self.logger.debug(
            f"Making API request to list inbound routes with params: {params}"
        )

        # Make API request
        response = self.client.request(
            method="GET", endpoint="inbound", params=params if params else None
        )

        return self._create_response(response)

    def get(self, request: InboundGetRequest) -> APIResponse:
        """
        Get a single inbound route by ID.

        Args:
            request: The inbound get request with inbound ID

        Returns:
            APIResponse containing the inbound route data
        """
        self.logger.debug(
            f"Preparing to get inbound route with ID: {request.inbound_id}"
        )

        # Make API request
        response = self.client.request(
            method="GET", endpoint=f"inbound/{request.inbound_id}"
        )

        return self._create_response(response)

    def create(self, request: InboundCreateRequest) -> APIResponse:
        """
        Create a new inbound route.

        Args:
            request: The inbound create request with all required data

        Returns:
            APIResponse containing the created inbound route response
        """
        self.logger.debug("Preparing to create inbound route")

        # Build request body using model's serialization method
        data = request.to_request_body()

        self.logger.debug(
            f"Making API request to create inbound route with data keys: {list(data.keys())}"
        )

        # Make API request
        response = self.client.request(method="POST", endpoint="inbound", body=data)

        return self._create_response(response)

    def update(self, request: InboundUpdateRequest) -> APIResponse:
        """
        Update an existing inbound route.

        Args:
            request: The inbound update request with inbound ID and update data

        Returns:
            APIResponse containing the updated response
        """
        self.logger.debug(
            f"Preparing to update inbound route with ID: {request.inbound_id}"
        )

        # Build request body using model's serialization method
        data = request.to_request_body()

        self.logger.debug(
            f"Making API request to update inbound route with data keys: {list(data.keys())}"
        )

        # Make API request
        response = self.client.request(
            method="PUT", endpoint=f"inbound/{request.inbound_id}", body=data
        )

        return self._create_response(response)

    def delete(self, request: InboundDeleteRequest) -> APIResponse:
        """
        Delete an inbound route.

        Args:
            request: The inbound delete request with inbound ID

        Returns:
            APIResponse containing the deletion result
        """
        self.logger.debug(
            f"Preparing to delete inbound route with ID: {request.inbound_id}"
        )

        # Make API request
        response = self.client.request(
            method="DELETE", endpoint=f"inbound/{request.inbound_id}"
        )

        return self._create_response(response)
