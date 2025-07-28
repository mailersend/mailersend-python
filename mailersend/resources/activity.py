from .base import BaseResource
from ..models.activity import ActivityRequest, SingleActivityRequest
from ..models.base import APIResponse
from ..exceptions import ValidationError


class Activity(BaseResource):
    """
    Client for interacting with the MailerSend Activity API.
    """

    def get(self, request: ActivityRequest) -> APIResponse:
        """
        Get activity data for a domain.

        Args:
            request: A fully-validated ActivityRequest object

        Returns:
            APIResponse with activity data and metadata

        Raises:
            ValidationError: If the ActivityRequest is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Preparing to get activity data")

        if not request:
            self.logger.error("No ActivityRequest object provided")
            raise ValidationError("ActivityRequest must be provided")

        if not isinstance(request, ActivityRequest):
            self.logger.error("Invalid ActivityRequest object provided")
            raise ValidationError("ActivityRequest must be provided")

        # Convert to query parameters for the API request
        params = request.to_query_params()
        
        self.logger.info(f"Getting activity data for domain: {request.domain_id}")
        self.logger.debug(f"Query params: {params}")

        response = self.client.request("GET", f"activity/{request.domain_id}", params=params)

        return self._create_response(response)

    def get_single(self, request: SingleActivityRequest) -> APIResponse:
        """
        Get a single activity by its ID.

        Args:
            request: A fully-validated SingleActivityRequest object

        Returns:
            APIResponse with single activity data

        Raises:
            ValidationError: If the SingleActivityRequest is invalid
            ResourceNotFoundError: If the activity is not found
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Preparing to get single activity")

        if not request:
            self.logger.error("No SingleActivityRequest object provided")
            raise ValidationError("SingleActivityRequest must be provided")

        if not isinstance(request, SingleActivityRequest):
            self.logger.error("Invalid SingleActivityRequest object provided")
            raise ValidationError("SingleActivityRequest must be provided")
        
        self.logger.info(f"Getting single activity: {request.activity_id}")

        response = self.client.request("GET", f"activities/{request.activity_id}")

        return self._create_response(response)
