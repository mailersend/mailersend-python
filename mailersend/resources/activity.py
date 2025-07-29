"""Activity resource"""

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
        """
        self.logger.debug("Preparing to get activity data")

        # Convert to query parameters for the API request
        params = request.to_query_params()

        self.logger.debug("Getting activity data for domain: %s", request.domain_id)
        self.logger.debug("Query params: %s", params)

        response = self.client.request(
            method='GET', endpoint=f'activity/{request.domain_id}', params=params
        )

        return self._create_response(response)

    def get_single(self, request: SingleActivityRequest) -> APIResponse:
        """
        Get a single activity by its ID.

        Args:
            request: A fully-validated SingleActivityRequest object

        Returns:
            APIResponse with single activity data
        """
        self.logger.debug("Preparing to get single activity")
        self.logger.debug("Getting single activity: %s", request.activity_id)

        response = self.client.request(method='GET', endpoint=f'activities/{request.activity_id}')

        return self._create_response(response)
