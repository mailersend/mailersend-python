"""Schedules resource"""

from .base import BaseResource
from ..models.schedules import (
    SchedulesListRequest,
    ScheduleGetRequest,
    ScheduleDeleteRequest,
)
from ..models.base import APIResponse


class Schedules(BaseResource):
    """
    Client for interacting with the MailerSend Message Schedules API.

    Provides methods for managing scheduled messages.
    """

    def list_schedules(self, request: SchedulesListRequest) -> APIResponse:
        """
        Retrieve a list of scheduled messages.

        Args:
            request: SchedulesListRequest with filtering and pagination options

        Returns:
            APIResponse containing the schedules list response
        """
        self.logger.debug("Preparing to list scheduled messages with query parameters")

        # Extract query parameters
        params = request.to_query_params()

        self.logger.debug("Making API request to list scheduled messages with params: %s", params)

        # Make API request
        response = self.client.request(
            method="GET",
            endpoint="message-schedules",
            params=params if params else None,
        )

        return self._create_response(response)

    def get_schedule(self, request: ScheduleGetRequest) -> APIResponse:
        """
        Retrieve information about a single scheduled message.

        Args:
            request: ScheduleGetRequest with message ID

        Returns:
            APIResponse containing the schedule response
        """
        self.logger.debug("Preparing to get scheduled message with ID: %s", request.message_id)

        # Make API request
        response = self.client.request(
            method="GET", endpoint=f"message-schedules/{request.message_id}"
        )

        return self._create_response(response)

    def delete_schedule(self, request: ScheduleDeleteRequest) -> APIResponse:
        """
        Delete a scheduled message.

        Args:
            request: ScheduleDeleteRequest with message ID to delete

        Returns:
            APIResponse (204 No Content on success)
        """
        self.logger.debug("Preparing to delete scheduled message with ID: %s", request.message_id)

        # Make API request
        response = self.client.request(
            method="DELETE", endpoint=f"message-schedules/{request.message_id}"
        )

        return self._create_response(response)
